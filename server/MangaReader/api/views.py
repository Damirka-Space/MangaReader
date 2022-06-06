from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from manga.services import (create_new_manga_object,
                            get_manga_list)
from .serializer import ChapterSerializer


class MangaAPIView(APIView):
    def get(self, request: Request) -> Response:
        manga_list = get_manga_list()
        return Response({'titles': list(manga_list)})

    def post(self, request: Request):
        return Response({
            'message': 'Success',
            'title': create_new_manga_object(
                name=request.data['name'],
                chapters_cnt=request.data['chapters_cnt']
            )
        })


class ChapterAPIView(APIView):
    def post(self, request: Request) -> Response:
        serializer = ChapterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'chapter': serializer.data})
