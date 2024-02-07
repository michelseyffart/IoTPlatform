from pathlib import Path

path_logs_folder = Path(__file__).parent.parent.parent.joinpath("logs").resolve()
path_config_folder = Path(__file__).parent.resolve()
path_templates_folder = Path(__file__).parent.parent.joinpath("templates").resolve()
path_token = Path(__file__).parent.parent.joinpath("token").resolve()
path_openhab_container_scripts = Path(__file__).parent.parent.joinpath("openhab_container_scripts").resolve()
path_data_collection = Path(__file__).parent.parent.parent.joinpath("data_collection").resolve()
path_rawdata_MQTT_folder = path_data_collection.joinpath("rawdata_MQTT").resolve()
path_rawdata_python_folder = path_data_collection.joinpath("rawdata_python").resolve()
path_secondary_disk = Path("J:/BA/Python/Auswertungsdaten")
