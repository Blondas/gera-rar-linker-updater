from linker_uploader.mapping.mapping_entry import MappingEntry
from abc import ABC, abstractmethod

class Mapper(ABC):
    @abstractmethod
    def get_mappings(self) -> list[MappingEntry]:
        pass