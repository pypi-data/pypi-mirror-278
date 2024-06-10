from __future__ import annotations

from shutil import which
from subprocess import DEVNULL, PIPE, Popen, run
from typing import TYPE_CHECKING

from .base import Cooler
from .exceptions import CoolingError


if TYPE_CHECKING:  # pragma: no cover
    from ..models import CoolUrl


class PageCooler(Cooler):
    """
    For web pages, this cooler attempts to serialise an entire page (js, css,
    images, and all) into one great big `index.html` file.
    """

    PRIORITY = 1.0

    def __init__(self, cool_url: CoolUrl) -> None:
        super().__init__(cool_url)

        self._target_path = self.target_dir / "index.html"
        self._target_url = self.target_url / "index.html"

        self._monolith = which("monolith")
        self._chromium = which("chromium")

    @property
    def remote_markup(self) -> str:
        return self.cool_url.url

    @property
    def local_markup(self) -> str:
        return str(self._target_url)

    @property
    def monolith_options(self) -> tuple[str, ...]:
        return (
            "--isolate",
            f"--base-url={self.cool_url.url}",
            f"--output={self._target_path}",
            "--no-audio",
            "--no-video",
        )

    @classmethod
    def can_handle(cls, cool_url: CoolUrl) -> bool:
        return True

    def cool(self) -> None:
        self.prepare_fetch()

        if self._target_path.exists():
            self.logger.warning(
                "Page has already been cooled at %s.  Exiting.",
                self._target_path,
            )
            self.cool_url.mark_as_ready()
            return

        if not self._monolith:
            raise CoolingError(
                "Cannot find monolith.  Please install it and make sure it's "
                "in your ${PATH} to continue."
            )

        if not self._chromium:
            self.logger.warning(
                "Chromium wasn't found, so we're going to continue without "
                "it.  For most pages, this should work fine, but for any page "
                "that's largely Javascript rendered at runtime, this will "
                "probably not come out the way you'd expect.  Installing "
                "Chromium should fix that though."
            )
            return self._cool_without_chromium()

        return self._cool_with_chromium()

    def _cool_with_chromium(self) -> None:
        """
        chromium --headless --incognito --dump-dom ${URL} \
          | monolith - -I -b ${URL} -o index.html -av
        """
        chromium_command = (
            self._chromium,
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--headless",
            "--incognito",
            "--dump-dom",
            self.cool_url.url,
        )
        monolith_command = (self._monolith, "-") + self.monolith_options
        process = Popen(
            monolith_command,
            stdin=Popen(chromium_command, stdout=PIPE, stderr=DEVNULL).stdout,
            stderr=PIPE,
            stdout=PIPE,
        )

        process.wait()
        if process.returncode != 0:
            c1 = " ".join(chromium_command)
            c2 = " ".join(monolith_command)
            self.cool_url.mark_as_failed()
            raise CoolingError(
                f"URL cooling failed.  "
                f"The command was: `{c1} | {c2}`\n"
                f"The the stdout was: {process.stdout.read().decode()}\n"
                f"The the stderr was: {process.stderr.read().decode()}\n"
            )

        self.cool_url.mark_as_ready()

    def _cool_without_chromium(self) -> None:
        """
        monolith - -I -b ${URL} -o index.html -av
        """
        cmd = (self._monolith, self.cool_url.url) + self.monolith_options
        process = run(cmd)
        if process.returncode != 0:
            self.cool_url.mark_as_failed()
            raise CoolingError(
                f"URL cooling failed.  "
                f"The command was: `{' '.join(cmd)}` "
                f"The the stdout was: {process.stdout.decode()}\n"
                f"The the stderr was: {process.stderr.decode()}\n"
            )

        self.cool_url.mark_as_ready()
