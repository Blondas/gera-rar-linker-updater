from linker_uploader.linker.linker import Linker
from linker_uploader.processor.Processor import Processor
from linker_uploader.mapping.mapping_entry import MappingEntry
from pathlib import Path
from linker_uploader.logger.logger_config import configured_logger as logger
import uuid
import re

class ProcessorImpl(Processor):
    def __init__(
        self,
        src_dir_prefix_path: Path,
        working_dir: Path,
        linker: Linker
    ):
        self._src_dir_prefix_path: Path = src_dir_prefix_path
        self._working_dir: Path = working_dir
        self._linker: Linker = linker
    
    def process(self, mapping: MappingEntry) -> None:
        logger.info(f"Processing mapping: {mapping}")
        file_path: Path = mapping.src_batch_filename

        target_base_dir: Path = self._create_random_subdir()
        
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
            for line in lines: 
                self._process_single_line(line, mapping, target_base_dir)
                logger.error(f"Error processing line '{line}' in '{file_path}', mapping: {mapping}")
            
        except (IOError, OSError) as e:
            logger.error(f"Failed to read output object names from file {file_path}, error: {str(e)}")
        
    def _process_single_line(self, line: str, mapping: MappingEntry, target_base_dir: Path) -> None:
        logger.info(f"Processing single object: {line}")

        # transform path
        output_object_name: str = self._create_output_object_name(line)
        output_object_name_path: Path = self._create_output_object_name_path(output_object_name)
        output_object: Path = self._create_output_object(output_object_name)
        output_object_path: Path = self._create_output_object_path(output_object, target_base_dir)
        destination_object: Path = self._get_destination_object(
            output_object=output_object, 
            dst_agid_name=mapping.dst_agid_name
        )    
        destination_object_path: Path = self._create_destination_object_path(destination_object, target_base_dir)
        
        #link
        self._linker.create_link(output_object_path, destination_object_path)
        
    @staticmethod
    def _create_output_object_name(line: str):
        ret = line.strip()
        logger.debug(f"output_object_name: {ret}")
        return ret

    def _create_output_object_name_path(self, output_object_name: str):
        ret = self._src_dir_prefix_path / output_object_name
        logger.debug(f"output_object_name_path: {ret}")
        return ret

    @staticmethod
    def _create_output_object(output_object_name: str) -> Path:
        path = Path(output_object_name)
        file = path.name
        ret = path.parent.parent / file
        logger.debug(f"output_object: {ret}")
        return ret
    
    @staticmethod
    def _create_output_object_path(output_object: Path, target_base_dir: Path) -> Path:
        ret = target_base_dir / output_object
        logger.debug(f"output_object_path: {ret}")
        return ret

    def _create_random_subdir(self) -> Path:
        random_name = uuid.uuid4().hex
        subdir_path = self._working_dir / random_name
        subdir_path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"random_subdir: {subdir_path}")
        return subdir_path
    
    @staticmethod
    def _get_destination_object(output_object: Path, dst_agid_name: str) -> Path:
        file: str = output_object.name
        new_parent: Path = output_object.parent.parent / dst_agid_name
        
        match = re.match(r'(\d+)([A-Za-z]{3}).*', file)
        if not match:
            raise ValueError(
                f"Cannot parse path: {output_object}. Expected format: numbers followed by at least 3 letters.")
        subfolder = match.group(1) + match.group(2)
        
        ret = new_parent / subfolder / file
        logger.debug(f"destination_object: {ret}")
        return ret

    @staticmethod
    def _create_destination_object_path(destination_object, target_base_dir) -> Path:
        ret = target_base_dir / destination_object
        logger.debug(f"destination_object_path: {ret}")
        return ret