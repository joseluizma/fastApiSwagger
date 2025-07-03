from fastapi import APIRouter, Depends, HTTPException
from auth.auth_service import AuthService
from users.users_service import UsersService
from users.dtos import UserUpdate

router = APIRouter()

users_service = UsersService()
auth_service = AuthService()

@router.get("/me", response_model=dict)
async def get_current_user_info(current_user: str = Depends(auth_service.get_current_user)):
    user = await users_service.get_user_by_username(current_user)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"username": user["username"], "id": user["id"]}

@router.put("/me", response_model=dict)
async def update_user(user_update: UserUpdate, current_user: str = Depends(auth_service.get_current_user)):
    try:
        updated_user = await users_service.update_user(current_user, user_update)
        return {"message": "Usuário atualizado com sucesso", "username": updated_user["username"]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/me", response_model=dict)
async def delete_user(current_user: str = Depends(auth_service.get_current_user)):
    await users_service.delete_user(current_user)
    return {"message": "Usuário deletado com sucesso"}