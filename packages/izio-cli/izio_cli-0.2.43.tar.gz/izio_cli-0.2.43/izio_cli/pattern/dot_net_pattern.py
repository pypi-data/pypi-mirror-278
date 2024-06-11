import os
from izio_cli.helper.strings_transformers import to_capitalized, to_pascal_case

from typer import Exit
from rich.console import Console
from izio_cli.helper.console_helper import run_command
from izio_cli.helper.fs_helper import create_directory, create_file
from izio_cli.helper.project_helper import getNetCoreProjects, setupWorkflows
from izio_cli.values.dot_net_payload import deValidationPayload, envPayload, modelAssmblyMarkerPayload, responseArrayInterfacePayload, responseArrayPayload, responseInterfacePayload, responsePayload, unitOfWokInterfacePayload, unitOfWorkPayload


def createNetCoreSolution(path, projectName, solutionName, solution, console):
    with console.status(
        "Creating a new solution", spinner="arc", spinner_style="bold green"
    ) as status:
        """
        Create a new .NET Core solution with a specified structure.

        This function initializes a new .NET Core solution using the 'dotnet new sln' command and sets up various projects within the solution. It also adds cross references, Izio library, and creates submodules as necessary.

        Args:
        - path (str): The file system path where the new .NET Core solution should be created.
        - projectName (str): The name of the project.
        - solution (str): The solution name for the new .NET Core project.
        - console (Console): The Rich console object for displaying the status.

        Note:
        The function assumes a specific structure and naming convention for the .NET Core projects within the solution.
        """

        setupWorkflows(path, solutionName, console)
        run_command(
            [
                "dotnet",
                "new",
                "sln",
                "-n",
                solutionName,
            ],
            path=path,
        )
        status.stop()
        projects = getNetCoreProjects(projectName)
        console.print(f"solutionName: {solutionName}, projectName: {projectName} projects: {projects}")

        status.start()
        if projects:
            status.update(
                status=f"Creating the following projects: {" ".join(projects)}",
            )
            createNetCoreProjects(path, projectName, projects)
            status.update(status="Adding cross references")
            addReferences(projectName, path)

            status.update(status="Adding external dependencies")
            addExternalDependencies(projectName, path)
            # teste de criação de entidade

            status.update(status="Creating submodules")
            createSubmodules(path, projectName)

            status.update(status="Setup apm")
            with open(
                f"{path}{os.sep}{projectName}.Api{os.sep}program.cs", "r"
            ) as file:
                data = file.read()
                # replace app.run() with app.UseElasticApm() and app.run()
                data = data.replace(
                    "app.Run();",
                    "app.UseElasticApm();\napp.Run();",
                )

            with open(
                f"{path}{os.sep}{projectName}.Api{os.sep}program.cs", "w"
            ) as file:
                file.write(data)

            status.update(status="Create default files!")
            create_file(f"{path}{os.sep}{projectName}.Application{os.sep}Dtos{os.sep}Responses", "ModelAssemblyMarker.cs", payload=modelAssmblyMarkerPayload(solution))

            status.update(status="Setup .env file")
            create_file(
                f"{path}{os.sep}{projectName}.Api",
                filename=".env",
                payload=envPayload(),
            )
            # succes message
            status.stop()
            console.print(
                f"🚀 [green]Successfully created the[/] [b].NET Core[/] solution",) 
            console.print("🚀 [green]You can now start coding![/]")

        else:
            Exit(code=0)


def createNetCoreProjects(path, projectName, projects):
    """
    Create .NET Core projects within a solution.

    This function iterates over a list of projects and creates each one using the 'dotnet new' command. It also adds each project to the solution file.

    Args:
    - path (str): The file system path where the projects should be created.
    - projectName (str): The name of the project.
    - projects (list): A list of project names to be created.
    """

    for project in projects:
        print(f"Creating project: {project}")
        run_command(
            [
                "dotnet",
                "new",
                "webapi" if project == f"{projectName}.Api" else "classlib",
                "-n",
                f"{project}",
            ],
            path=path,
        )
        run_command(
            [
                "dotnet",
                "sln",
                "add",
                f"{project}" + os.sep + f"{project}.csproj",
            ],
            path=path,
        )


def addReferences(projectName, path):
    """
    Add project references in a .NET Core solution.

    This function sets up references between different projects in a .NET Core solution based on a predefined structure.

        - Api: ["Infra.DependencyInjection"],
        - Application: ["Domain", "Infra.DependencyInjection"],
        - Infra.DataAccess: ["Offer.Domain"],
        - Infra.DependencyInjection: ["Offer.Domain"],
        - Domain: none,

    Args:
    - projectName (str): The name of the main project.
    - path (str): The file system path where the projects are located.
    """

    referencies = {
        "Api": ["Infra.DependencyInjection"],
        "Application": ["Domain"],
        "Infra.DataAccess": ["Domain"],
        "Infra.DependencyInjection": ["Application", "Domain", "Infra.DataAccess"],
    }
    for project, refs in referencies.items():
        for ref in refs:
            run_command(
                [
                    "dotnet",
                    "add",
                    f"{projectName}.{project}{os.sep}{projectName}.{project}.csproj",
                    "reference",
                    f"{projectName}.{ref}{os.sep}{projectName}.{ref}.csproj",
                ],
                path=path,
            )


def addExternalDependencies(projectName: str, path: str):
    """
    Add external dependencies to .NET Core projects.

    This function adds external dependencies to various .NET Core projects within the solution.

    ---Application
        AutoMapper
        FluentValidation.AspNetCore
        Microsoft.Extensions.DependencyInjection
        Swashbuckle.AspNetCore.Annotations
    
    ---Domain
        Microsoft.Extensions.DependencyInjection
        BE_Izio.Core.Biblioteca
    
    ---Infra.DependencyInjection
        Swashbuckle.AspNetCore.SwaggerUI

    Args:
    - projectName (str): The name of the main project.
    - path (str): The file system path where the DataAccess project is located.
    """
    # TODO: Add the new Izio Library package to the Domain and  project
    run_command(
        [
            "dotnet",
            "add",
            f"{projectName}.Domain{os.sep}{projectName}.Domain.csproj",
            "package",
            "Library",
            "--source",
            "https://api.nuget.org/v3/index.json"
        ],
        path=path,
    )

    run_command(
        [
            "dotnet",
            "add",
            f"{projectName}.Domain{os.sep}{projectName}.Domain.csproj",
            "package",
            "Microsoft.Extensions.DependencyInjection",
        ],
        path=path,
    )

    run_command(
        [
            "dotnet",
            "add",
            f"{projectName}.Infra.DependencyInjection{os.sep}{projectName}.Infra.DependencyInjection.csproj",
            "package",
            "Swashbuckle.AspNetCore.SwaggerUI",
        ],
        path=path,
    )

    run_command(
        [
            "dotnet",
            "add",
            f"{projectName}.Application{os.sep}{projectName}.Application.csproj",
            "package",
            "AutoMapper",
        ],
        path=path,
    )

    run_command(
        [
            "dotnet",
            "add",
            f"{projectName}.Application{os.sep}{projectName}.Application.csproj",
            "package",
            "FluentValidation.AspNetCore",
        ],
        path=path,
    )

    run_command(
        [
            "dotnet",
            "add",
            f"{projectName}.Application{os.sep}{projectName}.Application.csproj",
            "package",
            "Microsoft.Extensions.DependencyInjection",
        ],
        path=path,
    )

    run_command(
        [
            "dotnet",
            "add",
            f"{projectName}.Application{os.sep}{projectName}.Application.csproj",
            "package",
            "Swashbuckle.AspNetCore.Annotations",
        ],
        path=path,
    )


def createSubmodules(path, projectName):
    """
    Create submodules for various projects in a .NET Core solution.

    This function creates a set of predefined submodules (directories) for different projects within the solution, such as Extensions, Services, DTOs, Validators, etc.

        ...Api/Controllers
        ...Application/Dtos
        ...Application/Dtos/Responses
        ...Application/Interfaces
        ...Application/Mappers
        ...Application/Services
        ...Application/Validators
        ...Domain/Entities
        ...Domain/Interfaces
        ...Domain/Validations
        ...Infra.DataAccess/Repository
        ...Infra.DependencyInjection/Infra


    Args:
    - path (str): The file system path where the submodules should be created.
    - projectName (str): The name of the main project.
    """
    subMobules = [
        projectName + f".Api{os.sep}Controllers",
        projectName + f".Application{os.sep}Dtos",
        projectName + f".Application{os.sep}Dtos{os.sep}Responses",
        projectName + f".Application{os.sep}Interfaces",
        projectName + f".Application{os.sep}Mappers",
        projectName + f".Application{os.sep}Services",
        projectName + f".Application{os.sep}Validators",
        projectName + f".Domain{os.sep}Entities",
        projectName + f".Domain{os.sep}Interfaces",
        projectName + f".Domain{os.sep}Validations",
        projectName + f".Infra.DataAccess{os.sep}Repository",
        projectName + f".Infra.DataAccess{os.sep}Configuration",
        projectName + f".Infra.DependencyInjection{os.sep}Infra",
    ]
    for sub in subMobules:
        create_directory(f"{path}{os.sep}{sub}")


def create_entity(path, projectName, solutionName , name: str, console: Console):
    name = to_capitalized(name)
    
    console.print(f"🛠️ [blue]Creating entity in path: {path}{os.sep}{projectName}.Domain{os.sep}Entities")

    with console.status("Creating a new entity", spinner="arc", spinner_style="bold green") as status:

        create_file(
            f"{path}{os.sep}{projectName}.Domain{os.sep}Entities", f"{name}.cs", payload=f"// Todo: implement {name}.cs"
        )
        status.update(status="Creating API Controllers")
        create_file(
            f"{path}{os.sep}{projectName}.Api{os.sep}Controllers",
            f"{name}AppController.cs",
            payload=f"// Todo: implement {name}AppController.cs",
        )
        create_file(
            f"{path}{os.sep}{projectName}.Api{os.sep}Controllers",
            f"{name}OfficeController.cs",
            payload=f"// Todo: implement {name}OfficeController.cs",
        )
        status.update(status="Creating Domain Interfaces")
        create_file(
            f"{path}{os.sep}{projectName}.Domain{os.sep}Interfaces",
            f"I{name}AppRepository.cs",
            payload=f"// Todo: implement {name}AppRepository.cs",
        )
        create_file(
            f"{path}{os.sep}{projectName}.Domain{os.sep}Interfaces",
            f"I{name}OfficeRepository.cs",
            payload=f"// Todo: implement {name}OfficeRepository.cs",
        )
        status.update(status="Creating Domain Validations")
        create_file(
            f"{path}{os.sep}{projectName}.Domain{os.sep}Validations",
            "DomainExeptionValidation.cs",
            payload=deValidationPayload(solutionName),
        )
        status.update(status="Creating Application Dtos")
        create_file(
            f"{path}{os.sep}{projectName}.Application{os.sep}Dtos", f"{name}App.cs", payload=f"// Todo: implement {name}App.cs"
        )
        create_file(
            f"{path}{os.sep}{projectName}.Application{os.sep}Dtos",
            f"{name}Office.cs",
            payload=f"// Todo: implement {name}Office.cs",
        )
        status.update(status="Creating Application Interfaces")
        create_file(
            f"{path}{os.sep}{projectName}.Application{os.sep}Interfaces",
            f"I{name}AppServices.cs",
            payload=f"// Todo: implement {name}AppServices.cs",
        )
        create_file(
            f"{path}{os.sep}{projectName}.Application{os.sep}Interfaces",
            f"I{name}OfficeServices.cs",
            payload=f"// Todo: implement {name}OfficeServices.cs",
        )
        status.update(status="Creating Application Mappers")
        create_file(
            f"{path}{os.sep}{projectName}.Application{os.sep}Mappers", f"MappingProfile.cs", payload="// Todo: implement"
        )
        status.update(status="Creating Application Services")
        create_file(
            f"{path}{os.sep}{projectName}.Application{os.sep}Services",
            f"{name}AppServices.cs",
            payload="// Todo: implement {name}AppServices.cs",
        )
        create_file(
            f"{path}{os.sep}{projectName}.Application{os.sep}Services",
            f"{name}OfficeServices.cs",
            payload=f"// Todo: implement {name}OfficeServices.cs",
        )
        status.update(status="Creating Application Validators")
        create_file(
            f"{path}{os.sep}{projectName}.Infra.DataAccess{os.sep}Repository",
            f"{name}AppRepository.cs",
            payload="// Todo: implement",
        )
        status.update(status="Creating Infra DataAccess")
        create_file(
            f"{path}{os.sep}{projectName}.Infra.DataAccess{os.sep}Repository",
            f"{name}OfficeRepository.cs",
            payload="// Todo: implement",
        )
        
        console.print(f"🚀 [green]Successfully created the[/] [b blue].NET Core[/] Entity: {name}")