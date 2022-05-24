from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from manga.servises import get_manga_list, create_new_manga_object


class MangaAPIView(APIView):
    def get(self, request: Request) -> Response:
        manga_list = get_manga_list()
        return Response({'titles': list(manga_list)})

    def post(self, request: Request):
        return Response({'status': 'Success',
                         'title': create_new_manga_object(
                             name=request.data['name'],
                             chapters_cnt=request.data['chapters_cnt'])})
