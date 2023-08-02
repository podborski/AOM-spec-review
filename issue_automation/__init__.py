import os
import re
import sys
import subprocess
from docx import Document
from github import Github, Auth
from argparse import ArgumentParser

LABELS = {
    "ed": "editorial",
    "ge": "general",
    "te": "technical",
}


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
    assert len(table.columns) == 6, "Table should have exactly 6 columns"
    assert len(table.rows) > 1, "Table should have at least one row"

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
        rows.append(cell_values)
    return rows


def process_comments_document():
    parser = ArgumentParser(description="Process comments document")
    parser.add_argument("-i", "--comments_document", help="Path to comments document")
    parser.add_argument("-n", "--dry_run", help="Dry run", action="store_true")

    # Check if access token is set
    check_if_github_cli_is_installed()
    auth_token = os.popen("gh auth token").read().strip()

    # Initialize Github
    auth = Auth.Token(auth_token)
    g = Github(auth=auth)

    args = parser.parse_args()
    document = Document(args.comments_document)

    # Get header
    header = document.sections[0].header.paragraphs[0].text
    github_repo = re.search(r"github\.com\/(.+)\s*", header).group(1)
    print(f"GitHub repo: {github_repo}")

    # Process table
    assert len(document.tables) == 1, "Document should have exactly one table"
    table = document.tables[0]
    rows = get_rows(table)

    print(f"Found {len(rows)} comments")

    # Create issues
    for row in rows:
        # TODO: assert label exists

        label = LABELS[row[0]] + " comment"
        clause = row[2]
        title = row[3]
        comment = row[4]
        suggestion = row[5]

        # TODO: WIP create issue
