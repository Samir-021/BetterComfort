#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def _try_reexec_with_venv():
    """Auto-detect local virtual environment if Django is missing from current python."""
    base_dirs = [
        Path(__file__).resolve().parent,
        Path(__file__).resolve().parent.parent,
    ]
    venv_names = ['.venv', 'venv', 'env', 'ENV']
    for b in base_dirs:
        for v in venv_names:
            v_path = b / v
            candidates = [
                v_path / 'Scripts' / 'python.exe',  # Windows
                v_path / 'bin' / 'python',          # Unix / macOS
            ]
            for py_bin in candidates:
                if py_bin.is_file():
                    try:
                        current_exe = os.path.realpath(sys.executable).lower()
                        target_exe = os.path.realpath(str(py_bin)).lower()
                        if current_exe != target_exe:
                            import subprocess
                            code = subprocess.call([str(py_bin)] + sys.argv)
                            sys.exit(code)
                    except Exception:
                        pass


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bettercomfort.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        _try_reexec_with_venv()
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?\n\n"
            "To activate your virtual environment:\n"
            "  Windows PowerShell:  ..\\.venv\\Scripts\\Activate.ps1\n"
            "  Windows CMD:         ..\\.venv\\Scripts\\activate.bat\n"
            "  macOS / Linux:       source ../.venv/bin/activate\n"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
