import argparse
from linker_uploader.logger.logger_config import configured_logger as logger
from pathlib import Path

from linker_uploader.mapping.batch_status import BatchStatus
from linker_uploader.mapping.mapping_entry import MappingEntry
from linker_uploader.linker.linker import Linker
from linker_uploader.linker.linker_impl import LinkerImpl
from linker_uploader.processor.ProcessorImpl import ProcessorImpl


def parse_args():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--src-directory-prefix', type=str, required=True, help='Source directory')
    parser.add_argument('--output-directory-', type=str, required=True, help='Output working directory')
    parser.add_argument('--db-src-tsm-server-name', type=str, required=True, help='vmigpayld_mapping.src_tsm_server_name')
    parser.add_argument('--db-src-tsm-filespace-name', type=str, required=True, help='vmigpayld_mapping.src_tsm_filespace_name')
    parser.add_argument('--db-src-tsm-batch-filename', type=str, required=True, help='vmigpayld_mapping.src_tsm_batch_filename')
    parser.add_argument('--db-status', type=str, required=True, help='vmigpayld_mapping.status')
    parser.add_argument('--dst-agid-name', type=str, required=True, help='vmigpayld_mapping.dst_agid_name')
    return parser.parse_args()

def main():
    try:
        args = parse_args()
        
        #config
        output_working_directory: Path = Path(args.output_directory)
        src_directory_prefix: Path = Path(args.src_directory_prefix)
        
        # db row
        db_src_tsm_server_name: str = args.db_src_tsm_server_name
        db_src_tsm_filespace_name: str = args.db_src_tsm_filespace_name
        db_src_tsm_batch_filename: Path = Path(args.db_src_tsm_batch_filename)
        db_status: str = args.db_status
        db_dst_agid_name: str = args.db_dst_agid_name
        
        linker: Linker = LinkerImpl()
        ProcessorImpl(
            src_dir_prefix_path=src_directory_prefix,
            working_dir=output_working_directory,
            linker=linker,
        ).process(MappingEntry(
            src_server_name=db_src_tsm_server_name,
            src_filespace_name=db_src_tsm_filespace_name,
            src_batch_filename=db_src_tsm_batch_filename,
            status=BatchStatus[db_status],
            dst_agid_name=db_dst_agid_name
        ))
            
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise e
    
if __name__ == '__main__':
    main()