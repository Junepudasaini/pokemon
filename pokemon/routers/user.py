from fastapi import APIRouter, Depends, status, HTTPException
from crud import CRUD
from database import session
from models import User
from schemas import UserModel
from hashing import Hash
import oauth2

router = APIRouter(
    tags=['User']
)

db = CRUD()

# Create User

@router.post('/user', status_code=status.HTTP_201_CREATED)
async def create_user(request: UserModel):
    new_user = User (
        name = request.name,
        email = request.email,
        password = Hash.bcrypt(request.password)
        )  
    user = await db.add_user(session, new_user)
    
    return {"user": user, "message": f"User with the name {user.name} created successfully."}