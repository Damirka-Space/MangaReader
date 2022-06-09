from django.http import FileResponse, HttpResponse

from .service import get_image


def image_view(request, img_id: int) -> FileResponse:
    return FileResponse(get_image(img_id))
