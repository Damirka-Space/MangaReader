from rest_framework import serializers

from .models import Manga


class MangaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Manga
        fields = ('name', 'chapters_cnt')
