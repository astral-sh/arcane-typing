# /// script
# requires-python = ">=3.14"
# dependencies = ["markdown-it-py>=4", "ty>=0.0.101", "typing-extensions>=4.13"]
# ///
"""Run the Markdown tests for `arcane_typing`."""

import argparse
import os
import re
import subprocess
import sys
import tokenize
from collections import Counter
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from time import sleep
from typing import Iterator

from markdown_it import MarkdownIt

PROJECT_ROOT = Path(__file__).resolve().parent
SOURCE_ROOT = PROJECT_ROOT / "src"

ERROR_ASSERTION = re.compile(r"error:\s*\[([\w-]+)\]")
TY_DIAGNOSTIC = re.compile(r"section\.py:(\d+):\d+: \w+\[([\w-]+)\] (.*)")
TY_SUMMARY = re.compile(r"All checks passed!|Found \d+ diagnostics?")

TY_CONFIG = """\
[rules]
undefined-reveal = "ignore"

[terminal]
output-format = "concise"
"""

PYTHON_RUN_SECTION = """\
from runpy import run_path
from sys import argv
from typing import reveal_type

run_path(argv.pop(1), init_globals={"reveal_type": reveal_type}, run_name="__main__")
"""


@dataclass(frozen=True)
class Diagnostic:
    line: int
    code: str
    revealed: str | None = None

    def __str__(self) -> str:
        if self.revealed is not None:
            return f"revealed: {self.revealed}"
        return f"error: [{self.code}]"


def sections(markdown: str) -> Iterator[tuple[str, str]]:
    tokens = MarkdownIt().parse(markdown)
    title = "(document)"
    lines: list[str] = []

    for index, token in enumerate(tokens):
        if token.type == "heading_open" and token.level == 0:
            if lines:
                yield title, "\n".join(lines) + "\n"
                lines = []
            title = tokens[index + 1].content

        if token.type != "fence" or token.map is None:
            continue

        info = token.info.split(maxsplit=1)
        if not info:
            raise ValueError(f"line {token.map[0] + 1}: unlabeled code fence")
        if info[0] not in ("py", "python") or not token.content:
            continue

        # Preserve Markdown line numbers when Python and ty report failures.
        start = token.map[0] + 1
        lines.extend([""] * (start - len(lines)))
        lines.extend(token.content.removesuffix("\n").split("\n"))

    if lines:
        yield title, "\n".join(lines) + "\n"


def expected_diagnostics(source: str) -> Counter[Diagnostic]:
    expected: Counter[Diagnostic] = Counter()
    for token in tokenize.generate_tokens(StringIO(source).readline):
        if token.type != tokenize.COMMENT:
            continue

        comment = token.string[1:].strip()
        kind, separator, detail = comment.partition(":")
        if not separator or kind not in ("error", "revealed"):
            continue

        line, column = token.start
        target_line = line if token.line[:column].strip() else line + 1

        if error := ERROR_ASSERTION.fullmatch(comment):
            diagnostic = Diagnostic(target_line, error[1])
        elif kind == "revealed" and (revealed := detail.strip()):
            diagnostic = Diagnostic(target_line, "revealed-type", revealed)
        else:
            raise ValueError(f"line {line}: invalid assertion {comment!r}")

        expected[diagnostic] += 1

    return expected


def actual_diagnostics(output: str) -> Counter[Diagnostic]:
    actual: Counter[Diagnostic] = Counter()
    for line in output.splitlines():
        if match := TY_DIAGNOSTIC.fullmatch(line):
            line_number, code, message = match.groups()
            revealed = None
            if code == "revealed-type":
                revealed = message.removeprefix("Revealed type: `").removesuffix("`")
            actual[Diagnostic(int(line_number), code, revealed)] += 1
        elif line and not TY_SUMMARY.fullmatch(line):
            raise ValueError(f"unexpected ty output: {line}")

    return actual


def check_section(source: str, markdown_path: Path) -> list[str]:
    failures: list[str] = []
    with TemporaryDirectory() as temporary:
        directory = Path(temporary).resolve()
        script = directory / "section.py"
        script.write_text(source, encoding="utf-8")

        python = subprocess.run(
            [sys.executable, "-c", PYTHON_RUN_SECTION, str(script)],
            cwd=directory,
            env=os.environ | {"PYTHONPATH": str(SOURCE_ROOT)},
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )

        if python.returncode:
            traceback = python.stderr.rstrip().replace(str(script), str(markdown_path))
            failures.append(
                f"Python exited with status {python.returncode}\n{traceback}"
            )

        config_file = directory / "ty.toml"
        config_file.write_text(TY_CONFIG, encoding="utf-8")

        ty_env = os.environ.copy()
        ty_env.pop("TY_OUTPUT_FORMAT", None)

        ty = subprocess.run(
            [
                sys.executable,
                "-m",
                "ty",
                "check",
                "--config-file",
                config_file.name,
                "--color",
                "never",
                "--python",
                sys.executable,
                "--extra-search-path",
                str(SOURCE_ROOT),
                script.name,
            ],
            cwd=directory,
            env=ty_env,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )

        if ty.returncode not in (0, 1) or not ty.stdout:
            failures.append(
                f"ty failed with status {ty.returncode}\n{ty.stderr.rstrip()}"
            )
            return failures

    try:
        expected = expected_diagnostics(source)
        actual = actual_diagnostics(ty.stdout)
    except (SyntaxError, tokenize.TokenError, ValueError) as error:
        failures.append(str(error))
        return failures

    for diagnostic in (expected - actual).elements():
        failures.append(f"{markdown_path}:{diagnostic.line}: missing {diagnostic}")
    for diagnostic in (actual - expected).elements():
        failures.append(f"{markdown_path}:{diagnostic.line}: unexpected {diagnostic}")

    return failures


def discover_files() -> list[Path]:
    return sorted(
        path for path in (PROJECT_ROOT / "tests").rglob("*.md") if path.is_file()
    )


def run_tests(files: list[Path]) -> int:
    total = failed = 0
    invalid = False

    for path in files:
        try:
            file_sections = list(sections(path.read_text(encoding="utf-8")))
        except (OSError, ValueError) as error:
            invalid = True
            print(f"FAIL {path}\n{error}", file=sys.stderr)
            continue

        for title, source in file_sections:
            total += 1
            try:
                failures = check_section(source, path)
            except subprocess.TimeoutExpired as error:
                failures = [str(error)]

            if failures:
                failed += 1
                print(f"FAIL {path} :: {title}", file=sys.stderr)
                print("\n".join(failures), file=sys.stderr)

    if not total:
        if not invalid:
            print("No Python sections found", file=sys.stderr)
        return 1
    print(f"{total - failed}/{total} sections passed", flush=True)
    return int(failed > 0 or invalid)


def snapshot(files: list[Path]) -> dict[Path, tuple[int, int] | None]:
    stamps: dict[Path, tuple[int, int] | None] = {}
    for path in files:
        try:
            stat = path.stat()
        except OSError:
            stamps[path] = None
        else:
            stamps[path] = stat.st_mtime_ns, stat.st_size
    return stamps


def watch_tests(selected: list[Path]) -> int:
    print("Watching Markdown tests (Ctrl-C to stop)", flush=True)
    previous = None
    try:
        while True:
            files = selected or discover_files()
            current = snapshot(files)

            if current != previous:
                if previous is not None:
                    print("\nMarkdown tests changed. Rerunning.", flush=True)
                previous = current
                run_tests(files)

            sleep(0.25)
    except KeyboardInterrupt:
        return 130


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "files",
        metavar="FILE",
        type=Path,
        nargs="*",
        help="Markdown files to run (defaults to all Markdown files under tests/)",
    )
    parser.add_argument(
        "-w", "--watch", action="store_true", help="Rerun when Markdown tests change"
    )

    args = parser.parse_args()
    files: list[Path] = args.files
    if args.watch:
        return watch_tests(files)
    return run_tests(files or discover_files())


if __name__ == "__main__":
    raise SystemExit(main())
