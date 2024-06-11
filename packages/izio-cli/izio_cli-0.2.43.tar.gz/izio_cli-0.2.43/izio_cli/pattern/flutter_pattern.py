
import os

from izio_cli.helper.console_helper import run_command
from izio_cli.helper.fs_helper import create_directory, create_file
from izio_cli.helper.strings_transformers import to_snake_case
from izio_cli.values.flutter_payloads import (
    bindingPayload,
    controllerPayload,
    pagePayload,
    responsivePagePayload,
)

_subdirectories = [
    "binding",
    "controller",
    f"data{os.sep}data_sources",
    f"data{os.sep}models",
    f"data{os.sep}repo_impls",
    f"domain{os.sep}entities",
    f"domain{os.sep}repositories",
    f"domain{os.sep}use_cases",
    f"ui{os.sep}components",
]

_dirFilter = ["app", "firebase", "pages"]


def getModules(path: str):
    """
    Retrieve the list of Flutter modules from a given path.

    This function gets all Flutter module directories in the specified path, as a module. It adds "Cancel" and "New Module" options to the list of modules for user interaction.

    Args:
    - path (str): The file system path where Flutter modules are located.

    Returns:
    - list: A list of module names including "Cancel" and "New Module" options.
    """

    modules = getFlutterModules(path)
    modules.append("Cancel")
    modules.insert(0, "New Module")
    return modules



def getFlutterModules(path: str):
    """
    Retrieve the list of Flutter modules excluding certain predefined directories.

    This function checks for the existence of 'pubspec.yaml' and 'lib' folder in the specified path and then lists all the directories that are considered Flutter modules.

    Args:
    - path (str): The file system path where the Flutter project is located.

    Returns:
    - list: A sorted list of Flutter module names.

    Raises:
    - Exception: If 'pubspec.yaml' or 'lib' folder is not found in the given path.
    """
        
    # Verify if the path is a flutter project
    if not os.path.exists(path + f"{os.sep}pubspec.yaml"):
        raise Exception("pubspec.yaml not found, this is a flutter project?")

    # Verify if the path contains a lib folder
    if not os.path.exists(path + f"{os.sep}lib"):
        raise Exception("lib folder not found")

    modules = [
        d
        for d in os.listdir(path + f"{os.sep}lib")
        if os.path.isdir(os.path.join(path + f"{os.sep}lib", d))
    ]
    modules = [m for m in modules if m not in _dirFilter]
    modules.sort()
    return modules

def getFlutterFlavors(root: str, flutterProject="loyalty2_0"):
    """
    Retrieve the list of Flutter modules excluding certain predefined directories.

    This function checks for the existence of 'pubspec.yaml' and 'lib' folder in the specified path and then lists all the directories that are considered Flutter modules.

    Args:
    - path (str): The file system path where the Flutter project is located.

    Returns:
    - list: A sorted list of Flutter module names.

    Raises:
    - Exception: If 'pubspec.yaml' or 'lib' folder is not found in the given path.
    """
        
    # Verify if the path is a flutter project
    path = root + f"{os.sep}{flutterProject}{os.sep}envs"

    if not os.path.exists(path):
        raise Exception("envs folder not found, this is a izio project?")

    # list .env files inside envs folder
    flavors = [ f for f in os.listdir(path) if f.endswith(".env")]
    # remove .env extension
    flavors = [f[:-4] for f in flavors]

    flavors.sort()
    return flavors

def getFlutterPages(path: str, module: str):
    """
    Retrieve the list of Flutter pages from a specified module.

    This function lists all Dart files that end with '_page.dart' in the 'ui' directory of a given module.

    Args:
    - path (str): The file system path where the Flutter project is located.
    - module (str): The name of the module to search for pages.

    Returns:
    - list: A sorted list of Flutter page names.
    """
    pages = [
        d
        for d in os.listdir(path + f"{os.sep}lib{os.sep}" + module + f"{os.sep}ui")
        if os.path.isfile(os.path.join(path + f"{os.sep}lib{os.sep}" + module + f"{os.sep}ui", d))
    ]
    pages = [p for p in pages if p.endswith("_page.dart")]
    pages.sort()
    return pages


def new_module(path, module) -> dict[list[str], list[str]]:
    """
    Create a new module with subdirectories for a Flutter project.

    This function creates a new module directory and all the required subdirectories in the Flutter project. It returns the status of each directory creation.

    Args:
    - path (str): The file system path where the Flutter project is located.
    - module (str): The name of the module to be created.

    Returns:
    - dict: A dictionary with two lists, 'Directory' and 'status', indicating the names of created directories and their creation status respectively.
    """
    directories = []
    status = []

    result = create_directory(f"{path}{os.sep}lib{os.sep}{module}")
    directories.append(f"{result["directory"]} (module)")
    status.append(result["status"])

    for subdirectory in _subdirectories:
        result = create_directory(f"{path}{os.sep}lib{os.sep}{module}{os.sep}{subdirectory}")
        directories.append(f"{os.sep}" + subdirectory)
        status.append(result["status"])

    return {"Directory": directories, "status": status}

def create_page(path, module, page, isResponsive=False) -> dict[list[str], list[str]]:
    """
    Create the necessary files for a new page in a Flutter module.

    This function creates Dart files for UI, binding, and controller layers of a new page in the specified module. It returns the status of each file creation.

    Args:
    - path (str): The file system path where the Flutter project is located.
    - module (str): The module in which the page will be created.
    - page (str): The name of the page to be created.

    Returns:
    - dict: A dictionary with two lists, 'File' and 'Status', indicating the names of created files and their creation status respectively.
    """


    files = []
    status = []
    

    pageSnake = to_snake_case(page)

    if pageSnake.endswith("_page"):
        pageSnake = pageSnake[:-5]

    result = create_file(f"{path}{os.sep}lib{os.sep}{module}{os.sep}ui", f"{pageSnake}_page.dart", responsivePagePayload(page=page) if isResponsive else pagePayload(page=page))
    files.append(f"{result["file"]}")
    status.append(result["status"])

    result = create_file(f"{path}{os.sep}lib{os.sep}{module}{os.sep}binding", f"{pageSnake}_binding.dart", bindingPayload(page=page))
    files.append(f"{result["file"]}")
    status.append(result["status"])

    result = create_file(f"{path}{os.sep}lib{os.sep}{module}{os.sep}controller", f"{pageSnake}_controller.dart", controllerPayload(page=page))
    files.append(f"{result["file"]}")
    status.append(result["status"])

    return {"File": files, "Status": status}


def createFlutterProj(path, projectName, platforms, description, console):
    with console.status(
        "Creating a new project", spinner="arc", spinner_style="bold green"
    ):
        """
        Create a new Flutter project with specified parameters.

        This function initializes a new Flutter project using the 'flutter create' command with the given project name, platforms, and description. It shows a status spinner during the creation process.

        Args:
        - path (str): The file system path where the new Flutter project should be created.
        - projectName (str): The name of the new Flutter project.
        - platforms (str): The platforms for the Flutter project (e.g., 'android,ios,web').
        - description (str): A description for the new Flutter project.
        - console (Console): The Rich console object for displaying the status.

        Note:
        The function uses 'br.com.izio' as the default organization name.
        """
        run_command(
            [
                "flutter",
                "create",
                "-e",
                projectName,
                "--description",
                description if description else "A new Izio Flutter project.",
                "--platforms",
                platforms,
                "--org",
                "br.com.izio"
            ],
            path=path,
        )
