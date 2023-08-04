import docx
import urllib3
import datetime


class RateLimitRetry(urllib3.util.retry.Retry):
    """
    This class overrides the urllib3 retry mechanism to comply with
    GitHub's API rate limiting constraints
    Source: https://github.com/PyGithub/PyGithub/issues/1989#issuecomment-1261656811
    """

    def get_retry_after(self, response):
        reset_time = datetime.datetime.fromtimestamp(
            int(response.headers["X-RateLimit-Reset"])
        )
        retry_after = (reset_time - datetime.datetime.now()).total_seconds() + 1
        retry_after = max(retry_after, 0)
        print(f"Rate limited, retry after: {retry_after} seconds")
        return retry_after


def add_hyperlink(paragraph, url, text):
    """
    A function that places a hyperlink within a paragraph object.

    :param paragraph: The paragraph we are adding the hyperlink to.
    :param url: A string containing the required url
    :param text: The text displayed for the url
    :return: The hyperlink object

    Source: https://github.com/python-openxml/python-docx/issues/74#issuecomment-261169410
    """

    # This gets access to the document.xml.rels file and gets a new relation id value
    part = paragraph.part
    r_id = part.relate_to(
        url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True
    )

    # Create the w:hyperlink tag and add needed values
    hyperlink = docx.oxml.shared.OxmlElement("w:hyperlink")
    hyperlink.set(
        docx.oxml.shared.qn("r:id"),
        r_id,
    )

    # Create a w:r element
    new_run = docx.oxml.shared.OxmlElement("w:r")

    # Create a new w:rPr element
    rPr = docx.oxml.shared.OxmlElement("w:rPr")

    # Add color
    c = docx.oxml.shared.OxmlElement("w:color")
    c.set(docx.oxml.shared.qn("w:val"), "0000FF")
    rPr.append(c)

    # Add font size
    sz = docx.oxml.shared.OxmlElement("w:sz")
    sz.set(docx.oxml.shared.qn("w:val"), "20")
    rPr.append(sz)

    # Add underline
    u = docx.oxml.shared.OxmlElement("w:u")
    u.set(docx.oxml.shared.qn("w:val"), "single")
    rPr.append(u)

    # Join all the xml elements together add add the required text to the w:r element
    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)

    paragraph._p.clear()
    paragraph._p.append(hyperlink)

    return hyperlink
