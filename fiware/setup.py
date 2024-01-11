from fiware.config.paths import path_fiware_templates_folder
from filip.clients.ngsi_v2.cb import ContextBrokerClient, FiwareHeader, ContextEntity
import json
from requests import Session


#CB_URL = "http://137.226.248.250:1026"
#IOTA_URL = "http://137.226.248.250:4041"
#FIWARE_HEADER = FiwareHeader(service="iotplatform", service_path="/")
#s = Session()
#cbc = ContextBrokerClient(url=CB_URL, fiware_header=FIWARE_HEADER, session=s)


def post_entity_transaction(building: int, cbc: ContextBrokerClient):
    with open(path_fiware_templates_folder / "entity_transaction.json") as f:
        entity_transaction_template = f.read()
    entity_transaction = entity_transaction_template.replace("BUILDING_ID", str(building))
    entity_transaction = json.loads(entity_transaction)
    entity = ContextEntity(**entity_transaction)
    cbc.post_entity(entity=entity, update=True)


def post_entity_auction_iteration(building: int, cbc: ContextBrokerClient):
    with open(path_fiware_templates_folder / "entity_auction_iteration.json") as f:
        entity_auction_iteration_template = f.read()
    entity_auction_iteration = entity_auction_iteration_template.replace("BUILDING_ID", str(building))
    entity_auction_iteration = json.loads(entity_auction_iteration)
    entity = ContextEntity(**entity_auction_iteration)
    cbc.post_entity(entity=entity, update=True)


def post_entity_public_info(cbc: ContextBrokerClient):
    with open(path_fiware_templates_folder / "entity_public_info.json") as f:
        entity_public_info = json.load(f)
    entity = ContextEntity(**entity_public_info)
    cbc.post_entity(entity=entity, update=True)
