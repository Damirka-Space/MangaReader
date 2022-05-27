from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from manga.servises import (create_new_manga_object, get_manga_chapter,
                            get_manga_list)


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
    def get(self, request: Request) -> Response:
        return Response({
            'message': 'to be implemented',
            'chapter':  get_manga_chapter(
                name=request.data['name'],
                volume_serial=request.data['volume_serial'],
                chapter_serial=request.data['chapter_serial'],
            ),
        })
