import os
import shutil
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from functools import partial

# Кількість потоків (можна змінити залежно від навантаження)
MAX_WORKERS = 10


def copy_file(file_path: Path, target_dir: Path):
    ext = file_path.suffix.lower().lstrip('.') or 'no_extension'
    destination_dir = target_dir / ext
    destination_dir.mkdir(parents=True, exist_ok=True)

    base_name = file_path.stem
    suffix = file_path.suffix
    destination_file = destination_dir / (base_name + suffix)

    counter = 1
    # Генерація унікального імені, якщо файл вже існує
    while destination_file.exists():
        destination_file = destination_dir / f"{base_name}_{counter}{suffix}"
        counter += 1

    shutil.copy2(file_path, destination_file)


def process_directory(path: Path, target_dir: Path, executor: ThreadPoolExecutor):
    for item in path.iterdir():
        if item.is_file():
            executor.submit(copy_file, item, target_dir)
        elif item.is_dir():
            executor.submit(process_directory, item, target_dir, executor)


def main():
    if len(sys.argv) < 2:
        print("Usage: python sorter.py <source_dir> [target_dir]")
        sys.exit(1)

    source_dir = Path(sys.argv[1])
    target_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("dist")

    if not source_dir.exists() or not source_dir.is_dir():
        print(f"Source directory '{source_dir}' does not exist or is not a directory.")
        sys.exit(1)

    target_dir.mkdir(parents=True, exist_ok=True)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        process_directory(source_dir, target_dir, executor)


if __name__ == "__main__":
    main()


# Приклад запуску:
# python sorter.py ./picture ./dist