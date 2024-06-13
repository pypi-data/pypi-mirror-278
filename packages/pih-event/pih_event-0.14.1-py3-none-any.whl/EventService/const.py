import ipih


from pih.consts.hosts import Hosts
from pih.collections.service import ServiceDescription


NAME: str = "Event"

HOST = Hosts.BACKUP_WORKER

VERSION: str = "0.14.1"

CONFIG_FOLDER_NAME: str = "telegram_send_config"

PACKAGES: tuple[str, ...] = ("telegram-send",)

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Log and Event service",
    host=HOST.NAME,
    commands=("send_log_message", "send_event"),
    standalone_name="event",
    use_standalone=True,
    version=VERSION,
    packages=PACKAGES,
)
