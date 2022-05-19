from rest_framework import viewsets

from .serializer import MangaSerializer
from .models import Manga


class MangaViewSet(viewsets.ModelViewSet):
    queryset = Manga.objects.all().order_by('name')
    serializer_class = MangaSerializer
