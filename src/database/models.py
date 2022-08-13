from typing import Optional
from sqlmodel import Field, SQLModel, create_engine
import pathlib

class Config:
    base = pathlib.Path(__file__).resolve().parent
    sqlite_url = f"sqlite:///{base}/ssh_logs.db"
    engine = create_engine(sqlite_url)


class Logs(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    month: str
    day: str
    time: str
    server: str
    auth_type: str
    user: str
    ip_address: str
    port: str
    pub_key: Optional[str] = None


class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email :str
    password: str
    is_admin: Optional[bool] = False
