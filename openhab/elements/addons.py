from openhab.openhab_interface import openhab_request
from openhab.config.config import *
import openhab.create_logger as logs

log = logs.get_logger(filename="logs//setup.log", name="addons")


def install_addon(addon: str):

    rc = openhab_request(endpoint=f"/addons/{addon}/install", method="POST")
    log.info(f"Installed {addon}: {rc}")


def install_all_addons():
    addons: dict = get_required_addons()
    for key in addons.keys():
        install_addon(addons[key])


if __name__ == "__main__":
    install_all_addons()
