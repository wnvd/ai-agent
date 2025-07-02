from functions.get_files_info import get_files_info
from functions.get_file_contents import get_file_contents

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

for wp, file in file_content_check:
    print(f"""Result for {file}
{get_file_contents(wp, file)}
""")
