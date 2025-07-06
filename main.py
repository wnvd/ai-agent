import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

from functions.get_files_info import schema_get_files_info
from functions.get_file_contents import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_files import schema_write_python_file

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan.
You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You
do not need to specify the working directory in your function calls as 
it is automatically injected for security reasons.
"""


def verbose_output(user_prompt, response):
    print("User prompt:", user_prompt)
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_python_file,
    ]
)


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    user_prompt = sys.argv[1]
    if len(user_prompt) == 0:
        print("Please enter a prompt, usage python3 main <prompt>")

    is_verbose = False
    if len(sys.argv) >= 3:
        if sys.argv[2] == "--verbose":
            is_verbose = True

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    if is_verbose:
        verbose_output(user_prompt, response)
    print("")
    if not response.function_calls:
        print(response.text)
    print("")
    if response.function_calls is not None:
        for called_function in response.function_calls:
            print(f"Calling function: {
                  called_function.name}({called_function.args})")

if __name__ == "__main__":
    main()
