from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.user import UserRegister, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token
from app.core.database import users_collection

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')

@router.post('/register')
def register(user: UserRegister):
    existing = users_collection.find_one({'username': user.username})
    if existing:
        raise HTTPException(status_code=400, detail='Username already exists')
    hashed = hash_password(user.password)
    users_collection.insert_one({
        'username': user.username,
        'email': user.email,
        'hashed_password': hashed
    })
    return {'message': 'User registered successfully'}

@router.post('/token', response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({'username': form_data.username})
    if not user or not verify_password(form_data.password, user['hashed_password']):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = create_access_token({'sub': user['username']})
    return {'access_token': token, 'token_type': 'bearer'}
