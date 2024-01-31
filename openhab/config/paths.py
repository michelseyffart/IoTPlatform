from pathlib import Path

path_logs_folder = Path(__file__).parent.parent.parent.joinpath("logs").resolve()
path_config_folder = Path(__file__).parent.resolve()
path_templates_folder = Path(__file__).parent.parent.joinpath("templates").resolve()
path_token = Path(__file__).parent.parent.joinpath("token").resolve()
path_openhab_container_scripts = Path(__file__).parent.parent.joinpath("openhab_container_scripts").resolve()
