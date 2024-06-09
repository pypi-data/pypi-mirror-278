from __future__ import annotations
import abc
import re
import sys

if sys.version_info < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self


class Parsable:
    @staticmethod
    @abc.abstractmethod
    def pattern() -> "re.Pattern[str]": ...

    @classmethod
    def from_str(cls, text: "str") -> "list[Self]":
        return [cls(**m.groupdict()) for m in cls.pattern().finditer(text)]

    @classmethod
    def from_str_or_default(
        cls, text: "str", default: "Self | None" = None
    ) -> "Self | None":
        """return first from the string or some default"""
        res = cls.from_str(text)
        if len(res) == 0:
            return default
        return res[0]
