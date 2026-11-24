"""Regression tests for explicit missing inputs to ``lateralus fmt``."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def _run_fmt(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    return subprocess.run(
        [sys.executable, "-m", "lateralus_lang", "fmt", *args],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )


def test_check_missing_explicit_file_fails(tmp_path: Path) -> None:
    missing = tmp_path / "missing.ltl"
    result = _run_fmt("--check", str(missing))
    assert result.returncode != 0
    assert f"File not found: {missing}" in result.stderr


def test_check_reports_missing_file_when_mixed_with_valid_file(tmp_path: Path) -> None:
    existing = tmp_path / "good.ltl"
    existing.write_text("let value = 42\n", encoding="utf-8")
    missing = tmp_path / "missing.ltl"
    result = _run_fmt("--check", str(existing), str(missing))
    assert result.returncode != 0
    assert f"File not found: {missing}" in result.stderr
    assert "All files are properly formatted." not in result.stdout


def test_check_existing_file_keeps_success_status(tmp_path: Path) -> None:
    existing = tmp_path / "good.ltl"
    existing.write_text("let value = 42\n", encoding="utf-8")
    result = _run_fmt("--check", str(existing))
    assert result.returncode == 0
    assert "All files are properly formatted." in result.stdout
