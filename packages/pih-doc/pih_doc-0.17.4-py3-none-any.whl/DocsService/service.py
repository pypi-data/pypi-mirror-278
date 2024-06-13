import ipih

from pih import A
from typing import Any
from DocsService.const import SD

SC = A.CT_SC

ISOLATED: bool = False


def start(as_standalone: bool = False) -> None:

    if A.U.for_service(SD, as_standalone=as_standalone):
        from datetime import date
        import grpc
        from DocsService.api import DocumentApi
        from pih.tools import ParameterList, nnt
        from pih.consts.errors import IncorrectInputFile
        from pih.collections import FullName, LoginPasswordPair, Result, Note

        api: DocumentApi = DocumentApi(ISOLATED)

        def service_call_handler(sc: SC, pl: ParameterList, context) -> Any:
            if sc == SC.create_statistics_chart:
                return api.create_statistics_chart(pl.next())
            if sc == SC.create_user_document:
                path: str = pl.next()
                date_value: str = pl.next()
                web_site_name: str = pl.next()
                web_site: str = pl.next()
                email_address: str = pl.next()
                full_name: FullName = pl.next(FullName())
                tab_number: str = pl.next()
                pc: LoginPasswordPair = pl.next(LoginPasswordPair())
                polibase: LoginPasswordPair = pl.next(LoginPasswordPair())
                email: LoginPasswordPair = pl.next(LoginPasswordPair())
                return api.create_user_document(
                    path,
                    date_value,
                    web_site_name,
                    web_site,
                    email_address,
                    full_name,
                    tab_number,
                    pc,
                    polibase,
                    email,
                )
            if sc == SC.save_time_tracking_report:
                path: str = pl.next()                
                start_date: date = nnt(A.D.date_from_string(pl.next()))
                end_date: date = nnt(A.D.date_from_string(pl.next()))
                tab_number: list[str] = pl.next()
                plain_format: bool = pl.next()
                return api.save_time_tracking_report(
                    A.R_TT.create(start_date, end_date, tab_number), path, plain_format
                )
            if sc == SC.create_barcodes_for_inventory:
                try:
                    return api.create_inventory_barcodes(pl.next(), pl.next())
                except IncorrectInputFile:
                    return A.ER.rpc(
                        context, code=grpc.StatusCode.INVALID_ARGUMENT
                    )
            if sc == SC.create_barcode_for_polibase_person:
                person_pin: int = pl.next()
                A.PTH.make_directory_if_not_exists(A.PTH_P.person_folder(person_pin))
                return api.create_barcode_for_polibase_person(person_pin, pl.next())
            if sc == SC.check_inventory_report:
                return api.inventory_report_columns_is_exists(pl.next())
            if sc == SC.get_inventory_report:
                return Result(
                    A.CT_FC.INRENTORY.ITEM,
                    api.inventory_report(pl.next(), pl.next()),
                )
            if sc == SC.save_inventory_report_item:
                return api.save_inventory_report_item(pl.next(), pl.next())
            if sc == SC.drop_note_cache:
                api.drop_note_cache()
                return True
            if sc == SC.close_inventory_report:
                return api.close_inventory_report(pl.next())
            if sc == SC.create_qr_code:
                return api.create_qr_code(
                    pl.next(),
                    pl.next(),
                    pl.next(),
                    pl.next(),
                )
            if sc == SC.save_xlsx:
                return api.save_xlsx(
                    pl.next(),
                    pl.next(),
                    pl.next(),
                    pl.next(),
                )
            if sc == SC.create_note:
                note: Note = pl.next(Note())
                return api.create_note(
                    note,
                    pl.next(),
                    pl.next(),
                    pl.next(),
                )
            if sc == SC.get_note:
                return A.R.pack(
                    A.CT_FC.VALUE,
                    api.get_note(pl.next(), pl.next()),
                )
            if sc == SC.get_note_list_by_label:
                return A.R.pack(
                    A.CT_FC.VALUE,
                    api.get_notes_by_label(pl.next(), pl.next()),
                )

        def service_starts_handler() -> None:
            A.SRV_A.subscribe_on(A.CT_SC.heart_beat)
            for type in A.CT_STAT.Types:
                if type == A.CT_STAT.Types.CT:
                    continue
                name: str = A.D.get(type)
                if not A.PTH.exists(A.PTH.STATISTICS.get_file_path(name)):
                    api.create_statistics_chart(name)

        A.SRV_A.serve(
            SD,
            service_call_handler,
            service_starts_handler,
            isolate=ISOLATED,
            as_standalone=as_standalone,
        )

if __name__ == "__main__":
    start()