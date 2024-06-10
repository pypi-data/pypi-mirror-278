from __future__ import annotations

import re

from abc import ABC
from typing import TYPE_CHECKING

from django.template.loader import get_template
from django.utils.functional import cached_property
from django.utils.html import format_html

from yt_dlp import YoutubeDL
from yt_dlp.utils import YoutubeDLError

from .base import Cooler


if TYPE_CHECKING:  # pragma: no cover
    from ..models import CoolUrl


class VideoCooler(ABC, Cooler):
    """
    A special kind of cooler, subclasses of this class assume that you intend
    to embed the video at the end of the URL, and so may download multiple
    files to make that work.
    """

    PRIORITY = 0.5

    # Each subclass should define this and each should include a named match
    # for `video_id` so that it can be used in the .video_id property below.
    HANDLE_REGEX = re.compile(r"^$")

    def __init__(self, cool_url: CoolUrl) -> None:
        super().__init__(cool_url)
        self.output_template = self.target_dir / "video.%(ext)s"

    # Property methods --------------------------------------------------------

    @property
    def remote_markup(self) -> str:
        return get_template("cool_urls/videos/remote/default.html").render(
            {"url": self.cool_url.url}
        )

    @property
    def local_markup(self) -> str:
        return get_template("cool_urls/videos/local.html").render(
            {
                "poster": self.poster,
                "webm": self.webm_markup,
                "mp4": self.mp4_markup,
                "origin_url": self.cool_url.url,
                "origin": self.__class__.__name__.replace("Cooler", ""),
            }
        )

    @property
    def poster(self) -> str:
        return str(self.target_url / "video.webp")

    @property
    def webm_markup(self) -> str:
        return self._get_markup_by_format("webm")

    @property
    def mp4_markup(self) -> str:
        return self._get_markup_by_format("mp4")

    @cached_property
    def video_id(self) -> str:
        return self.HANDLE_REGEX.match(self.cool_url.url).group("video_id")

    @classmethod
    def can_handle(cls, cool_url: CoolUrl) -> bool:
        return bool(cls.HANDLE_REGEX.match(cool_url.url))

    # Public methods ----------------------------------------------------------

    def cool(self) -> None:
        if self.cool_url.is_ready:
            self.logger.warning("This video has already been downloaded")
            return

        if self.cool_url.is_processing:
            self.logger.warning(
                "Download of %s already in progress.  "
                "We're not going to try to parallel fetch.",
                self.cool_url.url,
            )
            return

        if self.cool_url.is_failed:
            self.logger.warning(
                "Attempting to fetch %s which failed last time we tried it, "
                "so we're not going to try again.  Clear the `is_failed` "
                "for this URL in the admin to try again.",
                self.cool_url.url,
            )
            return

        self.logger.info("Fetching %s", self.cool_url.url)

        self.prepare_fetch()

        at_least_one_worked = False
        for fmt in ("webm", "mp4"):
            if (self.target_dir / f"video.{fmt}").exists():
                self.logger.warning(
                    "It appears that a %s format of this video was already "
                    "downloaded, so we're not going to try again.  If you "
                    "wish to re-download it, you'll need to call .reset() on "
                    "the CoolURL object for %s",
                    fmt,
                    self.cool_url.url,
                )
                at_least_one_worked = True
                continue

            options = {
                "color": {"stderr": "no_color", "stdout": "no_color"},
                "extract_flat": "discard_in_playlist",
                "format": f"bestvideo[ext={fmt}]+bestaudio[ext={fmt}]/best[ext={fmt}]",  # NOQA: E501
                "fragment_retries": 10,
                "postprocessors": [
                    {
                        "key": "FFmpegConcat",
                        "only_multi_video": True,
                        "when": "playlist",
                    }
                ],
                "retries": 10,
                "writethumbnail": True,
                "quiet": True,
                "outtmpl": self.output_template.absolute().as_posix(),
            }
            try:
                with YoutubeDL(options) as ydl:
                    ydl.download([self.cool_url.url])
                at_least_one_worked = True
                self.logger.info(
                    "Downloading of %s succeeded for format %s",
                    self.cool_url.url,
                    fmt,
                )
            except YoutubeDLError:
                self.logger.warning(
                    "Downloading of %s failed for format %s",
                    self.cool_url.url,
                    fmt,
                )

        if at_least_one_worked:
            self.cool_url.mark_as_ready()
            return

        self.logger.error(
            "All attempts to download %s failed.", self.cool_url.url
        )
        self.cool_url.mark_as_failed()

    # Private methods ---------------------------------------------------------

    def _get_markup_by_format(self, fmt: str) -> str:
        name = f"video.{fmt}"
        path = self.target_dir / name
        if path.exists():
            return format_html(
                '<source src="{}" type="video/{}" />',
                self.target_url / name,
                fmt,
            )
        return ""


class InstagramCooler(VideoCooler):
    HANDLE_REGEX = re.compile(
        r"^https://(www\.)?instagram\.com/[^/]+/reel/(?P<video_id>[^/]+)/?"
    )


class VimeoCooler(VideoCooler):
    HANDLE_REGEX = re.compile(
        r"^https://(www\.)?vimeo\.com/(?P<video_id>\d+)/?"
    )

    @property
    def remote_markup(self) -> str:  # pragma: no cover
        return get_template("cool_urls/videos/remote/vimeo.html").render(
            {"video_id": self.video_id}
        )


class YoutubeCooler(VideoCooler):
    """
    This will embed any standard YouTube video, but *not* the shorts, as they
    apparently don't support embedding.
    """

    HANDLE_REGEX = re.compile(
        r"^https://(www\.)?youtube\.com/watch\?.*\bv=(?P<video_id>[^&]+)"
    )

    @property
    def remote_markup(self) -> str:  # pragma: no cover
        return get_template("cool_urls/videos/remote/youtube.html").render(
            {"video_id": self.video_id}
        )
