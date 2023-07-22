"""Models for RSS responses."""

from __future__ import annotations

from dataclasses import dataclass
from email.utils import parsedate_to_datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import sys
    from datetime import datetime

    if sys.version_info >= (3, 11):
        from typing import Self
    else:
        from typing_extensions import Self


@dataclass(frozen=True)
class RSSPackageMetadata:
    """RSS Package metadata."""

    title: str
    version: str | None
    package_link: str
    guid: str | None
    description: str | None
    author: str | None
    publication_date: datetime

    @classmethod
    def build_from(cls: type[Self], data: dict[str, str]) -> RSSPackageMetadata:
        """Build an instance from raw data."""
        split_title = data.get("title").removesuffix(" added to PyPI").split()
        title = split_title[0]
        version = split_title[1] if len(split_title) == 2 else None  # noqa: PLR2004 - is not magic

        publication_date = parsedate_to_datetime(data.get("pubDate")) if data.get("pubDate") is not None else None

        return cls(
            title=title,
            version=version,
            package_link=data.get("link"),
            guid=data.get("guid"),
            description=data.get("description"),
            author=data.get("author"),
            publication_date=publication_date,
        )
