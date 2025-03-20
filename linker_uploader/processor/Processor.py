from linker_uploader.mapping.mapping_entry import MappingEntry
from abc import ABC, abstractmethod

class Processor(ABC):
    @abstractmethod
    def process(self, mapping: MappingEntry) -> None:
        pass