"""
Caution: Do not import any UI dependencies in this file.
This file is used to validate the UI dependencies.
If you import any UI dependencies in this file, the validation will fail to execute.
"""

import importlib.metadata
from typing import Any

PACKAGE_NAME = "lastmile-eval"
UI_EXTRA = "ui"


def validate_ui_dependencies():
    metadata = importlib.metadata.metadata(PACKAGE_NAME)
    requires_dist = metadata.get_all("Requires-Dist", [])

    # See pyproject.toml for the definition of the UI extra.
    ui_dependencies = [
        dep.split(";")[0].strip().split(" ")[0]
        for dep in requires_dist
        if f"extra == '{UI_EXTRA}'" in dep
    ]

    missing_dependencies: list[Any] = []
    for dependency in ui_dependencies:
        try:
            # Check if package is installed, NOT if module is importable.
            importlib.metadata.version(dependency)
        except ImportError:
            missing_dependencies.append(dependency)

    if missing_dependencies:
        raise ModuleNotFoundError(
            f"Missing UI dependencies: {', '.join(missing_dependencies)}\n"
            f"Please install them with the following command (make sure to include the quotes): "
            f'pip install "lastmile-eval[ui]"'
        )
