from abc import ABC, abstractmethod
from pathlib import Path


class Linker(ABC):
    @abstractmethod
    def create_link(self, src_path: Path, dst_path: Path) -> None:
        pass