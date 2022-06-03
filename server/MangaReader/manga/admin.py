from django.contrib import admin

from .models import Chapter, MangaSource, Manga, Volume, Frame

admin.site.register((Chapter, Manga, Volume, MangaSource, Frame))
