from sqlmodel import SQLModel, Field
from typing import Optional


class CurrentUsers(SQLModel):
    email :str
    password: str
    is_admin: bool

class UsersSchema(SQLModel):
    first_name: str
    last_name: str
    email :str
    password: str
    is_admin: Optional[bool] = False


class UsersSchemaRead(UsersSchema):
    id: int


class Users(UsersSchema, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)