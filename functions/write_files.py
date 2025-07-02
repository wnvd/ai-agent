import os


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
