from pathlib import Path
from typing import Optional

import yaml
from dataclasses import dataclass

@dataclass
class DbConfig:
    database: str
    user: str
    password: str

@dataclass
class LinkerConfig:
    agid_name_lookup_table: str

@dataclass
class UploaderConfig:
    verify_ssl: bool
    s3_bucket: str
    s3_prefix: str

@dataclass
class LinkerUploaderConfig:
    src_directory_prefix: Path
    payload_mapping_table: str
    output_working_directory: Path
    db_config: DbConfig
    linker_config: LinkerConfig
    uploader_config: UploaderConfig

def load_config(config_path: Optional[str] = None) -> LinkerUploaderConfig:
    if config_path is None:
        config_path = str(Path(__file__).parent.parent / 'resources' / 'linker_uploader_config.yaml')

    with open(config_path) as f:
        yaml_config = yaml.safe_load(f)

    return LinkerUploaderConfig(
        src_directory_prefix=Path(yaml_config['src_directory_prefix']),
        payload_mapping_table=yaml_config['payload_mapping_table'],
        output_working_directory=Path(yaml_config['output_working_directory']),
        db_config=DbConfig(
          database=yaml_config['db_config']['database'],
          user=yaml_config['db_config']['user'],
          password=yaml_config['db_config']['password']
        ),
        linker_config=LinkerConfig(
            agid_name_lookup_table=yaml_config['linker_config']['agid_name_lookup_table']
        ),
        uploader_config=UploaderConfig(
            verify_ssl=yaml_config['uploader_config']['verify_ssl'],
            s3_bucket=yaml_config['uploader_config']['s3_bucket'],
            s3_prefix=yaml_config['uploader_config']['s3_prefix'],
        )
    )