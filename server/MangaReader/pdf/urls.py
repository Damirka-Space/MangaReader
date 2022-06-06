from django.urls import path

from . import views

urlpatterns = [
    path('<str:manga_name>/<int:volume_serial>/<int:chapter_serial>',
         views.chapter_view)
]
