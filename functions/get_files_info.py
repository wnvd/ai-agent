import os
from google.genai import types


def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = ""
    path = os.path.join(working_directory, directory)

    if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(os.path.abspath(path)):
        return f'Error: "{directory}" is not a directory'

    try:
        result = ""
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            file_size = os.path.getsize(item_path) or 0
            is_dir = os.path.isdir(item_path)
            result = result + \
                f'- {item}: file_size={file_size} bytes, is_dir={is_dir}' + '\n'
        return result
    except Exception as e:
        return f"Error listing files: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself."
                ),
        },
    ),
)
