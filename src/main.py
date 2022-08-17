import uvicorn
from fastapi import FastAPI, Depends, Form, Response
from database.operations import SetupDatabase, Read, Create
from database.models.logs import *
from database.models.user import *
import base64
from views.auth import *
from typing import List

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SetupDatabase.create_db_and_tables()

@app.get("/", response_model=CurrentUsers)
def current_user(cred: str = Depends(login)):
    return cred

@app.get("/logs/", response_model=List[LogsSchema])
def read_logs(_: str = Depends(login)):
    return Read.read_logs()

@app.get("/users/", response_model=List[CurrentUsers])
def read_users(_: str = Depends(login)):
    return Read.read_users()

@app.post("/logs/", response_model=LogsSchema)
def create_logs(data: LogsSchema, _: str = Depends(login)):
    return Create.create_logs(data=data)

@app.post("/users/", response_model=CreateUsers)
def create_user(data: CreateUsers, _: str = Depends(login)):
    data.password = Hashing.create_hash(data.password)
    return Create.create_user(data=data)

def run_server(host:str, port:int, debug:bool, reload:bool):
    uvicorn.run("main:app", host=host, port=port, debug=debug, reload=reload)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)