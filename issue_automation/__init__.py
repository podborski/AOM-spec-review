import os
import re
import sys
import hashlib
import subprocess
from docx import Document
from github import Github, Auth
from argparse import ArgumentParser
from loguru import logger

LABELS = {
    "ed": "editorial",
    "ge": "general",
    "te": "technical",
    "?": "question",
}


def assert_log(condition, message):
    if not condition:
        logger.error(message)
        raise AssertionError(message)


def check_if_github_cli_is_installed():
    # Check if Github CLI is installed
    try:
        subprocess.check_output(["gh", "--version"])
    except FileNotFoundError:
        logger.critical(
            "Github CLI is not installed. Please install it from https://cli.github.com"
        )
        sys.exit(1)


def create_issue_meta(rows):
    # Add header
    header = ["Version", "Source", "Clause(s)"]
    rows.insert(0, header)

    # Create table
    table = ""
    for i, row in enumerate(rows):
        table += "|"
        table += "|".join(row)
        table += "|\n"
        if i == 0:
            table += "|"
            table += "|".join([":---:"] * len(row))
            table += "|\n"
    return table


def get_rows(table):
    # There should be 6 columns
    assert_log(len(table.columns) == 6, "Table should have exactly 6 columns")
    assert_log(len(table.rows) > 1, "Table should have at least one row")

    rows = []
    for i, row in enumerate(table.rows):
        if i == 0:
            continue
        cell_values = []
        for cell in row.cells:
            parsed_text = ""
            for paragraph in cell.paragraphs:
                if "spec" in paragraph.style.name:
                    parsed_text += f"<blockquote>\n{paragraph.text}\n</blockquote>\n\n"
                    continue

                if "code" in paragraph.style.name:
                    parsed_text += f"\n```\n{paragraph.text}\n```\n"
                    continue

                for run in paragraph.runs:
                    if "code" in run.style.name:
                        parsed_text += f"`{run.text}`"
                    else:
                        parsed_text += run.text
                parsed_text += "\n"
            cell_values.append(parsed_text.strip())
        if any(c != "" for c in cell_values):
            rows.append(cell_values)
    return rows


def process_comments_document():
    # Change logger format
    logger.remove()  # All configured handlers are removed
    fmt = "<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>"
    logger.add(sys.stderr, format=fmt)

    parser = ArgumentParser(description="Process comments document")
    parser.add_argument(
        "-i", help="Path to comments document", dest="comments_document", required=True
    )
    parser.add_argument("-l", "--limit", help="Limit number of issues", type=int)
    parser.add_argument(
        "-t",
        "--only-type",
        help="Only process type, either string or 'all'. Must be seperated by comma",
        type=str,
    )
    parser.add_argument(
        "-c",
        "--only-clause",
        help="Only process clause, either number or 'all'. Must be seperated by comma",
        type=str,
    )
    parser.add_argument("-n", "--dry_run", help="Dry run", action="store_true")

    # Check if access token is set
    check_if_github_cli_is_installed()
    auth_token = os.popen("gh auth token").read().strip()

    # Initialize Github
    auth = Auth.Token(auth_token)
    git = Github(auth=auth)

    args = parser.parse_args()
    document = Document(args.comments_document)

    # Get GitHub repository and version from header
    version = document.sections[0].header.tables[0].rows[1].cells[1].text
    github_repo = document.sections[0].header.tables[0].rows[0].cells[2].text
    github_repo = re.search(r"github\.com\/(.+)\s*", github_repo).group(1)
    repo = git.get_repo(github_repo)

    # Get existing issues
    all_issues = repo.get_issues(state="all")
    existing_ids = set()
    for issue in all_issues:
        if issue.body is None:
            continue
        issue_id = re.search(r"<!-- id: (.+) -->", issue.body)
        if issue_id:
            issue_id = issue_id.group(1)
            existing_ids.add(issue_id)

    # Process table
    assert_log(len(document.tables) == 1, "Document should have exactly one table")
    table = document.tables[0]
    rows = get_rows(table)

    logger.info(f"Found {len(rows)} comments")

    # Create issues
    issues_created = 0
    issues_skipped = 0
    for row in rows:
        # Process labels
        labels = []
        if row[0] != "":
            for label in row[0].split(","):
                s_label = label.strip()
                assert_log(s_label in LABELS, f"Invalid label: {s_label}")
                labels.append(LABELS[s_label])

        # Check if type is in only_type
        if args.only_type:
            if row[0] == "":
                match = "all" in args.only_type
            else:
                match = any(
                    t.strip().lower() in row[0].lower()
                    for t in args.only_type.split(",")
                )

            if not match:
                logger.info(
                    f"Skipping {row[3]} as it is not in type(s) [{args.only_type}]"
                )
                issues_skipped += 1
                continue

        # Process clauses and title
        clause = None
        if row[2] != "":
            clause = [f"§{c.strip()}" for c in row[2].split(",")]
            clause = ", ".join(clause)
            title = f"{clause}: {row[3]}"
        else:
            title = row[3]

        # Check if clause is in only_clause
        if args.only_clause:
            if not clause:
                match = "all" in args.only_clause
            else:
                match = any(
                    re.search(rf"(?<!\.){c.strip()}", clause)
                    for c in args.only_clause.split(",")
                )

            if not match:
                logger.info(
                    f"Skipping {row[3]} as it is not in clause(s) [{args.only_clause}]"
                )
                issues_skipped += 1
                continue

        # Get rest of the data
        source = row[1]
        comment = row[4]
        suggestion = row[5]

        if source == "":
            source = "Unknown"
            logger.warning(f"No source for: {title}, setting to 'Unknown'")

        raw_id = f"{title}{comment}{suggestion}"
        id_hash = hashlib.sha1(raw_id.encode("utf-8")).hexdigest()

        if id_hash in existing_ids:
            logger.info(f"Skipping existing issue: {title}")
            issues_skipped += 1
            continue

        body = f"<!-- id: {id_hash} -->\n"
        body += create_issue_meta([[version, source, clause or "all"]])
        body += "\n"

        if comment == "":
            logger.warning(f"No comment for: {title}, skipping...")
            issues_skipped += 1
            continue
        body += f"\n#### Comment:\n{comment}\n"

        if suggestion != "":
            body += f"\n-----\n#### Suggestion:\n{suggestion}\n"

        if args.limit and issues_created >= args.limit:
            logger.info(f"Reached limit of {args.limit} issues")
            break

        if args.dry_run:
            logger.info(f"Would create issue: {title}")
            logger.debug(f"\n{body}")
            issues_created += 1
        else:
            logger.success(f"Creating issue: {title}")
            repo.create_issue(title=title, body=body, labels=labels)
            issues_created += 1

    logger.success(f"created={issues_created} skipped={issues_skipped}")
