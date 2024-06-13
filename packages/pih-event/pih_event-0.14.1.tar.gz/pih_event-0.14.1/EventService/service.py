import ipih

from pih import A
from EventService.const import SD
from typing import Any

SC = A.CT_SC

ISOLATED: bool = False


def start(as_standalone: bool = False) -> None:

    if A.U.for_service(SD, as_standalone=as_standalone):

        from pih.tools import ParameterList
        from pih.tools import BitMask as BM
        from EventService.api import LogApi as Api
        from pih.collections import EventDescription
        

        def service_call_handler(sc: SC, pl: ParameterList) -> bool | None:
            if sc == SC.send_log_message:
                Api.send_log_message(
                    pl.next(),
                    pl.next(A.CT_L_ME_CH),
                    pl.next(),
                    pl.next(),
                )
                return True
            elif sc == SC.send_event:
                event: A.CT_E = A.D.get(A.CT_E, pl.next())
                event_description: EventDescription = A.D.get(event)
                event_parameters: dict[str, Any] | None = pl.next()
                event_flags: int | None = pl.next()
                image_path: str | None = pl.next()
                Api.send_log_event(
                    event_description, event_parameters, event_flags, image_path
                )
                event_flags = event_flags or BM.set(event_description.flags) # type: ignore
                save: bool = BM.has(event_flags, A.CT_L_ME_F.SAVE)
                save_once: bool = BM.has(event_flags, A.CT_L_ME_F.SAVE_ONCE)
                if save or save_once:
                    A.A_E.register(event, event_parameters, save_once)
                if BM.has(event_flags, A.CT_L_ME_F.WHATSAPP):
                    pass
                return True
            return None

        A.SRV_A.serve(
            SD,
            service_call_handler,
            isolate=ISOLATED,
            as_standalone=as_standalone,
        )


if __name__ == "__main__":
    start()
