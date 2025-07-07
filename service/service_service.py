import os
import subprocess
from .dtos import ServiceCreate
from pyspark.sql import SparkSession
from dotenv import load_dotenv
from io import StringIO
import sys
import time
import uuid
import sqlite3


# Configuração do caminho do projeto (se necessário)
sys.path.append('/home/repository/fastApiSwagger/service_package')


def find_jdbc_driver():
    try:
        result = subprocess.run(
            ["find", "/home/repository/fastApiSwagger", "-name", "postgresql-42.7.7.jar"],
            capture_output=True,
            text=True,
            check=True
        )
        paths = result.stdout.strip().split("\n")
        paths = [p for p in paths if p]
        return paths[0] if paths else None
    except subprocess.CalledProcessError:
        return None

class ServiceService:
    async def create_service(self, service: ServiceCreate, username: str):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        if not user:
            conn.close()
            raise ValueError("Usuário não encontrado")
        user_id = user[0]
        c.execute("INSERT INTO service (title, description, user_id) VALUES (?, ?, ?)", 
                 (service.title, service.description, user_id))
        service_id = c.lastrowid
        conn.commit()
        conn.close()
        return service_id

    async def get_user_service(self, username: str):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        if not user:
            conn.close()
            raise ValueError("Usuário não encontrado")
        user_id = user[0]
        c.execute("SELECT id, title, description, user_id FROM service WHERE user_id = ?", (user_id,))
        service = [{"id": row[0], "title": row[1], "description": row[2], "user_id": row[3]} 
                 for row in c.fetchall()]
        conn.close()
        return service

    async def get_service(self, service_id: int, username: str):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        if not user:
            conn.close()
            raise ValueError("Usuário não encontrado")
        user_id = user[0]
        c.execute("SELECT id, title, description, user_id FROM service WHERE id = ? AND user_id = ?", 
                 (service_id, user_id))
        service = c.fetchone()
        conn.close()
        if service:
            return {"id": service[0], "title": service[1], "description": service[2], "user_id": service[3]}
        return None

    async def update_service(self, service_id: int, service: ServiceCreate, username: str):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        if not user:
            conn.close()
            raise ValueError("Usuário não encontrado")
        user_id = user[0]
        c.execute("UPDATE service SET title = ?, description = ? WHERE id = ? AND user_id = ?", 
                 (service.title, service.description, service_id, user_id))
        if c.rowcount == 0:
            conn.close()
            raise ValueError("Tarefa não encontrada ou não pertence ao usuário")
        conn.commit()
        conn.close()

    async def delete_service(self, service_id: int, username: str):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        if not user:
            conn.close()
            raise ValueError("Usuário não encontrado")
        user_id = user[0]
        c.execute("DELETE FROM service WHERE id = ? AND user_id = ?", (service_id, user_id))
        if c.rowcount == 0:
            conn.close()
            raise ValueError("Tarefa não encontrada ou não pertence ao usuário")
        conn.commit()
        conn.close()

    async def conexao_service(self):
        # Diretório de saída para o arquivo .txt
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)  # Criar diretório se não existir

        # Gerar um nome único para o arquivo
        file_name = f"t101_data_{uuid.uuid4().hex}.txt"
        file_path = os.path.join(output_dir, file_name)

     # Tentar localizar o driver JDBC
        jdbc_driver_path = find_jdbc_driver()
        if not jdbc_driver_path or not os.path.exists(jdbc_driver_path):
            raise FileNotFoundError(f"Driver JDBC não encontrado. Tentou procurar em: /home/repository/fastApiSwagger")

        # Configurar a sessão Spark
        spark = SparkSession.builder \
            .appName("PostgreSQL") \
            .config("spark.jars", jdbc_driver_path) \
            .config("spark.driver.extraClassPath", jdbc_driver_path) \
            .config("spark.executor.extraClassPath", jdbc_driver_path) \
            .getOrCreate()

        # Obter parâmetros de conexão do arquivo .env
        db_host = 
        db_port = 
        db_name = 
        db_user = 
        db_password = 

        # Validar se todas as variáveis foram carregadas
        if not all([db_host, db_port, db_name, db_user, db_password]):
            raise ValueError("Uma ou mais variáveis de ambiente não foram definidas no arquivo .env")

        # Construir a URL JDBC
        url = f"jdbc:postgresql://{db_host}:{db_port}/{db_name}"

        # Definir as propriedades de conexão
        properties = {
            "user": db_user,
            "password": db_password,
            "driver": "org.postgresql.Driver"
        }

        try:
            # Teste a conexão com uma query simples
            df_test = spark.read.jdbc(url=url, table="(SELECT 1) AS test", properties=properties)
            print("Conexão com o banco de dados bem-sucedida!")
            
            # Carregue os dados da tabela
            df = spark.read.jdbc(url=url, table="usu_0.t101", properties=properties)
            
            # Capturar o schema como string
            old_stdout = sys.stdout
            sys.stdout = schema_output = StringIO()
            df.printSchema()
            schema_text = schema_output.getvalue()
            sys.stdout = old_stdout

            # Capturar os dados como string
            sys.stdout = data_output = StringIO()
            df.show(truncate=False)
            data_text = data_output.getvalue()
            sys.stdout = old_stdout

            # Combinar schema e dados
            result_text = f"Schema da tabela usu_0.t101:\n{schema_text}\nDados da tabela usu_0.t101:\n{data_text}"
            
            # Salvar no arquivo .txt
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(result_text)
            
            return {"file_path": file_path, "file_name": file_name, "status": "success"}

        except Exception as e:
            return {"file_path": None, "file_name": None, "status": "error", "error": f"Erro ao conectar ou ler a tabela: {str(e)}"}

        finally:
            # Feche a sessão Spark
            spark.stop()
            


 