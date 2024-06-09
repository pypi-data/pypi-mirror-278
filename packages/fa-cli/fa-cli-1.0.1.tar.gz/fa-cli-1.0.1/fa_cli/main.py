import os
import typer
from typing import Optional
from .commands.project import create_project_structure
from .commands.controller import create_controller
from git import Repo
from rich import print


class FastAPICLI:
    def __init__(self):
        self.app = typer.Typer(help="FastAPI CLI tool")
        self.create_app = typer.Typer(help="Commands to create new project")
        self.generate = typer.Typer(help="Commands to generate elements")
        self.app.add_typer(self.create_app, name="new")
        self.app.add_typer(self.create_app, name="n")
        self.app.add_typer(self.generate, name="generate")
        self.app.add_typer(self.generate, name="g")
        self._register_commands()

    def _register_commands(self):
        self.create_app.command("project")(self.init_project)
        self.create_app.command("p")(self.init_project)
        self.generate.command("controller")(self.create_controller)
        self.generate.command("c")(self.create_controller)

    def init_project(self, name: str, repo: Optional[bool] = typer.Option(True, help="Init github repository")):
        """
        Create the project structure.
        """
        typer.echo(f"Initializing the workspace: {name}")
        base_path = os.path.join(os.getcwd(), name)
        if not os.path.exists(base_path):
            os.makedirs(base_path)
            create_project_structure(base_path=base_path)
        typer.echo(f"workspace {name} created successfully!")
        if repo:
            Repo.init(base_path)
            typer.echo(f"Repository successfully intialized!")
        print('[bold red] Now run the following command')
        print(f'[green] cd {name}')

    def create_controller(self, path: str):
        # try:
        result = create_controller(path=path)
        if isinstance(result, bool):
            print(f'[green] Done creating the controller {path}')
        else:
            print(f'[bold red] {result}')

    def run(self):
        self.app()


def app():
    cli = FastAPICLI()
    cli.run()


if __name__ == "__main__":
    app()
