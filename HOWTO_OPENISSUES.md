# Additional information

In this readme we provide additional information on how to write the entries in the word document and how to run the pythnon script to open GitHub issues based on that document.

## How to write comments

Here are best practices on how to write the word document.

### Styles
The provided template has 3 styles which you can use when preparing your feedback.

- `Normal`: Your comment
- `code`: Syntax elements
- `spec`: Use this style to quote parts of the spec.

Make sure you don't copy other styles into the document. Use only the 3 styles listed above whenever possible.

### Comment types
We define several comment types:

- `ed`: Editorial which will be linked to `editorial` label wehen opening issues on GitHub
- `te`: Technical which will be linked to `technical` label wehen opening issues on GitHub
- `ge`: General which will be linked to `general` label wehen opening issues on GitHub
- `?`: Question which will be linked to `question` label wehen opening issues on GitHub
- `!`: AOM internal discussion only, when putting this into the comment type no issue will be opened.

You can combine multiple types by separating them with a comma like this: `ed, ?`.

## How to use the scirpt to open issues

In your system you need to have [Python](https://www.python.org) installed. This project uses poetry to create a virtual environment and install dependencies. It won't interfere with your system Python installation. To setup poetry follow the instructions [here](https://python-poetry.org/docs/#installation). Then in the root directory of this repository run:

```bash
poetry install
```

When you finalize your comments document, the automation script can be used to open issues in the repository. The script will not open duplicate issues. (a unique hash is stored as metadata in every issue to avoid that). You can re-distribute the consolidated comment document and re-run the script anytime.

```bash
usage: process-comments-document [-h] -i COMMENTS_DOCUMENT [-l LIMIT] [-t TYPE_FILTER] [-c CLAUSE_FILTER] [-n]

Process comments document

options:
  -h, --help            show this help message and exit
  -i COMMENTS_DOCUMENT  Path to comments document
  -l LIMIT, --limit LIMIT
                        Limit number of issues
  -t TYPE_FILTER, --type-filter TYPE_FILTER
                        Only process type, either string or 'all'. Must be separated by a comma
  -c CLAUSE_FILTER, --clause-filter CLAUSE_FILTER
                        Only process clause, either number or 'all'. Must be separated by a comma
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
