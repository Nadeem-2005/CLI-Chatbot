from mcp.server.fastmcp import FastMCP
from pydantic import Field
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# TODO: Write a tool to read a doc
@mcp.tool(
    name="read_doc_contents",
    description="Reads the contents of a document and returns it as a string.",
)
def read_doc(doc_id:str = Field(..., description="The ID of the document to read.")):
    if doc_id not in docs:
        return f"Error: Document with ID '{doc_id}' not found."
    return docs[doc_id]

# TODO: Write a tool to edit a doc
@mcp.tool(
    name="edit_doc_contents",
    description="Edits the contents of a document and returns the updated content.",
)
def edit_doc(
    doc_id:str = Field(description="The ID of the document to edit."),
    old_content:str = Field(description="The current content of the document."),
    new_content:str = Field(description="The new content to write to the document."),
):
    if doc_id not in docs:
        return f"Error: Document with ID '{doc_id}' not found."
    docs[doc_id] = docs[doc_id].replace(old_content, new_content)
    return docs[doc_id]

# TODO: Write a resource to return all doc id's
@mcp.resource(
    uri="docs://documents",
    # name = "list_doc_ids",
    # description = "Returns a list of all document IDs available.",
    mime_type="application/json",
)

def list_docs() -> list[str] :
    return list(docs.keys())

# TODO: Write a resource to return the contents of a particular doc
@mcp.resource(
    uri = "docs://documents/{doc_id}",
    # name = "get_doc_contents",
    # description = "Returns the contents of a document given its ID.",
    mime_type="text/plain",
)

def fetch_doc(doc_id:str):
    if doc_id not in docs:
        return f"Error: Document with ID '{doc_id}' not found."
    return docs[doc_id]

# TODO: Write a prompt to rewrite a doc in markdown format
@mcp.prompt(
    name="format_doc_markdown",
    description="Summarizes the contents of a document in markdown format.",
)

def format_doc_prompt(
    doc_id:str = Field(description="The ID of the document to be formatted.")
) -> list[base.UserMessage]:
    prompt = f"""
Your goal is to reformat a document to be written with markdown syntax.

The id of the document you need to reformat is:
<document_id>
{doc_id}
</document_id>

Add in headers, bullet points, tables, etc as necessary. Feel free to add in structure.
Use the 'edit_document' tool to edit the document. After the document has been reformatted...
"""
    
    return [base.UserMessage(prompt)]
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
