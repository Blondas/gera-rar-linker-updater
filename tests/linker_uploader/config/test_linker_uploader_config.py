from linker_uploader.config.linker_uploader_config import load_config
from pathlib import Path

def test_load_config():
    # Get the project root directory (assuming tests are in a standard location)
    project_root = Path(__file__).parent.parent.parent.parent
    
    config_path = project_root / 'linker_uploader/resources/linker_uploader_config_SAMPLE.yaml'
    
    print()
    print(f'DEBUG: config path: {config_path}')
    assert Path(config_path).exists(), f"Config file not found: {Path(config_path).absolute()}"
    config = load_config(str(config_path))
    print(f'DEBUG: config: {config}')
    assert config is not None
