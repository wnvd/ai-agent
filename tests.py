from functions.get_files_info import get_files_info


dir_check = [
    ("calculator", "."),
    ("calculator", "pkg"),
    ("calculator", "/bin"),
    ("calculator", "../")
]

for wp, dir in dir_check:
    print(f"""Result for current directory:
{get_files_info(wp, dir)}
""")
