import pytest

from ..services.chapter import MockedChapter
from ..services.source.mock import MockedMangaSource


chapter = MockedChapter(
    source=MockedMangaSource,
    manga_name='one-piece',
    volume_serial=8,
    serial=71
)


@pytest.mark.django_db
def test_frames_cnt():
    assert chapter.frames_cnt == len(list(chapter.frames))
