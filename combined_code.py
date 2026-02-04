# pylint: skip-file
from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Set

# ================== НАСТРОЙКИ ==================


OUTPUT_FILE = "combined_modules.py"

EXCLUDE_DIRS: Set[str] = {
    ".venv",
    "venv",
    ".git",
    ".idea",
    "__pycache__",
    "alembic",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    "dist",
    "build",
    "node_modules",
}


# ===============================================


def to_rel_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def iter_py_files(root: Path, start: Path) -> List[Path]:
    files: List[Path] = []

    if start.is_file():
        return [start] if start.suffix == ".py" else []

    for p in start.rglob("*.py"):
        try:
            rel_parts = p.relative_to(root).parts
        except ValueError:
            continue

        if any(part in EXCLUDE_DIRS for part in rel_parts[:-1]):
            continue

        files.append(p)

    return sorted(files, key=lambda x: x.as_posix())


def ensure_header(file_path: Path, root: Path) -> bool:
    expected = f"# {to_rel_posix(file_path, root)}\n"

    text = file_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines(keepends=True)

    # пустой файл
    if not lines:
        file_path.write_text(expected, encoding="utf-8")
        return True

    # уже есть нужный хедер первой строкой
    if lines[0] == expected:
        return False

    # если первая строка - это такой же "путевой" хедер, но другой (например после перемещения файла),
    # можно заменить её, чтобы не копить несколько хедеров подряд.
    if lines[0].startswith("# ") and lines[0].rstrip().endswith(".py"):
        lines[0] = expected
    else:
        # иначе просто вставляем сверху, ничего не удаляя
        lines.insert(0, expected)

    file_path.write_text("".join(lines), encoding="utf-8")
    return True


def build_combined(py_files: Iterable[Path], out_file: Path) -> None:
    blocks: List[str] = []

    for p in py_files:
        blocks.append(
            p.read_text(encoding="utf-8", errors="replace").rstrip() + "\n"
        )

    out_file.write_text(
        "\n======================\n\n".join(blocks).rstrip() + "\n",
        encoding="utf-8",
    )


def main(path=None) -> None:
    root = Path(__file__).resolve().parent
    script_path = Path(__file__).resolve()
    out_file = root / OUTPUT_FILE

    if path:
        start = (root / path).resolve()
    else:
        start = root

    py_files = iter_py_files(root, start)

    # исключаем сам скрипт и итоговый файл
    py_files = [
        p for p in py_files
        if p.resolve() not in {script_path, out_file.resolve()}
    ]

    changed = 0
    for p in py_files:
        if ensure_header(p, root):
            changed += 1

    build_combined(py_files, out_file)

    print(f"Files processed: {len(py_files)}")
    print(f"Headers updated: {changed}")
    print(f"Combined file:   {out_file.name}")


if __name__ == "__main__":
    # None | "app/ws" | "app/ws/handlers.py"
    # main('app/services')
    main()
