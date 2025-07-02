import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

def verbose_output(user_prompt, response):
    print("User prompt:", user_prompt)
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)



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
        model="gemini-2.0-flash-001", contents=messages
    )

    print("")
    print(response.text)
    print("")
    if is_verbose:
        verbose_output(user_prompt, response)

if __name__ == "__main__":
    main()
