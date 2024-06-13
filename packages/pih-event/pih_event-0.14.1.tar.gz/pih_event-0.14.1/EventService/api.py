import telegram_send
from time import sleep
from datetime import datetime
from typing import Any, Callable

import ipih

from pih import A, PIHThreadPoolExecutor
from pih.collections import EventDescription
from EventService.const import CONFIG_FOLDER_NAME, SD
from pih.tools import BitMask as BM, js, n, nn, ne, nns
from pih.consts import LogMessageFlags, LogMessageChannels


message_send_executor: PIHThreadPoolExecutor = PIHThreadPoolExecutor(1)


class MST:
    timestamp: datetime | None = None
    last_success_timestamp: datetime | None = None
    count: int = 0
    time_wait: float | None = None


class LogApi:
    @staticmethod
    def send(
        message: str,
        log_message_channel: LogMessageChannels | None = LogMessageChannels.DEFAULT,
        flags_value: int = 0,
        image_path: str | None = None,
    ) -> None:
        def message_decoration_for_log_level(message: str, log_level_value: int) -> str:
            if BM.has(log_level_value, LogMessageFlags.ERROR):
                message = js(("Error:", message))
            if BM.has(log_level_value, LogMessageFlags.TASK):
                message = js(("Задача:", message))
            if BM.has(log_level_value, LogMessageFlags.ALERT):
                message = js(("Внимание:", message))
            return message

        log_message_channel = log_message_channel or LogMessageChannels.DEFAULT
        flags_value = flags_value or A.D.get(LogMessageFlags.DEFAULT)
        config: str = A.PTH.join(
            A.PTH_FCD.SERVICE_FILES(nns(SD.standalone_name)),
            CONFIG_FOLDER_NAME,
            A.PTH.add_extension(log_message_channel.name.lower(), "conf"),
        )

        def internal_send(
            message: str, flags_value: int = 0, image_path: str | None = None
        ) -> None:
            delta: float | None = (
                None
                if n(MST.last_success_timestamp)
                else (A.D.now() - MST.last_success_timestamp).total_seconds()  # type: ignore
            )
            if n(MST.time_wait):
                if n(MST.timestamp):
                    MST.timestamp = A.D.now()
                    MST.count = 0
            else:
                if nn(delta):
                    if delta < MST.time_wait:  # type: ignore
                        sleep(MST.time_wait - delta)  # type: ignore
                        if n(MST.timestamp):
                            MST.timestamp = A.D.now()
                            MST.count = 0
            while True:
                try:
                    if n(image_path):
                        telegram_send.send(
                            messages=[
                                message_decoration_for_log_level(message, flags_value)
                            ],
                            conf=config,
                        )
                    else:
                        with open(image_path, "rb") as image_file:  # type: ignore
                            telegram_send.send(
                                images=[image_file],
                                captions=[
                                    message_decoration_for_log_level(
                                        message, flags_value
                                    )
                                ],
                                conf=config,
                            )
                    MST.count += 1
                    MST.last_success_timestamp = A.D.now()
                    break
                except TimeoutError:
                    sleep(1.0)
                    continue
                except Exception as error:
                    time_wait: float = (
                        1.1 * int(A.D_Ex.decimal(error.message)) / (MST.count - 1)  # type: ignore
                    )
                    if n(MST.time_wait):
                        MST.time_wait = time_wait
                    else:
                        MST.time_wait = max(MST.time_wait, time_wait)  # type: ignore
                    MST.timestamp = None
                    sleep(A.D_Ex.decimal(error.message))  # type: ignore

        message_send_executor.submit(internal_send, message, flags_value, image_path)

    @staticmethod
    def send_log_message(
        message: str,
        log_message_channel: LogMessageChannels = LogMessageChannels.DEFAULT,
        flags_value: int = 0,
        image_path: str | None = None,
    ) -> bool:
        LogApi.send(message, log_message_channel, flags_value, image_path)
        return True

    @staticmethod
    def send_log_event(
        event_description: EventDescription,
        parameters: dict[str, Any] | None = None,
        flags: int | None = None,
        image_path: str | None = None,
    ) -> bool:
        channel: LogMessageChannels = event_description.channel  # type: ignore
        flags = flags or A.D.as_bitmask_value(event_description.flags)  # type: ignore
        if not BM.has(flags, LogMessageFlags.SILENCE):
            message: str | Callable[[dict[str, Any]], str] = event_description.message  # type: ignore
            if callable(message):
                message = A.D.as_value(message, parameters)
            if ne(parameters):
                if (
                    message.count("{}")
                    + len(
                        A.D.filter(
                            lambda item: not item.visible, event_description.params
                        )
                    )
                ) == len(
                    parameters
                ):  # type: ignore
                    message = message.format(*A.D.to_list(parameters))  # type: ignore
                else:
                    print(message, parameters)
                    message = message.format(**parameters)  # type: ignore
            LogApi.send(message, channel, flags, image_path)  # type: ignore
        return True
