import uvicorn
from fastapi import FastAPI
from database.operations import SetupDatabase

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SetupDatabase.create_db_and_tables()

@app.get("/")
def root():
    a = "a"
    b = "b" + a
    return {"hello world": b}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)