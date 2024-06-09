from __future__ import annotations
from dataclasses import dataclass
import re
import sys
from parsable import Parsable, ParsableCollection


EXAMPLE_TEXT = """

{
  "border": "{{int(1, 5)}}px {{random(solid, dotted, dashed)}} {{color()}}",
  "coordinates": {
    "type": "array",
    "count": 2,
    "items": "{{float(0, 120, 5)}}"
  },
  "password": "xX{{animal()}}-{{string(6, 10, *)}}"
}

{
  "border": "2px dashed gray",
  "coordinates": [
    14.95685,
    69.91848
  ],
  "password": "xXearthworm-*******"
}

"""


def test_basics() -> None:
    @dataclass
    class Coordinates(Parsable):
        x: float
        y: float

        @staticmethod
        def pattern() -> "re.Pattern[str]":
            return re.compile(
                r"\"coordinates\":\s*\[\s*(?P<x>\d+(?:\.\d+)?)\,\s*(?P<y>\d+(?:\.\d+)?)\,?\s*\]"
            )

        def __post_init__(self) -> None:
            self.x = float(self.x) if isinstance(self.x, str) else self.x
            self.y = float(self.y) if isinstance(self.y, str) else self.y

    coordinates = Coordinates.from_str(EXAMPLE_TEXT)

    assert len(coordinates) == 1
    assert coordinates[0].x == 14.95685
    assert coordinates[0].y == 69.91848

    if sys.version_info < (3, 9):
        to_inherit = ParsableCollection
    else:
        to_inherit = ParsableCollection[Coordinates]

    class CoordinatesCollection(to_inherit):
        @staticmethod
        def runtime_type() -> "type[Coordinates]":
            return Coordinates

    coordinates_alt = CoordinatesCollection.from_str(EXAMPLE_TEXT)
    assert len(coordinates_alt) == 1
    assert coordinates_alt[0].x == 14.95685
    assert coordinates_alt[0].y == 69.91848
