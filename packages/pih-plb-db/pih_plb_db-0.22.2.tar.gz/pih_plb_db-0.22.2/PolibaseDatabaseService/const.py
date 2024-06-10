import ipih

from pih import A
from pih.consts import CONST
from pih.collections.service import ServiceDescription

NAME: str = "PolibaseDatabase"

HOST = A.CT_H.POLIBASE

VERSION: str = "0.22.2"


SD: ServiceDescription = ServiceDescription(
    name=NAME,
    host=HOST.NAME,
    description="Polibase database service",
    commands=("create_polibase_database_backup",),
    version=VERSION,
    use_standalone=True,
    standalone_name="plb_db",
    host_changeable=False,
    run_from_system_account=True,
    python_executable_path=CONST.UNKNOWN_VALUE,
)

TEST_NAME: str = "test"
STUB_DIRECTORY_NAME: str = "stub"
#
POLIBASE_NAME: str = "Polibase"
ARCHIVE_TYPE: str = A.CT_F_E.ARCHIVE

class DATABASE_DUMP:
    FILE_NAME: str = "DatabaseDump"
    RESULT_FILE_NAME: str = "IN"
    FILE_EXTENSION: str = "DMP"
