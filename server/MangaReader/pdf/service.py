from io import BytesIO
from fpdf import FPDF
from PIL import Image

from manga.services.chapter import Chapter
from manga.services.source import ReadYagami, MangaLib


chapter_test = Chapter(
    source=ReadYagami,
    manga_name='tokyo_ghoul',
    volume_serial=1,
    serial=1
)


def get_pdf():
    pdf = FPDF()

    # for url in chapter_test.get_frame_urls():
    #     print('download to pdf ' + url)
    #     try:
    #         img_raw = requests.get(url).content
    #         img = Image.open(BytesIO(img_raw))
    #         width, height = img.size
    #     except:
    #         continue

    for frame in chapter_test.get_frames():
        img = Image.open(BytesIO(frame))
        width, height = img.size

        pdf.add_page(format=(width, height))
        pdf.image(img,
                  x=0, y=0,
                  w=width, h=height)

    return BytesIO(pdf.output())
