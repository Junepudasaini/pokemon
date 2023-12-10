from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from crud import CRUD
from database import session

router  = APIRouter(
    tags=['Authentication']
)

db = CRUD()

# Login Authentication

@router.post('/login')
async def login(request:OAuth2PasswordRequestForm = Depends()):
    user = await db.user_login(session, request)
    return user