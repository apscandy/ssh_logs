from libraries import *

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

class CRUD:

    def create_db_and_tables():
        SQLModel.metadata.create_all(Config.engine)
    
    def save(data: Logs | Users):
        with Session(Config.engine) as session:
            session.add(data)
            session.commit()
            session.refresh(data)
    
    def check_existence(data: Logs | Users):
          with Session(Config.engine) as session:
            statement = select(Users)
            results = session.exec(statement)
            if data in results: return True
            else: return False       

    def find(data: Logs | Users):
        with Session(Config.engine) as session:
            statement = select(Users)
            results = session.exec(statement)
            return list(results)
    
    def find_by_email(data: Logs | Users):
        with Session(Config.engine) as session:
            statement = select(Users).where(Users.email == data.email)
            results = session.exec(statement)
            return list(results)

    

if __name__ == "__main__":
    CRUD.create_db_and_tables()