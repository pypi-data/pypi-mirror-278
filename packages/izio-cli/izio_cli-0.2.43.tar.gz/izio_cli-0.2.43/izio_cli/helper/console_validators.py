import inquirer

from izio_cli.helper.strings_transformers import to_snake_case


def module_validation(modules, current):
    if to_snake_case(current) in modules:
        raise inquirer.errors.ValidationError(
            "",
            reason="This module name already exists. Please choose a different name.",
        )

    return True


def page_validation(pages, current):
    if f"{to_snake_case(current)}_page.dart" in pages:
        raise inquirer.errors.ValidationError(
            "",
            reason="This page name already exists. Please choose a different name.",
        )

    return True
