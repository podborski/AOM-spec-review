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
        print(
            "Github CLI is not installed. Please install it from https://cli.github.com"
        )
        sys.exit(1)


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
                if "code" in paragraph.style.name:
                    parsed_text += f"\n```\n{paragraph.text}\n```\n"
                    continue

                for run in paragraph.runs:
                    if "code" in run.style.name:
                        parsed_text += f"`{run.text}`"
                    else:
                        parsed_text += run.text
            cell_values.append(parsed_text)
        if any([c != "" for c in cell_values]):
            rows.append(cell_values)
    return rows


def process_comments_document():
    parser = ArgumentParser(description="Process comments document")
    parser.add_argument(
        "-i", help="Path to comments document", dest="comments_document", required=True
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
        issue_id = re.search(r"<!-- id: (.+) -->", issue.body)
        if issue_id:
            issue_id = issue_id.group(1)
            existing_ids.add(issue_id)

    # Process table
    assert_log(len(document.tables) == 1, "Document should have exactly one table")
    table = document.tables[0]
    rows = get_rows(table)

    print(f"Found {len(rows)} comments")

    # Create issues
    for row in rows:
        # Process labels
        labels = []
        if row[0].strip() != "":
            for label in row[0].split(","):
                s_label = label.strip()
                assert_log(s_label in LABELS, f"Invalid label: {s_label}")
                labels.append(f"{LABELS[s_label]} comment")

        # Process clauses and title
        if row[2].strip() != "":
            clause = [f"§{c.strip()}" for c in row[2].split(",")]
            clause = ", ".join(clause)
            title = f"{clause}: {row[3]}"
        else:
            title = row[3]

        comment = row[4]
        suggestion = row[5]

        raw_id = f"{title}{comment}{suggestion}"
        id_hash = hashlib.sha1(raw_id.encode("utf-8")).hexdigest()

        if id_hash in existing_ids:
            logger.info(f"Skipping existing issue: {title}")
            continue

        body = f"<!-- id: {id_hash} -->\n"
        body += f"_Comment for: {version}_\n"

        if comment == "":
            logger.warning(f"No comment for: {title}, skipping...")
            continue
        body += f"\n#### Comment:\n{comment}\n"

        if suggestion != "":
            body += f"\n-----\n#### Suggestion:\n{suggestion}\n"

        if args.dry_run:
            logger.info(f"Would create issue: {title}")
            logger.debug(f"\n{body}")
            continue

        logger.success(f"Creating issue: {title}")
        repo.create_issue(title=title, body=body, labels=labels)

    logger.success("Done")
