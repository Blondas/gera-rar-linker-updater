import argparse

from linker_uploader.config.linker_uploader_config import LinkerUploaderConfig, load_config
from linker_uploader.logger.logger_config import configured_logger as logger
from linker_uploader.mapping.mapper import Mapper
from linker_uploader.mapping.mapper_impl import MapperImpl
from linker_uploader.db2.db_connection import DBConnection
from linker_uploader.db2.db2_connection_impl import DB2ConnectionImpl
from linker_uploader.mapping.mapping_entry import MappingEntry
from linker_uploader.linker.linker import Linker
from linker_uploader.linker.linker_impl import LinkerImpl
from linker_uploader.processor.ProcessorImpl import ProcessorImpl


__main__.py

def main():
    try:
        # args = parse_args()
        config: LinkerUploaderConfig = load_config()
        logger.debug(f"config: {config}")
    
        #get mappings
        db2_connection: DBConnection = DB2ConnectionImpl(
            database=config.db_config.database,
            user=config.db_config.user,
            password=config.db_config.password
        )
        mapper: Mapper = MapperImpl(db2_connection, config.payload_mapping_table)
        mappings: list[MappingEntry] = mapper.get_mappings()
        logger.debug(f"mappings: {mappings}")
        
        linker: Linker = LinkerImpl()
        for mapping in mappings:
            ProcessorImpl(
                src_dir_prefix_path=config.src_directory_prefix,
                working_dir=config.output_working_directory,
                linker=linker,
            ).process(mapping)
            
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise e
    
if __name__ == '__main__':
    main()