from .models import Logs, Users, Config
from sqlmodel import Session, SQLModel, select


class SetupDatabase:

     def create_db_and_tables():
        SQLModel.metadata.create_all(Config.engine)


class Create:
    
    def create(data: Logs | Users):
        with Session(Config.engine) as session:
            session.add(data)
            session.commit()
            session.refresh(data)


class Read:

    def read(data: Logs | Users):
        with Session(Config.engine) as session:
            statement = select(Users)
            results = session.exec(statement)
            return list(results)

    def read_existence(data: Logs | Users):
          with Session(Config.engine) as session:
            statement = select(Users)
            results = session.exec(statement)
            if data in results: return True
            else: return False       

    def read_by_email(data: Logs | Users):
        with Session(Config.engine) as session:
            statement = select(Users).where(Users.email == data.email)
            results = session.exec(statement)
            return list(results)


class Update:
    pass


class Delete:
    pass