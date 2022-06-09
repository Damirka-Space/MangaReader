from typing import Optional


class IncompleteChapterError(Exception):
    def __init__(self, message: Optional[str] = None) -> None:
        self.message = message

    def __str__(self) -> str:
        if self.message:
            return self.message
        return 'Chapter should contain all frames'
