import os
import fnmatch

def ask_path(prompt, default="."):
    value = input(f"{prompt} [{default}]: ").strip()
    return value if value else default

def ask_yes_no(prompt, default="n"):
    value = input(f"{prompt} (y/n) [{default}]: ").strip().lower()
    if value == "":
        value = default
    return value == "y"

def ask_list(prompt, default=""):
    value = input(f"{prompt} (через запятую) [{default}]: ").strip()
    if not value:
        value = default
    return [v.strip() for v in value.split(",") if v.strip()]

def is_excluded(path: str, exclude_masks):
    filename = os.path.basename(path)
    for mask in exclude_masks:
        if fnmatch.fnmatch(filename, mask):
            return True
    return False

def build_tree(start_path: str, include_hidden: bool, exclude_masks) -> str:
    tree_lines = []

    for root, dirs, files in os.walk(start_path):
        if not include_hidden:
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if not f.startswith('.')]

        dirs[:] = [d for d in dirs if not is_excluded(d, exclude_masks)]
        files = [f for f in files if not is_excluded(f, exclude_masks)]

        level = root.replace(start_path, "").count(os.sep)
        indent = "    " * level
        tree_lines.append(f"{indent}- {os.path.basename(root)}/")

        sub_indent = "    " * (level + 1)
        for file in files:
            tree_lines.append(f"{sub_indent}- {file}")

    return "\n".join(tree_lines)

def collect_files(start_path: str, include_hidden: bool, exclude_masks) -> str:
    combined = []

    for root, dirs, files in os.walk(start_path):
        if not include_hidden:
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if not f.startswith('.')]

        dirs[:] = [d for d in dirs if not is_excluded(d, exclude_masks)]
        files = [f for f in files if not is_excluded(f, exclude_masks)]

        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), start_path)
            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                content = f"<<Ошибка чтения файла: {e}>>"

            combined.append(
                f"## `{rel_path}`\n\n"
                f"```text\n{content}\n```\n"
                f"---\n\n"
            )

    return "".join(combined)

def save_markdown(start_path: str, output_file: str, include_hidden: bool, exclude_masks):
    tree = build_tree(start_path, include_hidden, exclude_masks)
    files_content = collect_files(start_path, include_hidden, exclude_masks)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# 📁 Дерево проекта\n\n")
        f.write("```\n" + tree + "\n```\n\n")
        f.write("# 📄 Содержимое файлов\n\n")
        f.write(files_content)

    print(f"\nГотово! Markdown сохранён: {output_file}")

if __name__ == "__main__":
    print("=== Проектовый дампер в Markdown ===\n")

    start_path = ask_path("Введите путь к проекту", ".")
    output_file = ask_path("Введите имя выходного файла", "project_dump.md")
    include_hidden = ask_yes_no("Включать скрытые файлы?")
    exclude_masks = ask_list("Маски исключения", "*.pyc, __pycache__, *.sqlite3, migrations")

    print("\nСобираю данные...\n")
    save_markdown(start_path, output_file, include_hidden, exclude_masks)