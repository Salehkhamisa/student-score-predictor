from pydantic import BaseModel
from typing import Optional

class StudentInput(BaseModel):
    gender: str
    race_ethnicity: str
    parental_level_of_education: str
    lunch: str
    test_preparation_course: str
    reading_score: float
    writing_score: float

class PredictionResult(BaseModel):
    predicted_math_score: float
    input_data: dict

class MetricsResponse(BaseModel):
    r2_score: float
    mae: float
    rmse: float
    model_name: str
