from pathlib import Path
import sys

from wizlib.handler import Handler
from wizlib.parser import WizParser

INTERACTIVE = sys.stdin.isatty()


class StreamHandler(Handler):

    name = 'stream'
    text: str = ''

    def __init__(self, file=None, stdin=True):
        if file:
            self.text = Path(file).read_text()
        elif stdin and (not INTERACTIVE):
            self.text = sys.stdin.read()

    def __str__(self):
        return self.text

    @classmethod
    def fake(cls, value):
        """Return a fake StreamHandler with forced values, for testing"""
        handler = cls(stdin=False)
        handler.text = value
        return handler
