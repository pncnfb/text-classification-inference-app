import asyncio

from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException

from src.utils import sanitize_string
from src.models import Response
from src.globals import ocr_client, domain_predictor, notes_agent

router = APIRouter(prefix="/classifier", tags=["classifier"])

@router.post("/docu_predict/", response_model=List[Response])
async def predict(files: List[UploadFile] = File(...)):
    """
    This endpoint processes one or more PDF files, extracts text using OCR, and classifies the content into clinical domains.

    Args:
        files: List of uploaded PDF files.

    Returns:
        List[Response]: An array of objects containing the predictions for each document.

    Example:
        Request:
            POST /docu_predict/
            [PDF files]

        Response:
            [
                {"prediction": ["Gastroenterology", "Neurology"]},
                {"prediction": ["Radiology"]}
            ]
    """
    try:
        extracted_texts = await asyncio.gather(
            *(ocr_client.extract_text_from_pdf(file) for file in files)
        )

        extracted_notes = [
            notes_agent.segment_and_classify_notes(sanitize_string(docu))
            for docu in extracted_texts
        ]

        predictions = []
        for docu_notes in extracted_notes:
            docu_predictions = []
            for note in docu_notes:
                prediction = domain_predictor.predict(note.text)
                docu_predictions.append(prediction)
            predictions.append(set(docu_predictions))

        response = [Response(prediction=list(preds)) for preds in predictions]
        print(response) # just for cmd line visualization

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
