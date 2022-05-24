from rest_framework import serializers

from manga.models import Manga


class MangaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manga
        fields = ('name', 'chapters_cnt')
