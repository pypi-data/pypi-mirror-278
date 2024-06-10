from __future__ import annotations

import re

from typing import TYPE_CHECKING

import httpx

from .base import Cooler
from .exceptions import CoolingError


if TYPE_CHECKING:  # pragma: no cover
    from ..models import CoolUrl


class FileCooler(Cooler):
    """
    Download whatever is at the end of the provided URL.
    """

    PRIORITY = 0.5

    # This should match any URL that looks like a file
    HANDLE_REGEX = re.compile(
        r"^(ht|f)tps?://.*\.(?P<suffix>[a-zA-Z0-9]{1,4})(\?.*)?$"
    )
    PROBABLY_PAGES = ("html", "htm", "php", "asp", "aspx")

    def __init__(self, cool_url: CoolUrl) -> None:
        super().__init__(cool_url)

        suffix = cool_url.parsed.path.split(".")[-1]
        name = f"{self.cool_url.hash}.{suffix}"

        self._target_path = self.target_dir / name
        self._target_url = self.target_url / name

    @property
    def remote_markup(self) -> str:
        return self.cool_url.url

    @property
    def local_markup(self) -> str:
        return str(self._target_url)

    @classmethod
    def can_handle(cls, cool_url: CoolUrl) -> bool:
        if m := cls.HANDLE_REGEX.match(cool_url.url):
            return m.group("suffix").lower() not in cls.PROBABLY_PAGES
        return False

    def cool(self) -> None:
        self.prepare_fetch()

        with httpx.stream("GET", self.cool_url.url) as stream:
            if not stream.status_code == httpx.codes.OK:
                self.cool_url.mark_as_failed()
                raise CoolingError(
                    f"Received a response code of {stream.status_code} "
                    f"when attempting to download {self.cool_url.url}"
                )

            with self._target_path.open("wb") as f:
                for data in stream.iter_bytes():
                    f.write(data)

        self.cool_url.mark_as_ready()
