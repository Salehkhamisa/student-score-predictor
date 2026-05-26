from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.models.student import StudentInput, PredictionResult, MetricsResponse
from app.core.security import decode_token
from app.core.database import predictions_collection, metrics_collection
import pickle
import numpy as np
import os
from datetime import datetime

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')

def get_current_user(token: str = Depends(oauth2_scheme)):
    username = decode_token(token)
    if not username:
        raise HTTPException(status_code=401, detail='Invalid or expired token')
    return username

model = None
encoders = None

def load_model():
    global model, encoders
    try:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        with open(os.path.join(BASE_DIR, 'ml', 'model.pkl'), 'rb') as f:
            model = pickle.load(f)
        with open(os.path.join(BASE_DIR, 'ml', 'encoders.pkl'), 'rb') as f:
            encoders = pickle.load(f)
        print('Model loaded successfully')
    except Exception as e:
        print(f'Model load error: {e}')

def safe_encode(encoder, value):
    value = value.strip()
    if value not in encoder.classes_:
        raise HTTPException(status_code=422, detail=f'Invalid value: {value}. Valid options: {list(encoder.classes_)}')
    return encoder.transform([value])[0]

@router.post('/predict', response_model=PredictionResult)
def predict(data: StudentInput, username: str = Depends(get_current_user)):
    if model is None:
        raise HTTPException(status_code=500, detail='Model not loaded')
    try:
        gender_enc = safe_encode(encoders['gender'], data.gender)
        race_enc = safe_encode(encoders['race_ethnicity'], data.race_ethnicity)
        parent_enc = safe_encode(encoders['parental_level_of_education'], data.parental_level_of_education)
        lunch_enc = safe_encode(encoders['lunch'], data.lunch)
        prep_enc = safe_encode(encoders['test_preparation_course'], data.test_preparation_course)
        features = np.array([[gender_enc, race_enc, parent_enc, lunch_enc, prep_enc,
                               data.reading_score, data.writing_score]])
        prediction = model.predict(features)[0]
        result = round(float(prediction), 2)
        predictions_collection.insert_one({
            'username': username,
            'input': data.dict(),
            'predicted_math_score': result,
            'timestamp': datetime.utcnow()
        })
        return {'predicted_math_score': result, 'input_data': data.dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/metrics', response_model=MetricsResponse)
def get_metrics(username: str = Depends(get_current_user)):
    metrics = metrics_collection.find_one({}, sort=[('_id', -1)])
    if not metrics:
        raise HTTPException(status_code=404, detail='No metrics found')
    return {
        'r2_score': metrics['r2_score'],
        'mae': metrics['mae'],
        'rmse': metrics['rmse'],
        'model_name': metrics['model_name']
    }