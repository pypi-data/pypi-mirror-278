import os

import inquirer
import datetime
from izio_cli.helper.fs_helper import create_file
from rich import print
from rich.console import Console
from rich.table import Table
from typer import Context, Exit, Option, Typer

from izio_cli import __author__, __version__
from izio_cli.helper.console_helper import create_table, updateGradle
from izio_cli.helper.loyalty_helper import (
    changeAppIcon,
    changeSplash,
    changeOnesignalIcons,
    getEnv,
    setupEnvFile,
    setupFirebase,
    setupRemoteConfig,
)
from izio_cli.helper.pattern_helper import getPath, newModule, newPage
from izio_cli.helper.project_helper import (
    getPlatforms,
    getProjectName,
    getProjectPath,
    setupVsCode,
    setupWorkflows,
)
from izio_cli.helper.strings_transformers import (
    to_capitalized,
    to_pascal_case,
    to_snake_case,
    to_pascal_case_with_underscore,
)
from izio_cli.pattern.dot_net_pattern import (
    addReferences,
    create_entity,
    createNetCoreSolution,
)
from izio_cli.pattern.flutter_pattern import (
    create_page,
    createFlutterProj,
    getFlutterFlavors,
    getFlutterPages,
    getModules,
)
from izio_cli.pattern.flutter_pattern import new_module as flutter_new_module

console = Console()
app = Typer(epilog="Made by Saulo Senoski for Izio&Co")


def version_func(flag):
    if flag:
        print(f"[b white on green]izio_cli[/]")
        print(f"{__version__}")
        print(f"[blue][link=https://saulopef.github.io/izio_cli/]{__author__}[/]")
        raise Exit(code=0)


@app.callback(invoke_without_command=True)
def main(
    ctx: Context,
    version: bool = Option(
        False, "--version", "-v", callback=version_func, is_flag=True
    ),
):
    message = """Usage: [b white on green]izio_cli[/] [b][SUBCOMMAND] [ARGUMENTS][/]

 There are some subcommands available:

  [b u]::flutter::[/]
- [b]new-module[/]: Create new module for flutter project 
- [b]new-page[/]: Create new module for flutter project
- [b]loyalty-flavor[/]: Change the flavor of the Loyalty Flutter application
- [b]new-entity[/]: Create a new Entity in the .NET project

  [b u]::flutter, netCore::[/]
- [b]new-project[/]: Create new project for flutter or .NET * 

* [b i]Note:[/] [i]The .NET project is only available for Windows /
this command will only work if you have the .NET or Flutter SDK installed.[/]

[b]usage Examples:[/]
    izio create-module --module "my module"
    izio create-page --page "my page"
    izio create-project --project-name "my project" 

[b]to more quick info: [red]izio --help[/]

# [b]For detailed info please [blue][link=https://saulopef.github.io/izio_cli/]refer to de docs![/]
"""

    if ctx.invoked_subcommand:
        return
    console.print(message)


@app.command()
def new_module(
    path: str = Option(
        "",
        "--path",
        "-p",
        help="Path to the flutter project",
        hidden=True,
    ),
    module: str = Option("", "--module", "-m", help="Module name"),
):
    """
    Create a new module within a Flutter project.

    This command prompts the user to select or create a new module for a specified Flutter project.
    It also provides an option to create a new page in the module after creation.

    Attributes:
        path (str): The path to the Flutter project. If left empty, the user will be prompted.
        module (str): The name of the module to create. If left empty, the user will be prompted.

    Examples:

        izio new-module --module "my Module"
        {create a new module in the flutter project called "my_module"}

    """
    # Verify if the path exists
    path = getPath(path)

    # Create a list of modules
    modules = getModules(path)
    if not module:
        module = inquirer.list_input("Select a module", choices=modules)

        if module == "Cancel":
            raise Exit(code=0)

        if module == "New Module":
            module = newModule(modules)
            result = flutter_new_module(path, module)
            console.print(create_table(result))
    else:
        module = newModule(modules, module)
        result = flutter_new_module(path, module)
        console.print(create_table(result))

    confirm = inquirer.confirm(
        f"Do you want to create a new page in module {module}?", default=True
    )
    if not confirm:
        raise Exit(code=0)
    else:
        new_page(path, module=module, page="")

    return module


@app.command()
def new_page(
    path: str = Option(
        "",
        "--path",
        "-p",
        help="Path to the flutter project",
        hidden=True,
    ),
    module: str = Option("", "--module", "-m", help="Module name"),
    page: str = Option("", "--page", "-p", help="Page name"),
):
    """
    Create a new page within a module of a Flutter project.

    This command allows the creation of a new page in a specified module of a Flutter project.
    If module or page names are not provided, the user will be prompted.

    Args:

        path (str): The path to the Flutter project. If left empty, the user will be prompted.
        module (str): The name of the module where the page will be created. If left empty, the user will be prompted.
        page (str): The name of the page to be created. If left empty, the user will be prompted.

    Examples:

        izio createpage --module "my_module" --page "my_page"
    """

    # Verify if the path exists
    path = getPath(path)

    # Create a list of modules
    modules = getModules(path)

    if not module:
        module = inquirer.list_input("Select a module", choices=modules)

        if module == "Cancel":
            raise Exit(code=0)

        if module == "New Module":
            module = newModule(modules)
            result = flutter_new_module(path, module)
            console.print(create_table(result))
    else:
        # Verify if the module exists
        module = to_snake_case(module)

        if module not in modules:
            module = newModule(modules, module)
            result = flutter_new_module(path, module)
            console.print(create_table(result))

    if not page:
        page = inquirer.text("Enter the page name")
        page = to_pascal_case(page)
        print(f"Page name: {page}")
    else:
        page = to_pascal_case(page)

    pages = getFlutterPages(path, module)
    page = newPage(pages=pages, module=module, page=page)
    create_page(path, module, page, isResponsive=True)

    return page


@app.command()
def new_project(
    path: str = Option(
        "",
        "--path",
        "-p",
        help="Path to the flutter project",
        hidden=True,
    ),
    type: str = Option(
        "", "--type", "-t", help="Type of the project (flutter, netCore)"
    ),
    solution: str = Option(
        "IzPay",
        "--solution",
        "-s",
        help="What is the solution you are working on, like: Mangos, Loyalty, IzPay, etc",
    ),
    projectName: str = Option("", "--project-name", "-n", help="Name of the project"),
    platforms: str = Option("", "--platforms", "-l", help="Platforms"),
    description: str = Option(
        "", "--description", "-d", help="Description of the project"
    ),
):
    """Create a new Izio project of either Flutter or .NET type.
    This command initializes a new project, allowing the user to specify various details like project name, type, platforms, and description. The project type can be either Flutter or .NET.

    Attributes:
        path (str): The path where the project will be created. If left empty, the user will be prompted.
        type (str): The type of the project ('flutter' or 'netCore'). If left empty, the user will be prompted.
        solution (str): The solution name for the project. Default is 'IzPay'.
        projectName (str): The name of the project. If left empty, the user will be prompted.
        platforms (str): The platforms for the Flutter project (e.g., 'android,ios,web').
        description (str): A description of the project. If left empty, the user will be prompted.

    Examples:
        ```shell
        izio new-project -n "my_project" -s IzPay -d "my description" -p "path/to/project" -l "android,ios,web"
        {create a new flutter project in Mb.IzPay.flutter.my_project for android, ios, web}
        ```

        ```shell
        izio new-project -t netCore -n "my_dot_det_project" -s IzPay -d "my description" -p "path/to/project" -l "android,ios,web"
        {create a new flutter project in Be.IzPay.netCore.my_dot_det_project for android, ios, web}
        ```
    """

    if not type:
        type = inquirer.list_input(
            "Select the type of project, flutter or netCore | netCore is not suported on MacOs",
            choices=["flutter", "netCore"],
            default="flutter",
        )

    if not projectName:
        confirm, solutionName, projectName = getProjectName(
            type=type, solution=solution
        )
        if not confirm or not solutionName:
            confirm, solutionName, projectName = getProjectName(
                type=type, solution=solution
            )
            if not confirm:
                raise Exit(code=1)
            if not solutionName:
                raise ValueError("Project name is required")

        projectName = projectName
    else:
        confirm, solutionName, projectName = getProjectName(
            type=type, solution=solution
        )

    if not description:
        description = inquirer.text("Enter the project description")

    if not path:
        path = getProjectPath(
            solutionName,
        )
    else:
        path = getProjectPath(solutionName, path)

    if not platforms and type == "flutter":
        platforms = getPlatforms()

    # do not create a new project in the izio_cli folder
    if type == "flutter":
        setupVsCode(path, projectName, console)
        setupWorkflows(path, projectName, console)
        createFlutterProj(path, projectName, platforms, description, console)
    elif type == "netCore":
        createNetCoreSolution(path, projectName, solutionName, solution, console)
        # create first entity?
        entity = inquirer.confirm("Do you want to create a new entity?", default=True)
        if entity:
            new_entity(
                path=f"{path}", projectName=projectName, solutionName=solutionName
            )

    else:
        raise ValueError("Type of project not supported")


@app.command()
def loyaltyFlavor(
    path: str = Option(
        os.getcwd,
        "--path",
        "-p",
        help="Path to the Loyalty flutter project",
        hidden=True,
    ),
    flavor: str = Option("", "--flavor", "-f", help="Flavor name"),
):
    """
    Change the flavor of the Loyalty Flutter application.

    This command is used to change the flavor of the Loyalty Flutter application to a specified flavor. It includes updating various configuration files and settings to match the chosen flavor.

    Args:
    - path (str): The file system path to the root of the Loyalty Flutter project.
                  Defaults to the current working directory.
    - flavor (str): The name of the flavor to switch to. If not provided, the user will be
                    prompted to choose from available flavors.

    Raises:
    - ValueError: If the command is not run from within a Loyalty Flutter application directory.
    - Exit: If the specified flavor is not found among the available flavors.

    The command performs several actions:
    - Validates the current directory to ensure it's a Loyalty Flutter app.
    - Retrieves and lists available flavors from the 'envs' folder.
    - Prompts the user to select a flavor if not provided as an argument.
    - Updates Android settings (Gradle), app icon, OneSignal icons, and Firebase settings based on the selected flavor.
    - Sets up environment files corresponding to the new flavor.

    Upon successful execution, it updates the app to use the specified flavor.
    """
    # Verify if the command is running from a loyalty flutter app
    if "mb_izio.flutter.apployalty2_0" not in path:
        raise ValueError("This command must be run from a loyalty flutter app")

    # get root path of the app
    root = (
        path.split("mb_izio.flutter.apployalty2_0")[0] + "mb_izio.flutter.apployalty2_0"
    )
    # get all available flavors from envs folder
    flavors = getFlutterFlavors(root)

    # prompt the user to select a flavor
    if not flavor:
        flavor = inquirer.list_input("Select a flavor", choices=flavors)
    elif flavor not in flavors:
        print(f"Flavor {flavor} not found")
        print(f"Available flavors are: {flavors}")
        raise Exit(code=1)

    # change the flavor in the app
    # get env file data
    flavor, bundleId, appName, appIconPath = getEnv(flavor, root, console=console)

    with console.status(
        "Updating android settigns", spinner="arc", spinner_style="bold green"
    ) as status:
        updateGradle(root, bundleId, appName)
        status.update("Updating app icon")
        changeAppIcon(root, appIconPath.replace("/", os.sep))
        status.update("Updating onesignal icons")
        changeOnesignalIcons(root)
        status.update("Updating firebase settings")
        setupFirebase(flavor, root)
        status.update("setup envfile")
        setupEnvFile(flavor, root)
        status.stop()

    print(f"Loyalty Flavor changed to {flavor}!")


@app.command()
def izpay(
    path: str = Option(
        os.getcwd,
        "--path",
        "-p",
        help="Path to the IzPay flutter project",
        hidden=True,
    ),
    flavor: str = Option("", "--flavor", "-f", help="Flavor name"),
    platform: str = Option(
        "all",
        "--platform",
        "-0",
        help="Which platform to run the command [all, android, ios, web]",
    ),
    cd: bool = Option(
        False,
        "--cd",
        "-c",
        help="Mark if the command is running in a CD environment",
        hidden=True,
    ),
):
    """
    Change the flavor of the IzPay Flutter application.

    This command is used to change the flavor of the IzPay Flutter application to a specified flavor. It includes updating various configuration files and settings to match the chosen flavor.

    Args:
    - path (str): The file system path to the root of the IzPay Flutter project.
                  Defaults to the current working directory.
    - flavor (str): The name of the flavor to switch to. If not provided, the user will be
                    prompted to choose from available flavors.

    Raises:
    - ValueError: If the command is not run from within a IzPay Flutter application directory.
    - Exit: If the specified flavor is not found among the available flavors.

    The command performs several actions:
    - Validates the current directory to ensure it's a IzPay Flutter app.
    - Retrieves and lists available flavors from the 'envs' folder.
    - Prompts the user to select a flavor if not provided as an argument.
    - Updates Android settings (Gradle), app icon, OneSignal icons, and Firebase settings based on the selected flavor.
    - Sets up environment files corresponding to the new flavor.

    Upon successful execution, it updates the app to use the specified flavor.
    """
    print(f"Path: {path}")
    # Verify if the command is running from a loyalty flutter app
    if "mb_izpay" not in path:
        raise ValueError("This command must be run from a loyalty flutter app")

    # get root path of the app
    #   if path contains mb_izpay, split the path and get the first part
    if cd:
        root = path
    else:
        root = path.split("mb_izpay")[0] + "mb_izpay"
    # if path contains mb_izpay/mb_izpay, split the path and get part after the first mb_izpay

    # list directories inside the root
    dirs = [d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))]
    # exibe no console os diretorios de root
    print(f"Root: {root}")
    print(f"Dirs: {dirs}")
    # get all available flavors from envs folder

    if not cd and not flavor:

        flavors = getFlutterFlavors(root, flutterProject="izpay")

        # prompt the user to select a flavor
        if not flavor:
            flavor = inquirer.list_input("Select a flavor", choices=flavors)
        elif flavor not in flavors:
            print(f"Flavor {flavor} not found")
            print(f"Available flavors are: {flavors}")
            raise Exit(code=1)

    # change the flavor in the app
    # get env file data
    flavor, bundleId, appName, appIconPath, secondaryColor = getEnv(
        flavor, root, project="izpay", console=console
    )

    with console.status(
        "Setting up {flavor} app for {platform} platform(s)",
        spinner="arc",
        spinner_style="bold green",
    ) as status:
        if platform == "all" or platform == "android":
            status.update("Updating android settigns")
            updateGradle(root, bundleId, appName, project="izpay")
        status.update("Updating app icon")
        changeAppIcon(root, appIconPath.replace("/", os.sep), project="izpay")
        status.update("Updating Splash Screen")
        changeSplash(
            root, appIconPath.replace("/", os.sep), secondaryColor, project="izpay"
        )
        status.update("Updating onesignal icons")
        changeOnesignalIcons(root, project="izpay")
        status.update("Updating firebase settings")
        setupFirebase(flavor, root, project="izpay")
        status.update("setup envfile")
        setupEnvFile(flavor, root, project="izpay")
        status.stop()

    print(f"Success! [white on green]IzPay[/] Flavor changed to {flavor}!")


@app.command()
def new_entity(
    path: str = Option(
        "",
        "--path",
        "-p",
        help="Path to the project",
        hidden=True,
    ),
    entityName: str = Option("", "--name", "-n", help="Entity name"),
    solutionName: str = Option("", "--project", "-o", help="Project name"),
    projectName: str = Option("", "--project-name", "-n", help="Project name"),
):
    """
    Create a new Entity in the .NET project

    This command is used to create a new entity in the .NET project. It includes creating a new class file and adding it to the project.

    Args:
    - path (str): The file system path to the root of the .NET project.
                  Defaults to the current working directory.
    - name (str): The name of the entity to create. If not provided, the user will be
                    prompted to enter the name.

    Raises:
    - FileNotFoundError: If the command is not run from within a .NET project directory.
    - ValueError: If the specified entity name is not provided.

    """

    entityName = inquirer.text("Enter the entity name")
    if not entityName:
        raise ValueError("Entity name is required")

    if not solutionName:
        solutionName = inquirer.text("Enter the solution name")
        if not solutionName:
            raise ValueError("Solution name is required")

    if not path:
        path = (
            f"{os.getcwd()}{os.sep}{solutionName}"
            if solutionName not in os.getcwd()
            else os.getcwd()
        )

    create_entity(
        path,
        projectName=projectName,
        solutionName=solutionName,
        name=entityName,
        console=console,
    )


@app.command(hidden=True)
def testCommand():
    page = "splash screen"
    pageSnake = to_snake_case(page)
    pagePascal = to_pascal_case(pageSnake)

    print(f"Page name Pascal: {pagePascal}")
    print(f"Page name Snake: {pageSnake}")


@app.command()
def setup_remote_config(
    path: str = Option(
        os.getcwd,
        "--path",
        "-p",
        help="Path to the project",
        hidden=True,
    ),
    environment: str = Option(
        "dev", "--env", "-e", help="Environment name (dev, staging,prod)"
    ),
):
    """
    Setup remote config for the project
    """
    # Verify if the command is running from a loyalty flutter app
    if not environment:
        environment = inquirer.list_input(
            "Select a environment", choices=["dev", "staging", "prod"]
        )

    if environment not in ["dev", "staging", "prod"]:
        raise ValueError("Invalid environment")

    if "mb_izpay" not in path:
        raise ValueError("This command must be run from a loyalty flutter app")
    setupRemoteConfig(path, environment, console)


build_time = datetime.datetime.now()


def print_build_time():
    print("Build time:", build_time)


if __name__ == "__main__":
    app()
