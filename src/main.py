import uvicorn
from fastapi import FastAPI
from database.operations import SetupDatabase, Read, Create
from database.models.logs import *
from database.models.user import *
from typing import List

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SetupDatabase.create_db_and_tables()

@app.get("/logs/", response_model=List[LogsSchema])
def read_logs():
    return Read.read_logs()

@app.get("/users/", response_model=List[UsersSchema])
def read_users():
    return Read.read_users()

@app.post("/logs/", response_model=LogsSchema)
def create_logs(data: LogsSchema):
    return Create.create_logs(data=data)

@app.post("/users/", response_model=UsersSchema)
def create_user(data: UsersSchema):
    return Create.create_user(data=data)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)