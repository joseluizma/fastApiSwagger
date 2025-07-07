import os
import subprocess
from pyspark.sql import SparkSession
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

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

class PostgresConnection:
    def __init__(self):
        # Tentar localizar o driver JDBC
        self.jdbc_driver_path = find_jdbc_driver()
        if not self.jdbc_driver_path or not os.path.exists(self.jdbc_driver_path):
            raise FileNotFoundError(f"Driver JDBC não encontrado. Tentou procurar em: /home/repository/fastApiSwagger")

        # Configurar a sessão Spark
        self.spark = SparkSession.builder \
            .appName("PostgreSQL") \
            .config("spark.jars", self.jdbc_driver_path) \
            .config("spark.driver.extraClassPath", self.jdbc_driver_path) \
            .config("spark.executor.extraClassPath", self.jdbc_driver_path) \
            .getOrCreate()

        # Obter parâmetros de conexão do arquivo .env
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT")
        self.db_name = os.getenv("DB_NAME")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")

        # Validar se todas as variáveis foram carregadas
        if not all([self.db_host, self.db_port, self.db_name, self.db_user, self.db_password]):
            raise ValueError("Uma ou mais variáveis de ambiente não foram definidas no arquivo .env")

        # Construir a URL JDBC
        self.url = f"jdbc:postgresql://{self.db_host}:{self.db_port}/{self.db_name}"

        # Definir as propriedades de conexão
        self.properties = {
            "user": self.db_user,
            "password": self.db_password,
            "driver": "org.postgresql.Driver"
        }

    def read_table(self, table_name: str):
        try:
            # Teste a conexão com uma query simples
            df_test = self.spark.read.jdbc(url=self.url, table="(SELECT 1) AS test", properties=self.properties)
            print("Conexão com o banco de dados bem-sucedida!")
            
            # Carregar os dados da tabela especificada
            df = self.spark.read.jdbc(url=self.url, table=table_name, properties=self.properties)
            return df
        except Exception as e:
            raise Exception(f"Erro ao conectar ou ler a tabela {table_name}: {str(e)}")

    def close(self):
        # Fechar a sessão Spark
        self.spark.stop()