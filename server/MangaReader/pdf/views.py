from django.http import FileResponse

from .service import get_pdf


def pdf_view(request):
    return FileResponse(get_pdf(), content_type='application/pdf')
