from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, predict
from app.routes.predict import load_model

app = FastAPI(title='Student Score Predictor API', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000', 'https://*.vercel.app'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.on_event('startup')
async def startup_event():
    load_model()

app.include_router(auth.router, prefix='/auth', tags=['Authentication'])
app.include_router(predict.router, prefix='/api', tags=['Prediction'])

@app.get('/')
def root():
    return {'message': 'Student Score Predictor API is running'}
