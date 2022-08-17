import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from database.models.user import CurrentUsers

from database.operations import Read


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()

class Hashing:
    
    def verify_hash(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    def verify_user(username_request: str, username_database: str) -> bool:
        return secrets.compare_digest(username_request, username_database)
    
    def create_hash(password: str) -> str:
        return pwd_context.hash(password)

class Error:

    def unauthorized():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )


def login(credentials: HTTPBasicCredentials = Depends(security)):
    data = Read.read_users_login(email = credentials.username)
    if data is None:
        Error.unauthorized()
    correct_password = Hashing.verify_hash(credentials.password, data.password)
    correct_username = Hashing.verify_user(credentials.username, data.email)
    if not (correct_username and correct_password):
        Error.unauthorized()
    return data