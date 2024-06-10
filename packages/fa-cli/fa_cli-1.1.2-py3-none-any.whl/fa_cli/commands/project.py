import os
from .contents import PROJECT_STRUCTURE


def create_project_structure(base_path: str, structure: dict = PROJECT_STRUCTURE):
    for dir_name, files in structure.items():
        dir_path = os.path.join(base_path, dir_name)
        os.makedirs(dir_path, exist_ok=True)
        for file_name, content in files.items():
            file_path = os.path.join(dir_path, file_name)
            if isinstance(content, dict):
                # Recursively create subdirectories
                create_project_structure(dir_path, {file_name: content})
            else:
                # Create file with content
                with open(file_path, 'w') as f:
                    f.write(content)
