from functions.get_files_info import get_files_info
from functions.get_file_contents import get_file_contents
from functions.write_files import write_files
from functions.run_python import run_python_file

# checks for dir children
dir_check = [
    ("calculator", "."),
    ("calculator", "pkg"),
    ("calculator", "/bin"),
    ("calculator", "../")
]

# for wp, dir in dir_check:
#     print(f"""Result for current directory:
# {get_files_info(wp, dir)}
# """)


# Check for file content
file_content_check = [
    ("calculator", "main.py"),
    ("calculator", "pkg/calculator.py"),
    ("calculator", "/bin/cat/"),
]

# for wp, file in file_content_check:
#     print(f"""Result for {file}
# {get_file_contents(wp, file)}
# """)

# Check for file writes
file_write_check = [
    ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
    ("calculator", "pkg.morelorem.txt", "lorem ipsum dolor sit amet"),
    ("calculator", "/tmp/temp.txt", "this should not be allowed"),
]

# for wp, file, content in file_write_check:
#     print(f"""Result for {file}
# {write_files(wp, file, content)}
# """)

# check for call python of file

run_file = [
    ("calculator", "main.py"),
    ("calculator", "tests.py"),
    ("calculator", "../main.py"),
    ("calculator", "nonexistent.py"),
]

# for wp, file in run_file:
#     print(f"""Result for {file}
# {run_python_file(wp, file)}
# """)

# check for if LLM knows about file structure (manually)
# uv run main.py "what files are in the root?",
# uv run main.py "What files are in the pkg directory?",
