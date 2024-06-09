# Python Parsable Lib

## utilities for quickly structuring text parsing

![test_suite](https://github.com/GregSym/parsable/actions/workflows/test-suite.yml/badge.svg)

### intended for situations where full-blown ast parsing is unnecessary


```python
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
    
@dataclass
class Coordinates(Parsable):
    x: float
    y: float

    @staticmethod
    def pattern() -> "re.Pattern[str]":
        return re.compile(
            r"\"coordinates\":\s*\[\s*(?P<x>\d+(?:\.\d+)?)\,\s*(?P<y>\d+(?:\.\d+)?)\,?\s*\]"
        )

coordinates = Coordinates.from_str(EXAMPLE_TEXT)
print(coordinates)

```

which outputs:
```output
>>> [Coordinates(x=14.95685, y=69.91848)]
```

This particular functionality exploits the named capture groups feature in the version of regex used by python (available in many other typical implementations) to structure the desired data into a dataclass output that can be worked with easily for other tasks.
