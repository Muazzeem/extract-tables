import mimetypes
from typing import List, Sequence
from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1 as documentai

PROJECT_ID = "saifuls-playground"
LOCATION = "us"
PROCESSOR_ID = "ef5aebbd0034f4e8"


def online_process(
        file_path: str,
) -> documentai.Document:
    """
    Processes a document using the Document AI Online Processing API.
    """

    # Instantiates a client
    docai_client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{LOCATION}-documentai.googleapis.com"
        )
    )

    # The full resource name of the processor, e.g.:
    # projects/project-id/locations/location/processor/processor-id
    # You must create new processors in the Cloud Console first
    resource_name = docai_client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)

    # Read the file into memory
    with open(file_path, "rb") as file:
        file_content = file.read()

    mime_type = mimetypes.guess_type(file_path)[0]
    raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    # Use the Document AI client to process the sample form
    result = docai_client.process_document(request=request)

    return result.document


def get_table_data(
        rows: Sequence[documentai.Document.Page.Table.TableRow], text: str
):
    """
    Get Text data from table rows
    """
    all_values: List[List[str]] = []
    for row in rows:
        current_row_values: List[str] = []
        for cell in row.cells:
            current_row_values.append(
                text_anchor_to_text(cell.layout.text_anchor, text)
            )
        all_values.append(current_row_values)
    return all_values


def text_anchor_to_text(text_anchor: documentai.Document.TextAnchor, text: str) -> str:
    """
    Document AI identifies table data by their offsets in the entirity of the
    document's text. This function converts offsets to a string.
    """
    response = ""
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    for segment in text_anchor.text_segments:
        start_index = int(segment.start_index)
        end_index = int(segment.end_index)
        response += text[start_index:end_index]
    return response.strip().replace("\n", " ")
