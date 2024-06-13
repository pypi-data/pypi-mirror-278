import ipih


def start() -> None:
    from EventService.service import start

    start(True)


if __name__ == "__main__":
    start()
