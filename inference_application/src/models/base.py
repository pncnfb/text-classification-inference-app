from pydantic import BaseModel, Field
from typing import List

class Response(BaseModel):
    prediction: List[str] = Field(
        description="Predicted labels", examples=[["Gastroenterology", "Neurology"]]
    )