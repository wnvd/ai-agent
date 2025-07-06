import os
from google.genai import types


def write_files(working_directory, file_path, content):
    allowed_path = os.path.abspath(working_directory)
    path = os.path.join(working_directory, file_path)

    if not os.path.abspath(path).startswith(allowed_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        with open(os.path.abspath(path), "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'


schema_write_python_file = types.FunctionDeclaration(
    name="write_files",
    description="writes into the python file whose name is specifed in the provided workding directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file where content parameter needs to be written into"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content that needs to be written inside the file whose path is provided"
            )
        },
    )
)
