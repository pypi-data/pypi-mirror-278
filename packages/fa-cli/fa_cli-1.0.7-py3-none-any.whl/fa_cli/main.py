import os
import typer
from typing import Optional
from .commands.project import create_project_structure
from .commands.controller import create_controller, delete_controller
from git import Repo
from rich import print


class FastAPICLI:
    def __init__(self):
        self.app = typer.Typer(help="FastAPI CLI tool")
        self.create_app = typer.Typer(help="Commands to create new project")
        self.generate = typer.Typer(help="Commands to generate Controllers")
        self.rm = typer.Typer(help="Commands to remove controllers")
        self.app.add_typer(self.create_app, name="new")
        self.app.add_typer(self.create_app, name="n")
        self.app.add_typer(self.generate, name="generate")
        self.app.add_typer(self.generate, name="g")
        self.app.add_typer(self.generate, name="rm")
        self.app.add_typer(self.generate, name="r")
        self._register_commands()

    def _register_commands(self):
        self.create_app.command("project")(self.init_project)
        self.create_app.command("p")(self.init_project)
        self.generate.command("controller")(self.create_controller)
        self.generate.command("c")(self.create_controller)
        self.rm.command("rm")(self.delete_controller)
        self.rm.command("r")(self.delete_controller)

    def init_project(self, name: str, repo: Optional[bool] = typer.Option(True, help="Init github repository"), skip_examples: Optional[bool] = typer.Option(False, help="Skip examples")):
        """
        Create the project structure.
        """
        print(f"[green] Initializing the workspace: {name}")
        base_path = os.path.join(os.getcwd(), name)
        if not os.path.exists(base_path):
            os.makedirs(base_path)
            create_project_structure(
                base_path=base_path, skip_examples=skip_examples)
        print(f"[green] workspace {name} created successfully!")
        if repo:
            Repo.init(base_path)
            print(f"[green] Repository successfully intialized!")
        print('[bold red] Now run the following command')
        print(f'[green] cd {name}')

    def create_controller(self, path: str):
        # try:
        result = create_controller(path=path)
        if isinstance(result, bool):
            print(f'[green] Done creating the controller {path}')
        else:
            print(f'[bold red] {result}')

    def delete_controller(self, path: str):
        result = delete_controller(path=path)
        if isinstance(result, bool):
            print(f'[green] Done removing the controller {path}')
        else:
            print(f'[bold red] {result}')

    def run(self):
        self.app()


def app():
    cli = FastAPICLI()
    cli.run()


if __name__ == "__main__":
    app()
