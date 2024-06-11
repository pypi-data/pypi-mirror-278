import os
import shutil
import json
import re
from izio_cli.helper.console_helper import run_command
from rich.table import Table


def setupFirebase(flavor, root, project="loyalty2_0"):
    print(f"Setting up firebase Android for {flavor} flavor, in {project} project... from {root}...")
    # get android firebase json
    shutil.copy2(f"{root}{os.sep}firebase{os.sep}android{os.sep}google-services-{flavor}.json",
            f"{root}{os.sep}{project}{os.sep}android{os.sep}app{os.sep}src{os.sep}prod{os.sep}google-services.json",)
    
    shutil.copy2(f"{root}{os.sep}firebase{os.sep}web{os.sep}firebase_options_{flavor}.txt",
            f"{root}{os.sep}{project}{os.sep}lib{os.sep}firebase_options.dart",)
    

    print(f"Setting up firebase iOS for {flavor} flavor, in {project} project... from {root}...")
    # get ios firebase json
    shutil.copy2(f"{root}{os.sep}firebase{os.sep}apple{os.sep}GoogleService-Info-{flavor}.plist",
            f"{root}{os.sep}{project}{os.sep}ios{os.sep}Runner{os.sep}prod{os.sep}GoogleService-Info.plist",)
    with open(f"{root}{os.sep}firebase{os.sep}web{os.sep}firebase_options_{flavor}.txt", "r") as file:
        content = file.read()

        project_id = ''

    # Split lines and find the line containing 'projectId'
        for line in content.splitlines():
            if 'projectId' in line:
                project_id = line.split(':')[-1].strip().strip(',').strip('"')
                break

        print(f"Project ID: {project_id}")
          
        with open(f"{root}{os.sep}.firebaserc",'r') as file:
            data = json.load(file)
            data['projects']['default'] = project_id

            with open(f"{root}{os.sep}.firebaserc", "w") as file:
                json.dump(data, file, indent=4)



def changeOnesignalIcons(root, project="loyalty2_0"):
    if not os.getenv("CI"):
        print(f"Skipping Onesignal icons setup on a non cd environment")
        return
    
    base_path = f"{root}{os.sep}{project}{os.sep}android{os.sep}app{os.sep}src{os.sep}prod{os.sep}res"
    # create drawable folders
    folders = [
        "drawable-mdpi",
        "drawable-hdpi",
        "drawable-xhdpi",
        "drawable-xxhdpi",
        "drawable-xxxhdpi",
    ]
    for folder in folders:
        os.makedirs(f"{base_path}{os.sep}{folder}", exist_ok=True)

    files = {
        f"mipmap-hdpi{os.sep}ic_launcher.png": f"drawable-mdpi{os.sep}ic_stat_onesignal_default.png",
        f"mipmap-mdpi{os.sep}ic_launcher.png": f"drawable-hdpi{os.sep}ic_stat_onesignal_default.png",
        f"mipmap-xhdpi{os.sep}ic_launcher.png": f"drawable-xhdpi{os.sep}ic_stat_onesignal_default.png",
        f"mipmap-xxhdpi{os.sep}ic_launcher.png": f"drawable-xxhdpi{os.sep}ic_stat_onesignal_default.png",
        f"mipmap-xxxhdpi{os.sep}ic_launcher.png": f"drawable-xxxhdpi{os.sep}ic_stat_onesignal_default.png",
        f"mipmap-xxxhdpi{os.sep}ic_launcher.png": f"drawable-xxxhdpi{os.sep}ic_onesignal_large_icon_default.png",
    }
    for file, new_file in files.items():
        shutil.copy2(f"{base_path}{os.sep}{file}", f"{base_path}{os.sep}{new_file}")



def changeAppIcon(root, appIconPath, project="loyalty2_0"):
    with open(
        f"{root}{os.sep}{project}{os.sep}flutter_launcher_icons-prod.yaml", "r"
    ) as file:
        data = file.read()
        actualIcon = data.split("image_path: ")[1].split("\n")[0]
        data = data.replace(f"image_path: {actualIcon}", f"image_path: {appIconPath}")
        with open(
            f"{root}{os.sep}{project}{os.sep}flutter_launcher_icons-prod.yaml", "w"
        ) as file:
            file.write(data)

    shutil.copy2(
        f"{root}{os.sep}{project}{os.sep}ios{os.sep}Runner.xcodeproj{os.sep}project.pbxproj",
        f"{root}{os.sep}{project}{os.sep}ios{os.sep}Runner.xcodeproj{os.sep}project.pbxproj.bak",
    )

    shutil.copy2(f"{appIconPath.replace("/", os.sep).replace('..', root)}", 
    f"{root}{os.sep}{project}{os.sep}assets{os.sep}logo{os.sep}logo.png"
    )

    run_command(
            "dart run flutter_launcher_icons:main",
            path=f"{root}{os.sep}{project}",
            silent=True,
    )
    # apaga o arquivo antigo
    os.remove(f"{root}{os.sep}{project}{os.sep}ios{os.sep}Runner.xcodeproj{os.sep}project.pbxproj")
    # volta o backup
    shutil.copy2(
        f"{root}{os.sep}{project}{os.sep}ios{os.sep}Runner.xcodeproj{os.sep}project.pbxproj.bak",
        f"{root}{os.sep}{project}{os.sep}ios{os.sep}Runner.xcodeproj{os.sep}project.pbxproj",
    )
    # apaga o backup
    os.remove(f"{root}{os.sep}{project}{os.sep}ios{os.sep}Runner.xcodeproj{os.sep}project.pbxproj.bak")

def changeSplash(root, appIconPath, color, project="loyalty2_0"):
    with open(
        f"{root}{os.sep}{project}{os.sep}splash.yaml", "r"
    ) as file:
        data = file.read()
        color = color.replace("0xFF", "#").replace("0xff", "#")
        actualIcon = data.split("image: ")[1].split("\n")[0]
        actualColor = data.split("icon_background_color: ")[1].split("\n")[0]
        data = data.replace(f"image: {actualIcon}", f"image: {appIconPath}")
        data = data.replace(f"image_web: {actualIcon}", f"image_web: {appIconPath}")
        data = data.replace(f"icon_background_color: {actualColor}", f"icon_background_color: \"{color}\"")
        data = data.replace(f"color: {actualColor}", f"color: \"{color}\"")
        with open(
            f"{root}{os.sep}{project}{os.sep}splash.yaml", "w"
        ) as file:
            file.write(data)

    run_command(
            "flutter pub run flutter_native_splash:create --path=splash.yaml",
            path=f"{root}{os.sep}{project}",
            silent=True,
    )




def setupEnvFile(flavor, root, project="loyalty2_0"):
    shutil.copy2(f"{root}{os.sep}{project}{os.sep}envs{os.sep}{flavor}.env",
            f"{root}{os.sep}{project}{os.sep}.env",)
    print(f"Setting up .env file for {flavor} flavor, in {project} project :: ")
    print(f"{root}{os.sep}{project}{os.sep}.env")

    run_command(
        "dart run app_env",
        path=f"{root}{os.sep}{project}",
        silent=True,
    )


def getEnv(flavor, root, console, project="loyalty2_0"):
    if "mb_izpay/izpay" in root:
        path = f"{root}{os.sep}envs{os.sep}{flavor}.env"
    else:
        path = f"{root}{os.sep}{project}{os.sep}envs{os.sep}{flavor}.env"

    print(f"Env from {path}...")

    with open(path, "r") as file:
        data = file.read()
        bundleId = data.split("LOYALTY_APP_ID=")[1].split("\n")[0]
        appName = data.split("LOYALTY_APP_NAME_BUILD=")[1].split("\n")[0]
        flavor = flavor
        appIconPath = data.split("LOYALTY_PROJECT_ICON_PATH=")[1].split("\n")[0]
        secondary_color = data.split("LOYALTY_APP_SECONDARY_COLOR=")[1].split("\n")[0].replace("0xFF", "#").replace("0xff", "#")

        table = Table(title="Env File")
        table.add_column("Key", style="green bold", )
        table.add_column("Value")
        table.add_row("Bundle ID", bundleId)
        table.add_row("App Name", appName)
        table.add_row("Flavor", flavor)
        table.add_row("App Icon Path", appIconPath)
        table.add_row("Splash Color", secondary_color)
        console.print(table)
    return flavor, bundleId, appName, appIconPath , secondary_color

def check_and_create_template(path):
    try:
        with open(path, 'r', encoding='utf-8') as template_file:
            template = json.load(template_file)
            if not template.get('parameters'):
                template['parameters'] = {}
    except (FileNotFoundError, json.JSONDecodeError):
        template = {'parameters': {}}
    return template

def setupRemoteConfig(root,environment, console):
    folder_path = f"{root.replace(f"{os.sep}izpay", "")}{os.sep}firebase{os.sep}remote_config"
    template_path = f"{root.replace(f"{os.sep}izpay", "")}{os.sep}remoteconfig.template.json"
    table = Table(title="Updated values")
    table.add_column("Key", style="green bold")
    table.add_column("Value")
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if isinstance(data["envs"][environment], str):
                    # Directly use the string if the JSON data is just a simple string
                    escaped_json_string = data["envs"][environment]
                else:
                    json_string = json.dumps(data["envs"][environment])
                    escaped_json_string = json_string.replace('"', '\"')

                template = check_and_create_template(template_path)
                key_name = filename.split('.')[0]
                if key_name not in template['parameters']:
                    template['parameters'][key_name] = {
                        'defaultValue': {
                            'value': escaped_json_string  # Usar dados do arquivo como valor padrão
                        }
                    }
                else:
                    # Atualizar o valor existente, ou fazer outras operações necessárias
                    template['parameters'][key_name]['defaultValue']['value'] = escaped_json_string
                with open(template_path, 'w', encoding='utf-8') as template_file:
                    json.dump(template, template_file,ensure_ascii=False, indent=4)
                    value = json.dumps(data["envs"][environment], indent=2, separators=(',', ': '))
                    display_json = (value if len(value) < 100 else value[:97] + '<...>')
                    table.add_row(filename, display_json)
    console.print(table)
