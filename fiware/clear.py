from filip.clients.ngsi_v2.cb import ContextBrokerClient, FiwareHeader, ContextEntity
from filip.clients.ngsi_v2.iota import IoTAClient, ServiceGroup
from requests import Session
import fiware.config.config as fiware_config

url_fiware = fiware_config.get_from_config("url_fiware")
CB_URL = f"http://{url_fiware}:1026"
IOTA_URL = f"http://{url_fiware}:4041"
FIWARE_HEADER = FiwareHeader(service="iotplatform", service_path="/")
s = Session()
cbc = ContextBrokerClient(url=CB_URL, fiware_header=FIWARE_HEADER, session=s)
iota = IoTAClient(url=IOTA_URL, fiware_header=FIWARE_HEADER, session=s)


def clear_entities(type: str):
    entities = cbc.get_entity_list(type_pattern=type)
    cbc.delete_entities(entities)


def clear_devices():
    devices = iota.get_device_list()
    for device in devices:
        iota.delete_device(device_id=device.device_id)


if __name__ == "__main__":
    clear_entities(type="Transaction")
