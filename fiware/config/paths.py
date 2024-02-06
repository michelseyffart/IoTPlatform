from pathlib import Path

path_fiware_templates_folder = Path(__file__).parent.parent.joinpath("templates").resolve()
path_config_file = Path(__file__).parent.joinpath("config.json").resolve()
