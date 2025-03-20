from dataclasses import dataclass
from linker_uploader.mapping.batch_status import BatchStatus
from pathlib import Path

@dataclass
class MappingEntry:
    src_server_name: str
    src_filespace_name: str
    src_batch_filename: Path
    status: BatchStatus 
    dst_agid_name: str