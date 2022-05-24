from django.urls import include, path

from . import views


urlpatterns = [
    path('v1/manga_list/', views.MangaAPIView.as_view()),
    path('v1/manga_chapter/', views.ChapterAPIView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
