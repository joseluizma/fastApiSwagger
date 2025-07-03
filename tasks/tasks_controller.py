from fastapi import APIRouter, Depends, HTTPException
from auth.auth_service import AuthService
from tasks.tasks_service import TasksService
from tasks.dtos import TaskCreate, Task

router = APIRouter()

tasks_service = TasksService()
auth_service = AuthService()

@router.post("", response_model=dict)
async def create_task(task: TaskCreate, current_user: str = Depends(auth_service.get_current_user)):
    task_id = await tasks_service.create_task(task, current_user)
    return {"message": "Tarefa criada com sucesso", "task_id": task_id}

@router.get("", response_model=list[Task])
async def get_tasks(current_user: str = Depends(auth_service.get_current_user)):
    tasks = await tasks_service.get_user_tasks(current_user)
    return tasks

@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int, current_user: str = Depends(auth_service.get_current_user)):
    task = await tasks_service.get_task(task_id, current_user)
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return task

@router.put("/{task_id}", response_model=dict)
async def update_task(task_id: int, task: TaskCreate, current_user: str = Depends(auth_service.get_current_user)):
    try:
        await tasks_service.update_task(task_id, task, current_user)
        return {"message": "Tarefa atualizada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{task_id}", response_model=dict)
async def delete_task(task_id: int, current_user: str = Depends(auth_service.get_current_user)):
    try:
        await tasks_service.delete_task(task_id, current_user)
        return {"message": "Tarefa deletada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))