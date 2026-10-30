import sys
import os
import site


def is_in_virtual_environment() -> bool:
    return sys.prefix != sys.base_prefix


def get_venv_name() -> str | None:
    if sys.prefix == sys.base_prefix and "CONDA_PREFIX" not in os.environ:
        return None

    if "CONDA_DEFAULT_ENV" in os.environ:
        return os.environ["CONDA_DEFAULT_ENV"]

    return os.path.basename(sys.prefix)


def get_packages_folder_venv() -> str:
    if sys.prefix == sys.base_prefix:
        return ""
    try:
        folders = site.getsitepackages()
        return folders[0] if folders else ""
    except Exception:
        return ""


if is_in_virtual_environment():
    print(f"""LABORATORY STATUS: The laboratory is sealed

Current Python: {sys.executable}
Virtual Environment: {get_venv_name()}
Environment Path: {sys.prefix}

SUCCESS: You are working in an isolated environment!
Safe to install reagents without affecting the global system.

Reagent installation path: {get_packages_folder_venv()}""")

else:
    print(f"""LABORATORY STATUS: You are working in the open

Current Python: {sys.executable}
Virtual Environment: None detected

WARNING: You are in the global environment!
Every reagent you install here leaks into
the whole system.

To seal the laboratory, run:
python3 -m venv lab_env source
source lab_env/bin/activate # On Unix
lab_env\\Scripts\\activate # On Windows

Then run this program again.""")
