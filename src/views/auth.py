# import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()


def verify_hash(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_hash(password):
    return pwd_context.hash(password)


def login(credentials: HTTPBasicCredentials = Depends(security)):
    # correct_username = secrets.compare_digest(credentials.username, "admin")
    # correct_password = secrets.compare_digest(credentials.password, "password")
    correct_password = verify_hash(credentials.password, "$2b$12$/MT6kUHKNAeRYXvN25hLSOHPgzmBcjKGxhomOp.l9QTSOkP8Ct7Vq")
    correct_username = verify_hash(credentials.username, "$2b$12$0H8AJc9OMpr58RXa9SYV5egTmmDEQiAtkUBhPNJhKNVyNeAn3HLki")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username



