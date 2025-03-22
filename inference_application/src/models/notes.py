from pydantic import BaseModel, Field
from typing import List

class ClinicalNote(BaseModel):
    text: str = Field(..., description="The entire text of the segmented note")
    domain: str = Field(..., description="The domanin (Radiology, Urology, Gastroenterology, Orthopedic, Neurology)")

class Notes(BaseModel):
    notes: List[ClinicalNote]