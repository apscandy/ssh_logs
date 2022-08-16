from .models.logs import *
from .models.user import *
from .settings import Config
from sqlmodel import Session, SQLModel, select

class SetupDatabase:

     def create_db_and_tables():
        SQLModel.metadata.create_all(Config.engine)


class Create:
    
    def create_logs(data: LogsSchema):
        with Session(Config.engine) as session:
            data = Logs.from_orm(data)
            session.add(data)
            session.commit()
            session.refresh(data)
            return data

    def create_user(data: UsersSchema):
        with Session(Config.engine) as session:
            data = Users.from_orm(data)
            session.add(data)
            session.commit()
            session.refresh(data)
            return data


class Read:

    def read_users():
        with Session(Config.engine) as session:
            statement = select(Users)
            results = session.exec(statement).all()
            return results

    def read_logs():
        with Session(Config.engine) as session:
            statement = select(Logs)
            results = session.exec(statement).all()
            return results


class Update:
    pass


class Delete:
    pass