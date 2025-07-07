import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_contents import schema_get_file_content, get_file_contents
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_files import schema_write_python_file, write_files

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

available_function_dic = {
    "get_files_info": get_files_info,
    "get_file_contents": get_file_contents,
    "run_python_file": run_python_file,
    "write_files": write_files,
}


def generate_content(client, messages, user_prompt, is_verbose):
    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
            ),
        )

        # iterating response.condidates and appending
        # messages list for AI context
        if response.candidates is not None:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if is_verbose:
            verbose_output(user_prompt, response)

        if not response.function_calls:
            print(f"\n{response.text}\n")
            break

        if response.function_calls is not None:
            for function_call in response.function_calls:
                function_call_result = called_function(
                    function_call, is_verbose)

                # appending type.Content to messages list for AI context
                messages.append(function_call_result)

                if function_call_result is None:
                    raise Exception(f"result from called function is None")
                if is_verbose:
                    print(
                        f"-> {function_call_result.parts[0].function_response.response}")
        else:
            print(f"\n{response.text}\n")
            break


def called_function(function_call_part, is_verbose):

    function_name = function_call_part.name
    function_args = function_call_part.args

    if is_verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    if function_name not in available_function_dic:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    working_directory = "./calculator"
    function_result = available_function_dic[function_name](
        working_directory, **function_args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
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

    generate_content(client, messages, user_prompt, is_verbose)


if __name__ == "__main__":
    main()
