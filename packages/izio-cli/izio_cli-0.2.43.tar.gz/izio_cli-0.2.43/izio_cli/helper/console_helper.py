import os
import subprocess

from rich.table import Table


def create_table(data_dict) -> Table:
    table = Table()

    # Adicionando cabeçalhos
    for header in data_dict.keys():
        table.add_column(header)

    # Encontrando o número de linhas (baseado no item mais longo)
    num_rows = max(len(values) for values in data_dict.values())

    # Adicionando linhas
    for i in range(num_rows):
        row = [
            f"{"[green]:heavy_check_mark:" if data_dict[key][i] == "Ok" else f"[red]{data_dict[key][i]}"}" if key == "status" else f"[bold blink dark_green]{data_dict[key][i]}" if i < len(data_dict[key]) else "" for key in data_dict
        ]
        table.add_row(*row)

    return table

def run_command(command, path=os.getcwd(), silent=False):
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
            cwd=path,
            shell=True,
        )
        if not silent:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error: {e.stderr}")
    
def updateGradle(root, bundleId, appName, project="loyalty2_0"):
    # remove strings file with os if exists
    if os.path.exists(f"{root}{os.sep}{project}{os.sep}android{os.sep}app{os.sep}src{os.sep}prod{os.sep}res{os.sep}values{os.sep}strings.xml"):
        os.remove(f"{root}{os.sep}{project}{os.sep}android{os.sep}app{os.sep}src{os.sep}prod{os.sep}res{os.sep}values{os.sep}strings.xml")
        
    with open(f"{root}{os.sep}{project}{os.sep}android{os.sep}app{os.sep}build.gradle", "r") as file:
        data = file.read()
        # get prod productFlavor
        prd = data.split("prod {")[1].split("}")[0]
        actualFlavor = prd.split("applicationId ")[1].split('"')[1]
        data = data.replace(
            f'applicationId "{actualFlavor}"', f'applicationId "{bundleId}"'
        )
        actualName = prd.split('resValue "string", "app_name", ')[1].split('"')[1]
        data = data.replace(
            f'resValue "string", "app_name", "{actualName}"',
            f'resValue "string", "app_name", "{appName.replace('"', "")}"',
        )
        with open(f"{root}{os.sep}{project}{os.sep}android{os.sep}app{os.sep}build.gradle", "w") as file:
            file.write(data)
