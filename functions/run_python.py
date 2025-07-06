import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file):
    allowed_path = os.path.abspath(working_directory)
    file_path = os.path.abspath(os.path.join(working_directory, file))

    if not file_path.startswith(allowed_path):
        return f'Error: Cannot execute "{file}" as it is outside the permitted working directory'

    if not os.path.exists(file_path):
        return f'Error: File "{file}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: File "{file}" not found.'

    try:
        cmd = subprocess.run(
            ["python3", file_path],
            cwd=allowed_path,
            capture_output=True,
            timeout=30,
        )

        result_output = ""
        stdout = f'STDOUT: {cmd.stdout}'
        stderr = f'STDERR: {cmd.stderr}'
        result_output = f'{stdout}\n{stderr}\n'

        if cmd.check_returncode() != 0:
            result_output = result_output + '\n' + \
                f'Process exited with code {cmd.returncode}'

        if len(result_output) == 0:
            return "No output produced"

        return result_output

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the python file whose name is specifed in the provided workding directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
         "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
         ),
            "args": types.Schema(
             type=types.Type.ARRAY,
             items=types.Schema(
                 type=types.Type.STRING,
                 description="Optional arguments to pass to the Python file.",
             ),
             description="Optional arguments to pass to the Python file.",
         ),
        },
    )
)
