from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.theme import Theme
from typing import Tuple
import typer
from main import run_server
from database.operations import Delete, Read, Create, SetupDatabase
from database.models.logs import *
from database.models.user import *
from views.auth import Hashing

console_theme = Theme(
    {"success": "green",
    "info": "blue",
    "warring":"underline yellow",
    "error": "bold underline red"}
)
console = Console(theme=console_theme)
app = typer.Typer(add_completion=False)

database = typer.Typer()
api = typer.Typer()

app.add_typer(database, name="db")
app.add_typer(api, name="api")

@database.command()
def test(user: Tuple[str, str, str, str] = typer.Option((None, None, None, None))):
    data = UsersSchema(
        first_name=user[0],
        last_name=user[1],
        email=user[2],
        password=user[3]
    )
    data.password = Hashing.create_hash(data.password)
    print(data)


@database.command()
def setup(create: bool = typer.Option(..., prompt="Would you like to run the setup script", confirmation_prompt=True)):
    if create:
        SetupDatabase.create_db_and_tables()

@database.command()
def clear_users():
    delete = typer.confirm("Are you sure you want to delete it?", abort=True)
    if delete:
        Delete.delete_all_users()

@database.command()
def add_user(
    first_name: str = typer.Option(..., prompt="Please enter your first name"),
    last_name: str = typer.Option(..., prompt="Please enter your last name"),
    email :str = typer.Option(..., prompt="Please enter your email address"),
    password: str = typer.Option(..., prompt="Please enter your password", confirmation_prompt=True, hide_input=True)
):
    password = Hashing.create_hash(password=password)
    user = UsersSchema(first_name=first_name.capitalize(), last_name=last_name.capitalize(), email=email.lower(), password=password)
    if typer.confirm("Are these the right details?", abort=True):
        Create.create_user(user)
        print(Panel(f"{user.first_name} {user.last_name}\n{user.email}", title="User created"))

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