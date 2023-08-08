# AOM Specification review process

This repository contains a proposal on how the AOM can define a process for reviewing it's documents before the document receives a Working Group Approved (WGA) status.

Curretnly AOM documents follow the standardization process where every document is going thourogh the following [AOM deliverable stages](https://storage.googleapis.com/downloads.aomedia.org/assets/pdf/wg-charters/Alliance%20for%20Open%20Media%20Charter%20V.1.1.pdf):

- `PD` - Pre-Draft:  
  Any Working Group Participant may submit a proposed initial draft document as a candidate Draft Deliverable of that Working Group. The Working Group chair will designate each submission as a “Pre-Draft” document.
- `WGD` - AOM Working Group Draft:  
  Each Pre-Draft document of a Working Group must first be approved by a Supermajority Vote of the Working Group Participants of that Working Group in order to become a Draft Deliverable. Once the Working Group approves a document as a Draft Deliverable, the Draft Deliverable becomes the basis for all going forward work on that deliverable.
- `WGA` - AOM Working Group Approved Draft:  
  Once a Working Group believes it has achieved the objectives for its deliverable as described in the Scope, it will progress its Draft Deliverable to “Working Group Approved” status by a Supermajority Vote of the Participants of that Working Group.
- `FD` - AOM Final Deliverable:  
  Upon a Draft Deliverable reaching Working Group Approved status, the Executive Director or his/her designee will present that Working Group Approved Draft Deliverable to all Members for approval. Upon a Supermajority Vote of the Members, that Draft Deliverable will be designated a Final Deliverable `FD`.

The AOM Working Group Approved Draft `WGA` is a very important stage where major feedback from the experts of the entire Working Group is expected before labeling the document as `WGA`. However, currently there seems to be no process which would allow the AOM to organize that feedback.
Another important aspect is that different projects within a Working Group are worked on in Sub-Working Groups. While the Sub-Working Group is developing a document, other members of the Working Group may not be able to follow all the progress within that Sub-Working Group, so it is very important to have a clearly defined step where the Sub-Working-Group asks the whole Working Group for a review before a document can be given WGA status.

In this repository, you will find a suggested work process where a Sub-Working Group can ask for feedback from the Working Group to agree on the WGA status of the document before voting. It includes:

- a Word template ([AOM_comments_template.docx](./data/AOM_comments_template.docx)), which can be used to collect comments to a document in a table-like format. A detailed description on how to use that template can be found in [HOWTO_COMMENT.md](./HOWTO_COMMENT.md)
- a Python script, which can be used to create issues based on that document in the related AOM repository. A detailed description on how to use this can be found in [HOWTO_OPENISSUES.md](./HOWTO_OPENISSUES.md)

## Review process
We recommend that the AOM introduces the following review process:

1. The Sub-Working Group reaches the stage where it believes it has achieved the objectives for its deliverable as described in the scope
2. An announcement is made on the Working Group reflector with the request to provide feedback and seeking the `WGA` status (here AOM can even define a Subject template for such an anouncement. For example `Specification XYX is seeking WGA status. Request for comments.`). This request should include the initial version of the [AOM_comments_template.docx](./data/AOM_comments_template.docx) with a filled out header including:
    - The name of the document
    - The version of the document for review
    - (if applicable) the GitHub URL that can be used to track every entry in that table
3. AOM WG members start adding their feedback and send filled out word document back to the reflector.
    - inputs from multiple companies can be merged into a single document (single table)
    - at any time one can run the python script to start addressing the issues. The script will not create duplicate issues as long as the contents of the table's row does not change. Running the script early would allow starting to address issues early in the process.
4. After a set deadline (to be defined by the AOM), when all comments are gathered, the Sub-Working Group needs to address every single comment.
    - the resolution should capture if the comment is:
        - accepted: Will be implemented before reaching the `WGA` status
        - partially accepted: Only a portion will be implemented. The Working Group needs to explain why other parts are not accepted
        - delayed: Delayed for a future version with a reasoning why it is still ok to move forward for a publication in the current stage
        - rejected: The comment is not accepted with an explanation why.
5. After all comments have been addressed, the document is ready for a Working Group vote and can be designated a `WGA` if it receives a supermajority vote of the participants in that Working Group.
