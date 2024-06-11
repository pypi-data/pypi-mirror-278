from izio_cli.helper.strings_transformers import (
    to_pascal_case,
    to_snake_case,
    to_space_case,
)


def pagePayload(page: str):
    pageSnake = to_snake_case(page)
    pagePascal = to_pascal_case(page)
    return f"""
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../controller/{pageSnake}_controller.dart';

class {pagePascal}Page extends GetView<{pagePascal}Controller> {{
  const {pagePascal}Page({{Key? key}}) : super(key: key);

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(title: const Text('{pagePascal}Page')),
      body: const SafeArea(
        child: Text('{pagePascal}Controller'))
      );
  }}
}}
"""
def responsivePagePayload(page: str):
    pageSnake = to_snake_case(page)
    pagePascal = to_pascal_case(pageSnake)
    return f"""
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../controller/{pageSnake}_controller.dart';

class {pagePascal}Page extends GetResponsiveView<{pagePascal}Controller> {{
  {pagePascal}Page({{Key? key}}) : super(key: key);
  Widget responsiveWidget(bool isDesktop) {{
    //! Implementar layout responsivo usando o parametro isDesktop para definir o layout para desktop e mobile
    return Scaffold(
        appBar: AppBar(title: const Text('{pagePascal}Page')), body: const SafeArea(child: Text('{pagePascal}Controller')));
  }}

  @override
  Widget? desktop() {{
    super.desktop();
    return responsiveWidget(true);
  }}

  @override
  Widget? phone() {{
    super.phone();
    return responsiveWidget(false);
  }}
}}

"""


def controllerPayload(page: str):
    pageSnake = to_snake_case(page)
    pagePascal = to_pascal_case(page)
    return f"""
import 'package:get/get.dart';

class {pagePascal}Controller extends GetxController {{
}}
"""


def bindingPayload(page: str):
    pageSnake = to_snake_case(page)
    pagePascal = to_pascal_case(page)
    return f"""
import 'package:get/get.dart';
import '../controller/{pageSnake}_controller.dart';

class {pagePascal}Binding implements Bindings {{
@override
void dependencies() {{
  Get.lazyPut<{pagePascal}Controller>(() => {pagePascal}Controller());
  }}
}}
"""


def pullRequestPayload(projectName: str):
    projectName = to_space_case(projectName)
    return f"""
## IZio&co Pull Request

# {projectName}

## Impacto
<!--- Descreva as alteraçoes e o impacto delas -->

### Jira issue

> [IZIOPRJ-480](https://izio.atlassian.net/browse/IZIOPRJ-480) <!--- Please link to the Jira issue here: -->

## Sistemas impactados
<!---(Ex. Api que é usado pelo APP e Portal Cliente. Arquivo Datalake, Portal Loyalty, Extração por email e envio de dados para clientes) -->

## Evidencias dos testes realizados

<!-- Adicione imagens ou videos da alteração funcionando -->

### Checklist before requesting a review

> Obrigatório preencher todos os itens abaixo

- [ ] Self code review
- [ ] Unit tests
- [ ] Request reviewers
- [ ] Mangos Retail Know this?

> Selecionar pelo menos um item abaixo

- [ ] Hotfix (fix a production issue)
- [ ] Bugfix (fix a non-urgent issue)
- [ ] Feature (add a new feature)
- [ ] Refactor (refactor code)
"""


def launchFilePayload(projectName: str):
    return f"""{{
  //:: Gerado automaticamente pelo izio_cli::
  "version": "0.2.0",
  "configurations": [
    {{
      "name": "{projectName}",
      "cwd": "{projectName}",
      "request": "launch",
      "type": "dart"
    }},
    {{
      "name": "{projectName} (profile mode)",
      "cwd": "{projectName}",
      "request": "launch",
      "type": "dart",
      "flutterMode": "profile"
    }},
    {{
      "name": "{projectName} (release mode)",
      "cwd": "{projectName}",
      "request": "launch",
      "type": "dart",
      "flutterMode": "release"
    }}
  ]
}}
"""


def vscodeSettingsPayload(projectName: str):
    projectName = to_space_case(projectName)
    return f"""{{
"editor.formatOnSave": true,
"editor.wordWrapColumn": 80,
"editor.wordWrap": "wordWrapColumn"
}}
"""


def flutterCIWorkflowPayload(projectName: str):
    return f"""
name: Validate

on:
  pull_request:
    branches:
      - release
      - main

  workflow_dispatch:

jobs:
  flutter_test:
    name: Flutter Unit Tests and Lint
    runs-on: ${{ vars.LINUXRUNNER }}
    defaults:
      run:
        working-directory: {projectName}
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          # flutter-version: "3.13.9"
          channel: "stable"
          cache: true
      - run: flutter --version
      - name: Get dependencies
        run: |
          # git config --global --add safe.directory /actions-runner/_work/_tool/flutter/stable-3.10.5-x64
          flutter pub get

      - name: running lint analyze
        run: dart analyze
      - name: running tests
        run: flutter test
"""
