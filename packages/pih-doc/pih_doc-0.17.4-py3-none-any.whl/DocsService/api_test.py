import ipih

from pih import A

class GKEEP_USER_LINK:
    LOGIN: str = "GKEEP_USER_LOGIN"
    PASSWORD: str = "GKEEP_USER_PASSWORD"

""" settings = {"module_width": 0.15, "module_height": 3,
            "font_size": 6, "text_distance": 3, "quiet_zone": .5}
DocumentApi.create_barcode(BarCodeData("103310", "Nikita"), "//pih/facade/", "jpeg", settings=settings) """
from gkeepapi import Keep
keep = Keep()
keep.login(
   "it.pacifichosp", "guahtnevyjvthmxb"
)
print(keep.find(labels="Мобильные заметки"))