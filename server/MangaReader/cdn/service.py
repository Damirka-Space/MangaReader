from io import BytesIO

from manga.services.frame import FrameBrowser


def get_image(img_id) -> BytesIO:
    return BytesIO(FrameBrowser.get_by_id(img_id).img)
