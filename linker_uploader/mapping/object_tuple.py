from pathlib import Path
from dataclasses import dataclass

@dataclass
class ObjectTuple:
    output_object_name: str
    output_object_name_path: Path
    output_object_path: Path
    target_base_dir: Path
    output_object_target_path: Path
    