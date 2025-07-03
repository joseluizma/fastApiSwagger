import sqlite3
from passlib.context import CryptContext
from config import Config
from .dtos import UserUpdate

class UsersService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_user_by_username(self, username: str):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT id, username FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()
        if user:
            return {"id": user[0], "username": user[1]}
        return None

    async def update_user(self, username: str, user_update: UserUpdate):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        updates = []
        params = []
        if user_update.username:
            updates.append("username = ?")
            params.append(user_update.username)
        if user_update.password:
            updates.append("password = ?")
            params.append(self.pwd_context.hash(user_update.password))
        
        if not updates:
            conn.close()
            raise ValueError("Nenhum dado para atualizar")
        
        params.append(username)
        query = f"UPDATE users SET {', '.join(updates)} WHERE username = ?"
        try:
            c.execute(query, params)
            if c.rowcount == 0:
                conn.close()
                raise ValueError("Usuário não encontrado")
            conn.commit()
            c.execute("SELECT id, username FROM users WHERE username = ?", 
                     (user_update.username if user_update.username else username,))
            updated_user = c.fetchone()
            conn.close()
            return {"id": updated_user[0], "username": updated_user[1]}
        except sqlite3.IntegrityError:
            conn.close()
            raise ValueError("Novo username já existe")

    async def delete_user(self, username: str):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE username = ?", (username,))
        if c.rowcount == 0:
            conn.close()
            raise ValueError("Usuário não encontrado")
        conn.commit()
        conn.close()