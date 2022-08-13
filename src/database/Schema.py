from libraries import *


class Logs(BaseModel):
    month: str
    day: str
    time: str
    server: str
    auth_type: str
    user: str
    ip_address: str
    port: str
    pub_key: str


class Users(BaseModel):
    first_name: str
    last_name: str
    email :str
    password: str
    is_admin: bool

