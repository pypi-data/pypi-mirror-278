import os

import inquirer
from typer import Exit

from izio_cli.helper.console_validators import module_validation, page_validation
from izio_cli.helper.strings_transformers import to_snake_case


def newModule(modules: list[str], module: str = ""):
    newModule = ""
    if not module:
        newModule = inquirer.text(
            "Enter the module name",
            validate=lambda _, x: module_validation(modules, x),
        )
        newModule = to_snake_case(newModule)
        if newModule in modules:
            raise ValueError("Module already exists")
    else:
        newModule = to_snake_case(module)
        print(newModule)
        if newModule in modules:
            raise ValueError("Module already exists")

    module = newModule

    confirm = inquirer.confirm(
        f"Do you want to create a new module named {module}?", default=True
    )

    if not confirm:
        raise Exit(code=0)
    return module


def newPage(pages: list[str], module: str, page: str = ""):
    newPage = ""
    if not page:
        newPage = inquirer.text(
            "Enter the page name",
            validate=lambda _, x: page_validation(pages, x),
        )
        if f"{to_snake_case(newPage)}_page.dart" in pages:
            raise ValueError("Page already exists")
    else:
        newPage = page
        if f"{to_snake_case(newPage)}_page.dart" in pages:
            raise ValueError("Page already exists")

    page = to_snake_case(newPage)
    confirm = inquirer.confirm(
        f"Do you want to create a new page named {page} in module {module}?",
        default=True,
    )
    if not confirm:
        raise Exit(code=0)
    return page


def getPath(path: str):
    if not path:
        # verify if current path is a flutter project
        current_path = os.getcwd()
        if not os.path.exists(current_path + f"{os.sep}pubspec.yaml"):
            path = inquirer.prompt(
                [
                    inquirer.Path(
                        "path",
                        message="pubspec.yaml not found, please enter the path to the flutter project",
                        path_type=inquirer.Path.DIRECTORY,
                        exists=True,
                    )
                ]
            )["path"]
            if path == "":
                Exit(code=1)
        else:
            path = current_path

    return path
