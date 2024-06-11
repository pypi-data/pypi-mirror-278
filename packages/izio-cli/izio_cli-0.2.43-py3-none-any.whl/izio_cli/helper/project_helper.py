import os

import inquirer

from izio_cli.helper.strings_transformers import (
    to_pascal_case,
    to_pascal_case_with_underscore,
    to_snake_case,
)
from izio_cli.pattern.flutter_pattern import create_directory, create_file
from izio_cli.values.flutter_payloads import (
    flutterCIWorkflowPayload,
    launchFilePayload,
    pullRequestPayload,
    vscodeSettingsPayload,
)


def getPlatforms():
    result = inquirer.prompt(
        [
            inquirer.Checkbox(
                "platforms",
                message="Select the platforms",
                choices=[
                    "android",
                    "ios",
                    "web",
                    "windows",
                    "linux",
                    "macos",
                ],
                default=["android", "ios", "web"],
            )
        ]
    )

    platforms = ",".join(result["platforms"])
    return platforms


def getNetCoreProjects(projectName):
    projectName = to_pascal_case(projectName)
    return [
        f"{projectName}.Api",
        f"{projectName}.Application",
        f"{projectName}.Infra.DependencyInjection",
        f"{projectName}.Infra.DataAccess",
        f"{projectName}.Domain",
    ]


def getProjectPath(solutionName, path=os.getcwd()):
    path = f"{path}{os.sep}{solutionName}"
    confirm = inquirer.confirm(
        f"Do you want to create a new project in {path}", default=True
    )
    if not confirm:
        path = inquirer.prompt(
            [inquirer.Path("path", message="Enter the project path", default=path)]
        )["path"]
    return path


def getProjectName(projeName="", type="flutter", solution="IzPay") -> tuple[bool, str, str]:
    if not projeName:
        projecName = to_pascal_case(inquirer.text("Enter the project name"))
    else:
        projecName = to_pascal_case(projeName)
        
    solutionName = (
        f"Mb_{solution}.flutter.{projecName}"
        if type == "flutter"
        else f"Be_{solution}.{projecName}"
    )
    confirm = inquirer.confirm(f"Your project name will be {solutionName}", default=True)
    return (confirm, solutionName, projecName)


def setupWorkflows(path, projectName, console):
    console.print("Creating pull request template")
    create_directory(
        path,
    )
    create_directory(
        f"{path}{os.sep}.github",
    )
    console.print("Creating continuous integration workflow")
    create_directory(
        f"{path}{os.sep}.github{os.sep}workflows",
    )
    create_file(
        f"{path}{os.sep}.github",
        filename="pull_request_template.md",
        payload=pullRequestPayload(projectName),
    )
    create_file(
        f"{path}{os.sep}.github{os.sep}workflows",
        filename="continuous-integration.yml",
        payload=flutterCIWorkflowPayload(projectName),
    )


def setupVsCode(path, projectName, console):
    console.print("Creating vscode and lint settings")
    create_directory(
        f"{path}{os.sep}.vscode",
    )
    create_file(
        f"{path}{os.sep}.vscode",
        filename="launch.json",
        payload=launchFilePayload(projectName),
    )
    create_file(
        f"{path}{os.sep}.vscode",
        filename="settings.json",
        payload=vscodeSettingsPayload(projectName),
    )
