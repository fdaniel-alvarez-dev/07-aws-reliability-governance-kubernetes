#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import textwrap


def _print_missing_config_and_exit(missing: list[str]) -> None:
    msg = "\n".join(f"- {item}" for item in missing)
    print(
        (
            "Production-mode tests are enabled, but required configuration is missing.\n\n"
            "Fix the following and re-run:\n"
            f"{msg}\n\n"
            "Re-run:\n"
            "  PRODUCTION_TESTS_CONFIRM=1 TEST_MODE=production python3 tests/run_tests.py"
        )
    )
    raise SystemExit(2)


def _run(cmd: list[str], *, cwd: str) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)


def main() -> int:
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mode = os.environ.get("TEST_MODE", "").strip().lower()
    if mode not in {"demo", "production"}:
        print(
            "Missing or invalid TEST_MODE. Set TEST_MODE=demo or TEST_MODE=production.\n"
            "Examples:\n"
            "  TEST_MODE=demo python3 tests/run_tests.py\n"
            "  PRODUCTION_TESTS_CONFIRM=1 TEST_MODE=production python3 tests/run_tests.py"
        )
        return 2

    if mode == "demo":
        _run([sys.executable, "-m", "unittest", "discover", "-s", "tests/unit", "-p", "test_*.py"], cwd=repo_root)
        return 0

    missing: list[str] = []
    if os.environ.get("PRODUCTION_TESTS_CONFIRM") != "1":
        missing.append("PRODUCTION_TESTS_CONFIRM=1 (explicit acknowledgement)")
    if shutil.which("aws") is None:
        missing.append("aws CLI installed and configured (used for real S3 integration tests)")
    if os.environ.get("S3_TEST_BUCKET", "").strip() == "":
        missing.append("S3_TEST_BUCKET (an existing bucket for integration test uploads)")
    if os.environ.get("AWS_REGION", "").strip() == "":
        missing.append("AWS_REGION")

    if missing:
        _print_missing_config_and_exit(missing)

    _run([sys.executable, "-m", "unittest", "discover", "-s", "tests/integration", "-p", "test_*.py"], cwd=repo_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
