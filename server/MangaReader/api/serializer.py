from rest_framework import serializers

from manga.models import Manga
from manga.services import get_manga_chapter


class MangaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manga
        fields = ('name', 'chapters_cnt')


class ChapterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=256)
    source = serializers.JSONField(read_only=True)
    volume_serial = serializers.IntegerField()
    serial = serializers.IntegerField()
    frames_cnt = serializers.IntegerField(read_only=True)
    frames_urls = serializers.ListField(read_only=True)

    def create(self, validated_data: dict) -> None:
        return get_manga_chapter(**validated_data)
