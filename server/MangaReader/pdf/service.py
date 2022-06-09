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

    for frame in chapter.frames:
        img = Image.open(BytesIO(frame.img))

        pdf.add_page(format=img.size)
        pdf.image(img,
                  x=0, y=0,
                  w=img.width, h=img.height)

    return BytesIO(pdf.output())
