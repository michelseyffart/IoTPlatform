from elements.timer import setup_timer, clear_timer
from elements.addons import install_all_addons
from elements.broker import post_broker, delete_broker


def clear_everything():
    clear_timer()
    delete_broker()


def setup_everything():
    post_broker()
    setup_timer()


if __name__ == "__main__":
    install_all_addons()
    setup_everything()
