import typer
from rich.console import Console
from rich.table import Table
from main import run_server
from views.auth import Hashing
from database.operations import Read, Create, Delete
from database.models.user import *
import json
from enum import Enum


class NeuralNetwork(Enum):
    simple = "simple"
    conv = "conv"
    lstm = "lstm"





console = Console()
app = typer.Typer(add_completion=False)
database = typer.Typer()
security = typer.Typer()
api = typer.Typer()
app.add_typer(database, name="db")
app.add_typer(security, name="sec")
app.add_typer(api, name="api")


def iterate_user():
    data  = Read.read_users()
    for user in data:
        user = UsersSchemaRead(**user.dict())
        yield user.dict()

@database.command()
def load_users():
    total = 0
    test = []
    with typer.progressbar(iterate_user(), length=10) as progress:
        for value in progress:
            test.append(ListingDB(**value).dict())
    console.print(f"Processed {total} user IDs.")
    typer.confirm("Would you print the users", abort=True)
    console.print(test)

@database.command()
def make_user(
    first_name:str = typer.Option(..., prompt=True),
    last_name:str = typer.Option(..., prompt=True),
    password: str = typer.Option(..., prompt=True, confirmation_prompt=True, hide_input=True),
    email: str = typer.Option(..., prompt=True, confirmation_prompt=True)
    ):
    password = Hashing.create_hash(password)
    user = UsersSchema(first_name=first_name, last_name=last_name, password=password, email=email)
    Create.create_user(user)
    console.print(json.dumps(user.dict(), indent=2))

@database.command()
def get_users():
    data  = Read.read_users()
    for user in data:
        user = CurrentUsers(**user.dict())
        console.print(json.dumps((user.dict()), indent=2))

@security.command()
def get_password(password: str = typer.Option(..., prompt=True, confirmation_prompt=True, hide_input=True)):
    password = Hashing.create_hash(password)
    console.print(password)

@security.command()
def make_config():
    user_list = []
    for value in iterate_user():
        user_list.append(ListingDB(**value).dict())
    console.print(user_list)

@security.command()
def table():
    table = Table('ID', 'Email/user', style="#00FF00")
    for value in iterate_user():
        user = ListingDB(**value)
        table.add_row(str(user.id), user.email)
    console.print(table)
    select: int = typer.prompt("please enter and ID to delete")
    Delete.delete_user(select)


@api.command()
def quick(
    host:str = typer.Option("0.0.0.0", prompt="Please enter and IP address"), 
    port:int = typer.Option(8000, prompt="Please enter and port"), 
    debug:bool = typer.Option(False, prompt="Would you like to run the server in debug mode"), 
    reload:bool = typer.Option(False, prompt="Would you like to hot reload the server "),
    open_window:bool = typer.Option(False, prompt="Would you like to a browser window?")
):
    if open_window: typer.launch(f"http://{host}:{port}/docs/")
    run_server(host=host, port=port, debug=debug, reload=reload)


if __name__ == "__main__":
    app()