from pih.collections.service import ServiceDescription
from pih.consts.hosts import Hosts

NAME: str = "Docs"

EXCEL_TITLE_MAX_LENGTH: int = 31


class GKEEP_USER_LINK:
    LOGIN: str = "GKEEP_USER_LOGIN"
    PASSWORD: str = "GKEEP_USER_PASSWORD"


class INVENTORY:
    NAME_COLUMN_NAME: str = "наименование, назначение и краткая характеристика объекта"
    NUMBER_COLUMN_NAME: str = "инвентарный"
    QUANTITY_COLUMN_NAME: str = "фактическое наличие"
    NAME_MAX_LENTH: int = 120
    QUANTITY_NOT_SET: str = "-"


HOST = Hosts.DC2

VERSION: str = "0.17.4"

PACKAGES: tuple[str, ...] = (
    "xlsxwriter",
    "xlrd",
    "xlutils",
    "openpyxl",
    "python-barcode",
    "pillow",
    "qrcode",
    "docx-mailmerge",
    "gkeepapi",
    "numpy",
    "ipywidgets",
    "kaleido",
    "plotly",
)

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Documents service",
    host=HOST.NAME,
    commands=(
        "get_invetory_report",
        "create_user_document",
        "save_time_tracking_report",
        "create_barcodes_for_inventory",
        "create_barcode_for_polibase_person",
        "create_qr_code",
        "check_inventory_report",
        "save_inventory_report_item",
        "close_inventory_report",
        "create_note",
        "get_note",
        "create_statistics_chart",
        "get_note_list_by_label",
        "save_xlsx",
    ),
    standalone_name="doc",
    use_standalone=True,
    version=VERSION,
    packages=PACKAGES,
)
