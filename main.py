from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from auth.auth_module import AuthModule
from users.users_module import UsersModule
from tasks.tasks_module import TasksModule
from service.service_module import ServiceModule

app = FastAPI(
    title="Micro-serviço com JWT",
    description="API com autenticação JWT, gerenciamento de usuários e tarefas",
    version="1.0"
)

# Montar o diretório de arquivos estáticos
app.mount("/output", StaticFiles(directory="output"), name="output")

# Registrar os módulos
auth_module = AuthModule(app)
users_module = UsersModule(app)
tasks_module = TasksModule(app)
service_module = ServiceModule(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)