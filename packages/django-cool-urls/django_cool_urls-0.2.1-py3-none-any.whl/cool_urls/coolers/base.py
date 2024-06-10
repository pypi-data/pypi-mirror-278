from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Self

from django.conf import settings

from ..logging import Loggable
from .exceptions import NoArchiverAvailableError


if TYPE_CHECKING:  # pragma: no cover
    from ..models import CoolUrl


class Cooler(Loggable):
    """
    While the CoolUrl object contains the state of the cooling process,
    subclasses of this class do the actual work of "cooling" (archiving
    locally) the URL in question.
    """

    PRIORITY: float  # On a scale of 0 (highest) to 1 (lowest)

    DIR = getattr(settings, "COOL_URLS_DIR", "archives")
    MEDIA_ROOT = Path(settings.MEDIA_ROOT) / DIR
    MEDIA_URL = Path(settings.MEDIA_URL) / DIR

    def __init__(self, url: CoolUrl) -> None:
        self.cool_url = url
        self.target_dir = self.MEDIA_ROOT / self.cool_url.hash
        self.target_url = self.MEDIA_URL / self.cool_url.hash

    @property
    def remote_markup(self) -> str:
        """
        How to render this URL when we don't have a local copy.
        """
        raise NotImplementedError()

    @property
    def local_markup(self) -> str:
        """
        How to render this URL when we have a local copy.
        """
        raise NotImplementedError()

    def prepare_fetch(self) -> None:
        self.target_dir.mkdir(parents=True, exist_ok=True)
        self.cool_url.mark_as_processing()

    def cool(self) -> None:
        raise NotImplementedError()

    @classmethod
    def can_handle(cls, cool_url: CoolUrl) -> bool:  # pragma: no cover
        return False

    @classmethod
    def get_subclasses(cls):
        for subclass in cls.__subclasses__():
            yield from subclass.get_subclasses()
            yield subclass

    @classmethod
    def build(cls, cool_url: CoolUrl) -> Self:
        candidates = []
        for klass in cls.get_subclasses():
            if klass.can_handle(cool_url):
                candidates.append(klass)

        if not candidates:  # pragma: no cover
            raise NoArchiverAvailableError(
                f"Can't find an cooler for {cool_url.url}.  This shouldn't be "
                f"possible, since the PageCooler should be the default, so if "
                f"you're seeing this, and you haven't been tinkering with the "
                f".can_handle() methods on the various Cooler classes, please "
                f"report it as a bug."
            )

        return sorted(candidates, key=lambda _: _.PRIORITY)[0](cool_url)
