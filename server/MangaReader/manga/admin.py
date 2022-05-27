from django.contrib import admin

from .models import Chapter, MangaSource

admin.site.register((Chapter, MangaSource))
