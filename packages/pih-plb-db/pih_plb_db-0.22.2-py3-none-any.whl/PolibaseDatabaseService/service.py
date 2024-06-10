import ipih

from pih import A
from PolibaseDatabaseService.const import SD

SC = A.CT_SC

ISOLATED: bool = False

def start(as_standalone: bool = False) -> None:

    from pih import PIHThread
    from pih.tools import ParameterList
    from PolibaseDatabaseService.api import PolibaseDBApi as Api
    
    from typing import Any

    def service_call_handler(sc: SC, pl: ParameterList) -> Any:
        if sc == SC.create_polibase_database_backup:
            PIHThread(
                lambda file_name, test: Api.create_dump(file_name, test),
                args=(pl.next(), pl.next()),
            )
        if sc == SC.heart_beat:
            if A.C_P_DB.creation_start_time(A.D_Ex.parameter_list(pl).get()):
                Api.create_dump()
        return True

    def service_starts_handler() -> None:
        A.SRV_A.subscribe_on(SC.heart_beat, name="Polibase database backup")

    A.SRV_A.serve(
        SD,
        service_call_handler,
        service_starts_handler,
        isolate=ISOLATED,
        as_standalone=as_standalone,
    )


if __name__ == "__main__":
    start()
