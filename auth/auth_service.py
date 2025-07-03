from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
import sqlite3
from config import Config
from auth.dtos import User, Token

security = HTTPBearer()

class AuthService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        Config.init_db()

    async def register_user(self, user: User):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        hashed_password = self.pwd_context.hash(user.password)
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                     (user.username, hashed_password))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            raise ValueError("Username já existe")
        finally:
            conn.close()

    async def login_user(self, user: User):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (user.username,))
        db_user = c.fetchone()
        conn.close()

        if db_user and self.pwd_context.verify(user.password, db_user[2]):
            access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = self.create_access_token(
                data={"sub": user.username}, expires_delta=access_token_expires
            )
            return {"access_token": access_token, "token_type": "bearer"}
        return None

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
        return encoded_jwt

    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)):
        try:
            payload = jwt.decode(credentials.credentials, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Invalid authentication credentials")
            return username
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")