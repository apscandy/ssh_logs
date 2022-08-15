from sqlmodel import create_engine
import pathlib


class Config:
    base = pathlib.Path(__file__).resolve().parent
    sqlite_url = f"sqlite:///{base}/ssh_logs.db"
    engine = create_engine(sqlite_url)
