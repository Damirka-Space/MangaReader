from django.http import FileResponse
from django.core.handlers.wsgi import WSGIRequest

from .service import get_image


def image_view(request: WSGIRequest, img_id: int) -> FileResponse:
    return FileResponse(get_image(img_id))
