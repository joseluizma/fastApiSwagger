from fastapi import APIRouter, Depends, HTTPException
from auth.auth_service import AuthService
from service.service_service import ServiceService
from service.dtos import ServiceCreate, Service

router = APIRouter()

service_service = ServiceService()
auth_service = AuthService()

@router.post("", response_model=dict)
async def create_service(service: ServiceCreate, current_user: str = Depends(auth_service.get_current_user)):
    service_id = await service_service.create_service(service, current_user)
    return {"message": "Tarefa criada com sucesso", "service_id": service_id}

@router.get("", response_model=list[Service])
async def get_services(current_user: str = Depends(auth_service.get_current_user)):
    services = await service_service.get_user_service(current_user)
    return services

@router.get("/{service_id}", response_model=Service)
async def get_service(service_id: int, current_user: str = Depends(auth_service.get_current_user)):
    service = await service_service.get_service(service_id, current_user)
    if not service:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return service

@router.put("/{service_id}", response_model=dict)
async def update_service(service_id: int, service: ServiceCreate, current_user: str = Depends(auth_service.get_current_user)):
    try:
        await service_service.update_service(service_id, service, current_user)
        return {"message": "Tarefa atualizada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{service_id}", response_model=dict)
async def delete_service(service_id: int, current_user: str = Depends(auth_service.get_current_user)):
    try:
        await service_service.delete_service(service_id, current_user)
        return {"message": "Tarefa deletada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/oi/")
async def conexao_service(current_user: str = Depends(auth_service.get_current_user)):
    try:
        result = await service_service.conexao_service()
        
        if result["status"] == "error":
            raise ValueError(result["error"])
        
        # Construir a URL para download do arquivo
        file_url = f"/output/{result['file_name']}"
        return {"message": "Arquivo gerado com sucesso", "download_url": file_url}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))