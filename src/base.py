from dataclasses import dataclass
from datetime import datetime


@dataclass
class Instant:
    id: str
    value: datetime
    start: bool = False
    end: bool = False

    def __str__(self) -> str:
        if self.start:
            return f"start {self.id}"
        elif self.end:
            return f"end {self.id}"
        else:
            return self.id


@dataclass
class Relation:
    source: Instant
    target: Instant

    @property
    def value(self):
        if self.source.value < self.target.value:
            return "<"
        elif self.source.value > self.target.value:
            return ">"
        else:
            return "="

    def to_dict(self):
        return {
            "source": str(self.source),
            "target": str(self.target),
            "relation": self.value,
        }
