import ipih
from pih import A

A.U.packages(("pillow", "numpy"))
from PIL import Image
from io import BytesIO
import numpy as np


class Converter:

    @staticmethod
    def pdf_to_pages_as_image_list(path: str) -> list[Image.Image]:
        from pdf2image import convert_from_path

        return convert_from_path(path)

    @staticmethod
    def image_to_base64(value: Image.Image) -> str | None:
        buffered: BytesIO = BytesIO()
        value.save(buffered, format=A.CT_F_E.JPEG.upper())
        return A.D_CO.bytes_to_base64(buffered.getvalue())

    @staticmethod
    def image_array_to_image(value: np.ndarray) -> Image.Image:
        return Image.fromarray(np.uint8(value)).convert("RGB")
