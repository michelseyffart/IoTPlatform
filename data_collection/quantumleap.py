import pickle

from filip.clients.ngsi_v2.quantumleap import QuantumLeapClient, FiwareHeader
from requests import Session
import logs.create_logger as logs
import logging
import fiware.config.config as fiware_config


def save_data(data: dict, filename: str):
    with open(f"rawdata_quantumleap/{filename}", "wb") as f:
        pickle.dump(data, f)


def save_bids_and_transactions(scenario_name: str):
    qlc = QuantumLeapInterface()
    bid_entities = qlc.get_entities(type="Bid")
    bids = dict()
    for bid_entity in bid_entities:
        bids[bid_entity.entityId] = qlc.get_values(id=bid_entity.entityId)
    save_data(data=bids, filename=f"bids_{scenario_name}")
    transaction_entities = qlc.get_entities(type="Transaction")
    transactions = dict()
    for transaction_entity in transaction_entities:
        transactions[transaction_entity.entityId] = qlc.get_values(id=transaction_entity.entityId)
    save_data(data=bids, filename=f"transactions_{scenario_name}")


class QuantumLeapInterface:

    def __init__(self):
        url_fiware = fiware_config.get_from_config("url_fiware")
        self.QL_URL = f"http://{url_fiware}:8668"
        self.FIWARE_HEADER = FiwareHeader(service="iotplatform", service_path="/")
        self.s = Session()
        self.qlc = QuantumLeapClient(url=self.QL_URL, fiware_header=self.FIWARE_HEADER, session=self.s)
        self.log = logs.get_logger(filename="fiware_interface.log", name="fiware interface", consolelevel=logging.INFO)

    def get_values(self, id: str):
        try:
            return self.qlc.get_entity_values_by_id(entity_id=id, limit=1000000)
        except AssertionError as e:
            print(f"AssertionError at {id}: {e}")
            return None

    def get_entities(self, type: str):
        return self.qlc.get_entities(entity_type=type)


if __name__ == "__main__":
    save_bids_and_transactions(scenario_name="all_data")
