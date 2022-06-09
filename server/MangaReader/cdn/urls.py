from django.urls import path

from . import views


urlpatterns = [
    path('img/<int:img_id>', views.image_view)
]
