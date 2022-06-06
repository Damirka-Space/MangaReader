from django.http import FileResponse
# from django.core.wsgi import

from .service import get_chapter_in_pdf


def chapter_view(request, manga_name: str,
                 volume_serial: int, chapter_serial: int) -> FileResponse:
    return FileResponse(get_chapter_in_pdf(
        manga_name, volume_serial, chapter_serial),
        content_type='application/pdf')
