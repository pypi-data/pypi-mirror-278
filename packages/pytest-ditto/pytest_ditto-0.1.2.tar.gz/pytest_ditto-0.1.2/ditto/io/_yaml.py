from pathlib import Path
from typing import ClassVar, Any

import yaml


class Yaml:
    extension: ClassVar[str] = "yaml"

    @staticmethod
    def save(data: Any, filepath: Path) -> None:
        with open(filepath, "w") as f:
            yaml.dump(data, f, Dumper=yaml.SafeDumper)

    @staticmethod
    def load(filepath: Path) -> Any:
        with open(filepath, "r") as f:
            return yaml.load(f, Loader=yaml.SafeLoader)
