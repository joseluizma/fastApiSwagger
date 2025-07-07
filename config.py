import sqlite3

class Config:
    SECRET_KEY = "sua-chave-secreta-aqui"  # Substitua por uma chave segura
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    @staticmethod
    def init_db():
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      username TEXT UNIQUE NOT NULL, 
                      password TEXT NOT NULL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS tasks 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      title TEXT NOT NULL, 
                      description TEXT, 
                      user_id INTEGER NOT NULL, 
                      FOREIGN KEY (user_id) REFERENCES users(id))''')
        conn.commit()
        conn.close()