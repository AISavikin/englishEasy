import os
import fnmatch
from datetime import datetime
import mimetypes


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


def ask_int(prompt, default=0):
    value = input(f"{prompt} [{default}]: ").strip()
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        print(f"Некорректное число, используется значение по умолчанию: {default}")
        return default


def get_language_from_extension(filename):
    """Определяет язык программирования по расширению файла"""
    extension_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.java': 'java',
        '.c': 'c',
        '.cpp': 'cpp',
        '.h': 'c',
        '.hpp': 'cpp',
        '.cs': 'csharp',
        '.go': 'go',
        '.rs': 'rust',
        '.rb': 'ruby',
        '.php': 'php',
        '.html': 'html',
        '.htm': 'html',
        '.css': 'css',
        '.scss': 'scss',
        '.sass': 'sass',
        '.less': 'less',
        '.sql': 'sql',
        '.json': 'json',
        '.xml': 'xml',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.toml': 'toml',
        '.ini': 'ini',
        '.cfg': 'ini',
        '.sh': 'bash',
        '.bash': 'bash',
        '.zsh': 'bash',
        '.ps1': 'powershell',
        '.md': 'markdown',
        '.txt': 'text',
        '.csv': 'csv',
        '.tsv': 'tsv',
        '.svg': 'xml',
        '.rst': 'restructuredtext',
        '.tex': 'latex',
        '.r': 'r',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.kts': 'kotlin',
        '.dart': 'dart',
        '.lua': 'lua',
        '.pl': 'perl',
        '.pm': 'perl',
        '.tcl': 'tcl',
        '.vim': 'vim',
        '.dockerfile': 'dockerfile',
        '.env': 'properties',
        '.properties': 'properties',
        '.gitignore': 'gitignore',
        '.dockerignore': 'gitignore',
        '.npmignore': 'gitignore',
    }

    _, ext = os.path.splitext(filename.lower())
    if ext in extension_map:
        return extension_map[ext]

    # Попробуем определить по MIME-типу
    mime_type, _ = mimetypes.guess_type(filename)
    if mime_type:
        if mime_type.startswith('text/'):
            return 'text'
        elif mime_type == 'application/json':
            return 'json'
        elif mime_type == 'application/xml':
            return 'xml'

    return 'text'


def is_binary_file(filepath):
    """Проверяет, является ли файл бинарным"""
    try:
        with open(filepath, 'tr', encoding='utf-8') as f:
            f.read(1024)
        return False
    except:
        return True


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


def collect_files(start_path: str, include_hidden: bool, exclude_masks, max_file_size_mb=1) -> list:
    """Собирает информацию о файлах, возвращает список словарей"""
    files_data = []
    max_size_bytes = max_file_size_mb * 1024 * 1024

    for root, dirs, files in os.walk(start_path):
        if not include_hidden:
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if not f.startswith('.')]

        dirs[:] = [d for d in dirs if not is_excluded(d, exclude_masks)]
        files = [f for f in files if not is_excluded(f, exclude_masks)]

        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, start_path)

            # Проверяем размер файла
            try:
                file_size = os.path.getsize(file_path)
                if file_size > max_size_bytes:
                    print(f"Пропускаем {rel_path} (размер {file_size // 1024}KB > {max_file_size_mb}MB)")
                    continue
            except OSError:
                continue

            # Проверяем, не бинарный ли файл
            if is_binary_file(file_path):
                print(f"Пропускаем бинарный файл: {rel_path}")
                continue

            language = get_language_from_extension(file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                try:
                    with open(file_path, "r", encoding="cp1251") as f:
                        content = f.read()
                except Exception as e:
                    content = f"<<Ошибка чтения файла: {e} (пробовали utf-8 и cp1251)>>"
            except Exception as e:
                content = f"<<Ошибка чтения файла: {e}>>"

            files_data.append({
                "path": rel_path,
                "language": language,
                "content": content,
                "size": file_size
            })

    return files_data


def calculate_tokens_approximate(content):
    """Приблизительный расчет количества токенов (очень грубая оценка)"""
    # Простая эвристика: 1 токен ≈ 4 символа для английского текста
    # Для русского/кода может быть другая пропорция
    chars = len(content)
    words = len(content.split())
    return {
        "chars": chars,
        "words": words,
        "tokens_approx": chars // 4  # Очень грубая оценка
    }


def build_toc(files_data):
    """Создает оглавление с якорными ссылками"""
    toc_lines = ["## 📑 Оглавление файлов\n"]

    for i, file_info in enumerate(files_data, 1):
        anchor = f"file-{i:04d}"
        toc_lines.append(f"{i}. [{file_info['path']}](#{anchor})")

    return "\n".join(toc_lines)


def save_markdown_enhanced(start_path: str, output_file: str, include_hidden: bool, exclude_masks, max_file_size_mb=1):
    """Создает улучшенный Markdown файл"""
    print("Строю дерево проекта...")
    tree = build_tree(start_path, include_hidden, exclude_masks)

    print("Собираю содержимое файлов...")
    files_data = collect_files(start_path, include_hidden, exclude_masks, max_file_size_mb)

    if not files_data:
        print("Предупреждение: не найдено ни одного файла для включения в дамп!")

    # Статистика
    total_files = len(files_data)
    total_chars = sum(f["size"] for f in files_data)
    stats = calculate_tokens_approximate("\n".join([f["content"] for f in files_data]))

    # Метаданные
    metadata = f"""# 📁 Дамп проекта: {os.path.basename(os.path.abspath(start_path))}

## 📊 Метаданные

- **Дата создания:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Исходный путь:** `{os.path.abspath(start_path)}`
- **Включено файлов:** {total_files}
- **Общий размер:** {total_chars // 1024 if total_chars > 1024 else total_chars} {'KB' if total_chars > 1024 else 'bytes'}
- **Приблизительное количество токенов:** {stats['tokens_approx']:,} (оценка)
- **Символов:** {stats['chars']:,}
- **Слов:** {stats['words']:,}
- **Включены скрытые файлы:** {'Да' if include_hidden else 'Нет'}
- **Исключенные маски:** `{', '.join(exclude_masks)}`
- **Максимальный размер файла:** {max_file_size_mb} MB

---
"""

    # Оглавление
    toc = build_toc(
        files_data) if total_files <= 100 else "## 📑 Оглавление файлов\n\n*Оглавление скрыто из-за большого количества файлов (>100)*\n"

    # Содержимое файлов
    files_content = []
    for i, file_info in enumerate(files_data, 1):
        anchor = f"file-{i:04d}"
        file_header = f'\n\n<a id="{anchor}"></a>\n## 📄 `{file_info["path"]}`\n\n'
        file_header += f"**Язык:** `{file_info['language']}`  \n"
        file_header += f"**Размер:** {file_info['size']} bytes\n\n"

        code_block = f"```{file_info['language']}\n{file_info['content']}\n```\n"
        files_content.append(file_header + code_block + "---")

    with open(output_file, "w", encoding="utf-8") as f:
        # Записываем метаданные
        f.write(metadata + "\n")

        # Записываем оглавление
        f.write(toc + "\n\n")

        # Записываем дерево проекта
        f.write("## 🌳 Дерево проекта\n\n")
        f.write("```\n" + tree + "\n```\n\n")
        f.write("---\n\n")

        # Записываем содержимое файлов
        f.write("# 📄 Содержимое файлов\n\n")
        f.write("\n".join(files_content))

    print(f"\n✅ Готово! Улучшенный Markdown сохранён: {output_file}")
    print(f"📊 Статистика: {total_files} файлов, ~{stats['tokens_approx']:,} токенов")


def save_json_alternative(start_path: str, output_file: str, include_hidden: bool, exclude_masks):
    """Альтернатива: сохранение в JSON формате (для машинной обработки)"""
    import json

    print("Собираю данные для JSON...")
    files_data = collect_files(start_path, include_hidden, exclude_masks)

    project_data = {
        "metadata": {
            "project_name": os.path.basename(os.path.abspath(start_path)),
            "created_at": datetime.now().isoformat(),
            "source_path": os.path.abspath(start_path),
            "include_hidden": include_hidden,
            "exclude_masks": exclude_masks,
            "total_files": len(files_data)
        },
        "files": files_data
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(project_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Готово! JSON сохранён: {output_file}")


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════╗
║   🚀 УЛУЧШЕННЫЙ ДАМПЕР ПРОЕКТОВ          ║
║   для LLM и анализа кода                 ║
╚══════════════════════════════════════════╝
    """)

    # Основные параметры
    start_path = ask_path("Введите путь к проекту", ".")
    output_file = ask_path("Введите имя выходного файла", "project_dump.md")
    include_hidden = ask_yes_no("Включать скрытые файлы?")

    # Расширенные настройки
    exclude_masks = ask_list("Маски исключения",
                             "*.pyc, __pycache__, *.sqlite3, migrations, node_modules, .git, .env, *.log, *.tmp, *.temp, *.o, *.obj, *.exe, *.dll, *.so, *.dylib, *.class, *.jar, *.war, *.ear, *.zip, *.tar, *.gz, *.rar, *.7z, *.pdf, *.doc, *.docx, *.xls, *.xlsx, *.ppt, *.pptx, *.jpg, *.jpeg, *.png, *.gif, *.bmp, *.tiff, *.ico, *.mp3, *.mp4, *.avi, *.mov, *.wmv")

    # Выбор формата
    print("\n🎯 Выберите формат вывода:")
    print("  1. Markdown (лучше для LLM, рекомендуемый)")
    print("  2. JSON (лучше для машинной обработки)")

    format_choice = input("Выбор [1]: ").strip()
    if format_choice == "2":
        use_json = True
    else:
        use_json = False

    if not use_json:
        # Дополнительные опции для Markdown
        max_file_size = ask_int("Максимальный размер файла в MB (0 = без ограничений)", 1)

        print("\n" + "=" * 50)
        print("⚙️  Конфигурация Markdown:")
        print(f"   • Путь: {os.path.abspath(start_path)}")
        print(f"   • Выходной файл: {output_file}")
        print(f"   • Скрытые файлы: {'Да' if include_hidden else 'Нет'}")
        print(f"   • Исключения: {exclude_masks}")
        print(f"   • Макс. размер файла: {max_file_size} MB")
        print("=" * 50 + "\n")

        print("Собираю данные...\n")
        save_markdown_enhanced(start_path, output_file, include_hidden, exclude_masks, max_file_size)
    else:
        print("\nСобираю данные в JSON...\n")
        save_json_alternative(start_path, output_file.replace('.md', '.json'), include_hidden, exclude_masks)

    print("\n✨ Дамп успешно создан! Готов к загрузке в LLM.")