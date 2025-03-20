from enum import Enum, unique

@unique
class BatchStatus(Enum):
    BATCH_CREATED: int = 1
    BATCH_RETRIEVED: int = 2
    BATCH_ERROR: int = 3

    def __str__(self) -> str:
        return str(self.value)