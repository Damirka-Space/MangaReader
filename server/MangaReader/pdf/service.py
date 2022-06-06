from io import BytesIO
from fpdf import FPDF
from PIL import Image

from manga.services.chapter import Chapter
from manga.services.source import ReadYagami, MangaLib


def get_chapter_in_pdf(manga_name: str, volume_serial: int,
                       serial: int) -> BytesIO:
    pdf = FPDF()

    chapter = Chapter(
        source=MangaLib,
        manga_name=manga_name,
        volume_serial=volume_serial,
        serial=serial
    )

    for frame in chapter.get_frame_images():
        img = Image.open(BytesIO(frame))
        width, height = img.size

        pdf.add_page(format=(width, height))
        pdf.image(img,
                  x=0, y=0,
                  w=width, h=height)

    return BytesIO(pdf.output())
