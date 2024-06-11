from dataclasses import dataclass
from functools import cached_property

from cx_core.misc.timepoint import TimePoint


@dataclass(order=True)
class Subtitle:
    start: TimePoint
    end: TimePoint
    content: str

    def __rich__(self):
        return f'''[yellow]{self.start.timestamp} [cyan]-->[/cyan] {self.end.timestamp}[/yellow]\
[cyan] : [/cyan][blue]{self.content}[blue]'''

    @cached_property
    def duration(self):
        return self.end - self.start

    def with_content(self, content):
        return Subtitle(self.start, self.end, content)


class SubtitleProcessor:
    def __init__(self):
        pass

    def __call__(self, subtitle: Subtitle) -> Subtitle:
        return subtitle
