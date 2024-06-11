import os
import sys
import importlib
from pinnacle_cli.constants import DIRECTORY

def import_modules(subdirectory: str = ""):
    sys.path.append(os.getcwd())

    import_directory = DIRECTORY + subdirectory

    try: 
        for filename in os.listdir(import_directory):
            if filename.endswith(".py"):
                module_name = os.path.splitext(filename)[0]
                module_parent = (
                    import_directory[2:] if import_directory.startswith("./") else import_directory
                ).replace("/", ".")
                importlib.import_module(f"{module_parent + "." if module_parent else ""}{module_name}")
    except Exception as e:
        print(f"Error importing modules: {e}")
        sys.exit(1)
