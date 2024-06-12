import os
content = '''from yoyo import step

steps = [
    step(
        # put here the actual migration
        """
        
        """,
        # put here the rollback 
        """
        """
    )
]
'''


def create_migration_file(name: str):
    base_dir = os.getcwd()
    if not "src" in os.listdir(base_dir):
        return "Please change to the workspace directory of the project!"
    migration_path = os.path.join(base_dir, "src/db/migrations")
    if not os.path.exists(migration_path):
        return f"Folder not found in this path [bold] {migration_path}\nPlease make sure that didn't change the project template!"
    migration_files = os.listdir(migration_path)

    enumerations = [file.split("_")[0] for file in migration_files]
    enumerations = sorted(enumerations)
    message = ''
    try:
        index = int(enumerations[-1])+1
        print(enumerations)
        migration_filename = f"{index:04d}_{name}.py"
        if len(enumerations) == 0:
            migration_filename = f"0001_{name}.py"
        with open(os.path.join(migration_path, migration_filename), "w") as f:
            f.write(content)
    except Exception as e:
        return f"Got an error when creating the migration file make sure that you didn't put silly names!!\nError: {e}"

    return True
