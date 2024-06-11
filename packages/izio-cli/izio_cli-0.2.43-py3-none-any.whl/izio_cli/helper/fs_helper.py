import os


def create_directory(path) -> dict[str, str]:
    """
    Create a directory at a specified path.

    This function attempts to create a directory at the given path. It returns the status of the directory creation.

    Args:
    - path (str): The file system path where the directory should be created.

    Returns:
    - dict: A dictionary with 'directory' indicating the name of the created directory and 'status' showing the result of the operation.
    """

    status = ""
    try:
        os.makedirs(
            path, exist_ok=True
        )  # exist_ok=True impede que um erro seja levantado se o diretório já existir
        status = "Ok"
    except OSError as error:
        status = f"Error: {error}"

    return {"directory": path.split("/")[-1], "status": status}


def create_file(path, filename, payload: str = "") -> dict[str, str]:
    """
    Create a file with specified content at a given path.

    This function creates a file with the provided filename and writes the given payload to it. It returns the status of the file creation.

    Args:
    - path (str): The file system path where the file should be created.
    - filename (str): The name of the file to be created.
    - payload (str, optional): The content to be written to the file.

    Returns:
    - dict: A dictionary with 'file' indicating the name of the created file and 'status' showing the result of the operation.
    """

    status = ""
    try:
        with open(f"{path}/{filename}", "w") as file:
            file.write(payload)
        status = "Ok"
    except OSError as error:
        status = f"Error: {error}"

    return {"file": filename, "status": status}
