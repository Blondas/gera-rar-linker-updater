from linker_uploader.linker.linker import Linker
from pathlib import Path
from linker_uploader.logger.logger_config import configured_logger as logger

class LinkerImpl(Linker):
    
    def create_link(self, src_path: Path, dst_path: Path) -> None:
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        if not src_path.exists():
            msg = f"Source path does not exist: {src_path}"
            logger.error(msg)
            raise FileNotFoundError(msg)
        if dst_path.exists():
            msg = f"Destination path already exists, source path: {src_path}, destination path: {dst_path}"
            logger.error(msg)
            raise FileExistsError(msg)
        
        src_path.hardlink_to(dst_path)
        logger.debug(f"Hardlink Created, {src_path} <- {dst_path}")