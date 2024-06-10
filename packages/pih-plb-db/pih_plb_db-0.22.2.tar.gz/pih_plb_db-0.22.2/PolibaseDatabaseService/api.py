import ipih

import os
from pih import A
from pih.tools import j, n, js, esc
from PolibaseDatabaseService.const import *

TEST: bool = False
#


class PolibaseDBApi:

    @staticmethod
    def create_dump(file_name: str | None = None, test: bool | None = None) -> None:
        test = TEST if n(test) else test

        local_polibase_database_dump_folder_name: str = j(
            (POLIBASE_NAME, DATABASE_DUMP.FILE_NAME)
        )
        nas_polibase_database_dump_folder_name: str = A.PTH.join(
            POLIBASE_NAME, DATABASE_DUMP.FILE_NAME
        )
        polibase_folder_path: str = A.PTH.join(
            j(("C", A.CT.SPLITTER)),
            os.sep,
            local_polibase_database_dump_folder_name,
        )

        if test:
            file_name = TEST_NAME
        else:
            if n(file_name):
                file_name = A.D.now_to_string(A.CT_P.DB_DATETIME_FORMAT)

        dump_file_name_result: str = A.PTH.add_extension(
            DATABASE_DUMP.RESULT_FILE_NAME, DATABASE_DUMP.FILE_EXTENSION
        )
        file_database_dump_name_out: str = A.PTH.add_extension(
            file_name, DATABASE_DUMP.FILE_EXTENSION
        )
        if test:
            polibase_folder_path_src: str = polibase_folder_path
            polibase_folder_path = A.PTH.for_windows(
                A.PTH.join(polibase_folder_path, TEST_NAME)
            )
            os.system(
                js(
                    (
                        "robocopy",
                        A.PTH.join(polibase_folder_path_src, STUB_DIRECTORY_NAME),
                        polibase_folder_path,
                        file_database_dump_name_out,
                    )
                )
            )
        polibase2_folder_path: str = A.PTH.for_windows(
            A.PTH.join(A.CT_H.POLIBASE2.NAME, local_polibase_database_dump_folder_name)
        )

        archiver_program_path: str = 'C:/"Program Files"/7-Zip/7z'

        file_out_name = A.PTH.add_extension(file_name, ARCHIVE_TYPE)

        nas_folder_path: str = A.PTH.for_windows(
            A.PTH.join(A.CT_H.NAS.IP, "backups", nas_polibase_database_dump_folder_name)
        )

        nas_copy_command: str = js(
            (
                "robocopy",
                polibase_folder_path,
                (nas_folder_path),
                file_out_name,
                "/J",
            )
        )
        polibase2_copy_command: str = js(
            (
                "robocopy",
                polibase_folder_path,
                (polibase2_folder_path),
                file_database_dump_name_out,
                "/J",
            )
        )
        os.chdir(polibase_folder_path)

        # step 1
        A.E.backup_notify_about_polibase_creation_db_dumb_start(not test)
        if not test:
            os.system(
                j(
                    (
                        "exp userid=POLIBASE/POLIBASE owner=POLIBASE file=",
                        file_database_dump_name_out,
                        " ",
                        "parfile=backpar.txt",
                    )
                )
            )
        A.E.backup_notify_about_polibase_creation_db_dumb_complete(
            os.path.getsize(
                A.PTH.join(polibase_folder_path, file_database_dump_name_out)
            ),
            not test,
        )

        # step 3
        A.E.backup_notify_about_polibase_creation_archived_db_dumb_start()
        archive_creation_parameters: str | None = A.S.get(
            A.CT_S.POLIBASE_DB_DUMP_ARCHIVE_CREATION_PARAMETERS
        )
        password_parameter: str = j(
            (
                "-p",
                (
                    "test"
                    if test
                    else esc(A.D_V_E.value("POLIBASE_DATABASE_ARCHIVE_PASSWORD"))
                ),
            )
        )
        compression_level: int | None = A.S.get(
            A.CT_S.POLIBASE_DB_DUMP_ARCHIVE_COMPRESSION_LEVEL
        )

        os.system(
            js(
                (
                    archiver_program_path,
                    (
                        (
                            js(
                                (
                                    j(("a -t", ARCHIVE_TYPE)),
                                    (
                                        None
                                        if n(compression_level)
                                        else j(
                                            (
                                                "-mx",
                                                compression_level,
                                            )
                                        )
                                    ),
                                    password_parameter,
                                )
                            )
                        )
                        if n(archive_creation_parameters)
                        else js(
                            (
                                archive_creation_parameters,
                                password_parameter,
                            )
                        )
                    ),
                    file_out_name,
                    file_database_dump_name_out,
                )
            )
        )

        A.E.backup_notify_about_polibase_creation_archived_db_dumb_complete(
            os.path.getsize(A.PTH.join(polibase_folder_path, file_out_name)), not test
        )

        # step 4
        A.E.backup_notify_about_polibase_coping_archived_db_dumb_start(
            A.CT_H.NAS.ALIAS
        )
        A.L.debug_bot(j((nas_copy_command, ":", str(os.system(nas_copy_command)))))
        A.E.backup_notify_about_polibase_coping_archived_db_dumb_complete(
            A.CT_H.NAS.ALIAS
        )

        # step 5
        A.E.backup_notify_about_polibase_coping_db_dumb_start(
            A.CT_H.POLIBASE2.ALIAS
        )
        A.L.debug_bot(j((polibase2_copy_command, ":", str(os.system(polibase2_copy_command)))))
        
        A.E.backup_notify_about_polibase_coping_db_dumb_complete(
            A.CT_H.POLIBASE2.ALIAS
        )

        # step 6
        polibase2_previous_file_delete_command: str = js(
            (
                "del",
                A.PTH.for_windows(
                    A.PTH.join(
                        (polibase2_folder_path),
                        os.sep,
                        dump_file_name_result,
                    )
                ),
            )
        )
        polibase_file_rename_command: str = js(
            (
                "ren",
                A.PTH.for_windows(
                    A.PTH.join(
                        (polibase2_folder_path),
                        os.sep,
                        file_database_dump_name_out,
                    )
                ),
                dump_file_name_result,
            )
        )

        os.system(polibase2_previous_file_delete_command)
        os.system(polibase_file_rename_command)
        # step 8
        os.system(js(("del", file_database_dump_name_out)))
        os.system(js(("del", file_out_name)))
