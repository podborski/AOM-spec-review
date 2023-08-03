# How to use Issue Automation Scripts

In your system you need to have [Python](https://www.python.org) installed. This project uses poetry to create a virtual environment and install dependencies. It won't interfere with your system Python installation. To setup poetry follow the instructions [here](https://python-poetry.org/docs/#installation). Then in the root directory of this repository run:

```bash
poetry install
```

## How to write comments

The provided template has 3 styles which you can use when preparing your feedback.

- `Normal`: Your comment
- `code`: Syntax elements
- `spec`: Use this style to quote parts of the spec.

Make sure you don't copy other styles into the document. Use only the 3 styles listed above whenever possible.

## How to use script to open issues

When you finalize your comments document, the automation script can be used to open issues in the repository. The script will not open duplicate issues. (a unique hash is stored as metadata in every issue to avoid that). You can re-distribute the consolidated comment document and re-run the script anytime.

```bash
usage: process-comments-document [-h] -i COMMENTS_DOCUMENT [-l LIMIT] [-t ONLY_TYPE] [-c ONLY_CLAUSE] [-n]

Process comments document

options:
  -h, --help            show this help message and exit
  -i COMMENTS_DOCUMENT  Path to comments document
  -l LIMIT, --limit LIMIT
                        Limit number of issues
  -t ONLY_TYPE, --only-type ONLY_TYPE
                        Only process type, either string or 'all'. Must be separated  by comma
  -c ONLY_CLAUSE, --only-clause ONLY_CLAUSE
                        Only process clause, either number or 'all'. Must be separated  by comma
  -n, --dry_run         Dry run
```

### Examples

These examples provide different scenarios of how to use the script. If you only specify input file (`-i`) and nothing else it will open issues for all comments in the document.

<details>
  <summary>Open issues for only <code>technical</code> comments</summary>

  ```bash
  poetry run process-comments-document -- -i AOM_comments_iamf.docx -t te
  ```
</details>

<details>
  <summary>Open issues for only <code>technical</code> and <code>editorial</code> comments</summary>

  ```bash
  poetry run process-comments-document -- -i AOM_comments_iamf.docx -t te,ed
  ```
</details>

<details>
  <summary>Open issues for only clause <code>2</code> and its sub-clauses</summary>

  ```bash
  poetry run process-comments-document -- -i AOM_comments_iamf.docx -c 2
  ```
</details>

<details>
  <summary>Open issues for comments that don't specify a clause</summary>

  ```bash
  poetry run process-comments-document -- -i AOM_comments_iamf.docx -c all
  ```
</details>

<details>
  <summary>Open only 10 issues</summary>

  ```bash
  poetry run process-comments-document -- -i AOM_comments_iamf.docx -l 10
  ```
</details>

<details>
  <summary>Do a dry run to see how the issues would be opened</summary>

  ```bash
  poetry run process-comments-document -- -i AOM_comments_iamf.docx -n
  ```
</details>
