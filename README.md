# AOM Specification reivew process

This repository contains a proposal on how AOM can define a process for reviewing it's specifications before the specification receives the Working Group Approved (WGA) status.

Curretnly AOM specificaions follow the following standardization process:

- `PD`: Pre-Draft
- `WGD`: AOM Working Group Draft
- `WGA`: AOM Working Group Approved Draft
- `FD`: AOM Final Deliverable

When a sub-working group finilizes the specification, that specification is sent to the working group for review.
After a successful review the specification moves into the `WGA` status and can continue it path to become a Final Deliverable of AOM.

The AOM Working Group Approved Draft `WGA` is a very important stage where a major feedback from the experts of the entire working group is expected before labeling the specification as `WGA`. However, currently there seems to be no process which would allow the AOM to organize that feedback.

In this repository you can find a proposal for such process. It includes:

- a Word template ([AOM_comments_template.docx](./data/AOM_comments_template.docx)) which can be used to collect comments to a specification in a table-like format.
- a Python script which can be used to create issues based on that document in the related AOM repository. A detailed descirption on how to use this can be found in [HOWTO](HOWTO.md)

## Reivew process
We recommend that AOM intorduces the following review process:

- Sub-working group *finishes* the specification for the Working Group to review
- Anouncement is made on the reflector with the request to provide feedback. This request should include the initial version of the [AOM_comments_template.docx](./data/AOM_comments_template.docx) with a filled out header including:
  - Name of the specification
  - Version of the specification for review
  - (if applicable) the GitHub URL which can be used to track every entry in that table
- AOM WG members start adding their feedback and input from multiple groups is merged into a single document (single table)
  - at any time one can run the python scirpt to start addressing the issues. The script will not create duplicate issuses as long as the contents of the table row does not change. Running the script early would allow starting to address issues early in the process.
- After a set deadline when all comments are gathered the sub-working group need to address every single comment.
- When all comments are adressed the specification can be marked as `WGA`: AOM Working Group Approved Draft.
