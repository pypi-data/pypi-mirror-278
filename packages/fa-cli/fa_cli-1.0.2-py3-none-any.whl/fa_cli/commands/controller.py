import os
import re

controller_content = """from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from src.controller.core import GenericController, Controller
from .schema import {}

@Controller
class {}(GenericController):
    def __init__(self, app: APIRouter) -> None:
        super().__init__(app)
        self.url_prefix = "/{}"
        self.add_api_route("/", self.example, methods=['POST'])
        self.app.include_router(self.router, prefix=self.url_prefix)
    async def get(self):
        pass
"""
schema_content = """from pydantic import BaseModel

class {}(BaseModel):
    pass
"""

init_update = "\from .{}.router import *"


def is_valid_name(s):
    pattern = r'^[\w]+$'
    return bool(re.match(pattern, s))


def create_controller(path: str):
    controller_name = path.split("/")[-1]
    controller_name = controller_name.replace("-", "_")
    controller_name = controller_name.replace(".", "_")
    if not is_valid_name(controller_name):

        return "Controller name must be in snake case does not special characters other then _ "
    root_dir = os.getcwd()
    files = os.listdir(root_dir)
    if not ("app.py" in files):
        return "Please change to the root directory"
    controller_path = os.path.join(root_dir, "src/controller", path)
    os.makedirs(controller_path, exist_ok=True)
    # create the file router and schema and add the router content
    class_name = " ".join(controller_name.split(
        '_')).capitalize().replace(" ", "")
    with open(os.path.join(controller_path, "router.py"), "w") as f:
        f.write(controller_content.format(class_name+"Schema"),
                class_name, class_name.lower())
    with open(os.path.join(controller_path, "schema.py"), "w") as f:
        f.write(controller_content.format(class_name+"Schema"))

    with open(os.path.join(root_dir, "src/controller", "__init__.py"), "a") as f:
        f.write(init_update.format(path.replace("/", ".")))
    return True
