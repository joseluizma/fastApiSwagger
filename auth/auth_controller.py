from fastapi import APIRouter, HTTPException
from .auth_service import AuthService
from .dtos import User, Token

router = APIRouter()

auth_service = AuthService()

@router.post("/register", response_model=dict)
async def register(user: User):
    try:
        await auth_service.register_user(user)
        return {"message": "Usuário registrado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
async def login(user: User):
    token = await auth_service.login_user(user)
    if not token:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return token