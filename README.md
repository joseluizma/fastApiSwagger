# fastApiSwagger
Projeto python api com autenticação JWT / Swagger

python3 -m venv venv

source venv/bin/activate

pip3 install fastapi uvicorn python-jose\[cryptography\] passlib\[bcrypt\]



mkdir -p /home/repository/fastApiSwagger/{auth,users,tasks}
touch /home/repository/fastApiSwagger/__init__.py
touch /home/repository/fastApiSwagger/auth/__init__.py
touch /home/repository/fastApiSwagger/users/__init__.py
touch /home/repository/fastApiSwagger/tasks/__init__.py

