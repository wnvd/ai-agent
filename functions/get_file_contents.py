import os
from google.genai import types

MAX_CHARACTERS = 10000


def get_file_contents(workding_directory, file_path):
    allowed_path = os.path.abspath(workding_directory)
    path = os.path.join(workding_directory, file_path)

    if not os.path.abspath(path).startswith(allowed_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(os.path.abspath(path)):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(os.path.abspath(path)) as f:
            content = f.read(MAX_CHARACTERS)
            if os.path.getsize(os.path.abspath(path)) > MAX_CHARACTERS:
                content += (
                    f'[...File "{
                        file_path}" truncated at ({MAX_CHARACTERS}) characters"]'
                )
            return content
    except Exception as e:
        return f'Error: {e}'


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_contents",
    description="Lists content inside the specified file along, also truncates the file if maximum characters inside the file exceed 10000 and notifies user by append the content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory is where the file is, it is relative and if not provided the file is inside the current working directory."
            )
        },
    )
)
