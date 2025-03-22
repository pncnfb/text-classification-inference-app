from mistralai import Mistral
from fastapi import UploadFile
from typing import List

class MistralClient:
    def __init__(self, api_key: str):
        """
        Initializes the Mistral client with the given API key.
        """
        self.api_key = api_key
        self.client = Mistral(api_key=self.api_key)

    # DEPRECATED: GREEDY FUNCTION THAT SPLITS IN PAGES AND NOT IN SEMANTIC NOTES
    # async def extract_pages_from_pdfs(self, files: List[UploadFile]) -> List[str]:
    #     """
    #     This function processes a list of uploaded PDF files, extracts text using OCR,
    #     and returns the extracted text from each PDF.

    #     Args:
    #         files: List of uploaded PDF files.

    #     Returns:
    #         List of extracted text strings from each document.
    #     """
    #     extracted_texts = []

    #     for file in files:
    #         uploaded_pdf = self.client.files.upload(
    #             file={"file_name": file.filename, "content": await file.read()},
    #             purpose="ocr"
    #         )

    #         signed_url = self.client.files.get_signed_url(file_id=uploaded_pdf.id)

    #         ocr_response = self.client.ocr.process(
    #             model="mistral-ocr-latest",
    #             document={"type": "document_url", "document_url": signed_url.url}
    #         )

    #         if hasattr(ocr_response, "pages"):
    #             extracted_texts.extend([page.markdown for page in ocr_response.pages if page.markdown])

    #     return extracted_texts



    async def extract_text_from_pdf(self, file: UploadFile) -> str:
        """
        Processes a single uploaded PDF file, extracts and concatenates text using OCR,
        and returns the full extracted text.

        Args:
            file: An uploaded PDF file.

        Returns:
            A single string containing the concatenated text from the PDF.
        """
        uploaded_pdf = self.client.files.upload(
            file={"file_name": file.filename, "content": await file.read()},
            purpose="ocr"
        )

        signed_url = self.client.files.get_signed_url(file_id=uploaded_pdf.id)

        ocr_response = self.client.ocr.process(
            model="mistral-ocr-latest",
            document={"type": "document_url", "document_url": signed_url.url}
        )

        if hasattr(ocr_response, "pages"):
            full_text = " ".join(
                page.markdown for page in ocr_response.pages if page.markdown
            )
            return full_text

        return ""
