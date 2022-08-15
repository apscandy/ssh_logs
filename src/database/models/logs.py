from sqlmodel import SQLModel, Field
from typing import Optional


class LogsSchema(SQLModel):
    month: str
    day: str
    time: str
    server: str
    auth_type: str
    user: str
    ip_address: str
    port: str
    pub_key: Optional[str] = None


class LogsSchemaRead(LogsSchema):
    id: int


class Logs(LogsSchema, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)