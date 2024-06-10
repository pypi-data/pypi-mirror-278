from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from yt_dlp.utils import YoutubeDLError

from ...coolers.videos import VideoCooler
from ...models import CoolUrl


class VideoCoolerTestCase(TestCase):
    def test_remote_markup(self):
        cu = CoolUrl.objects.create(url="https://youtube.com/watch?v=test")
        self.assertEqual(
            VideoCooler(cu).remote_markup.strip(),
            '<p>Waiting on download of <a href="https://youtube.com/watch?v=test">https://youtube.com/watch?v=test</a></p>',  # NOQA: E501
        )

    def test_local_markup(self):
        url = "https://youtube.com/watch?v=test"
        hsh = "d3569d4e77d39b5c28e6111206653718"
        cu = CoolUrl.objects.create(url=url)

        with TemporaryDirectory() as d:
            d = Path(d)

            target_dir = d / hsh
            target_dir.mkdir(parents=True)

            webm = target_dir / "video.webm"
            webm.touch()

            webp = target_dir / "video.webp"
            webp.touch()

            with patch("cool_urls.coolers.videos.VideoCooler.MEDIA_ROOT", d):
                cooler = VideoCooler(cu)
                self.assertIn(f"{hsh}/video.webp", cooler.local_markup)
                self.assertIn(f"{hsh}/video.webm", cooler.local_markup)
                self.assertNotIn(f"{hsh}/video.mp4", cooler.local_markup)

            mp4 = target_dir / "video.mp4"
            mp4.touch()

            with patch("cool_urls.coolers.videos.VideoCooler.MEDIA_ROOT", d):
                cooler = VideoCooler(cu)
                self.assertIn(f"{hsh}/video.webp", cooler.local_markup)
                self.assertIn(f"{hsh}/video.webm", cooler.local_markup)
                self.assertIn(f"{hsh}/video.mp4", cooler.local_markup)

    @patch("cool_urls.coolers.videos.YoutubeDL")
    def test_cool_already_cooled(self, m):
        cooler = VideoCooler(
            CoolUrl.objects.create(
                url="https://youtube.com/watch?v=test",
                is_ready=True,
                archived_at=timezone.now(),
            )
        )
        with patch.object(VideoCooler.logger, "warning") as lg:
            cooler.cool()
            self.assertEqual(lg.call_count, 1)
            self.assertIn("already been downloaded", lg.call_args[0][0])
        self.assertEqual(m.call_count, 0)

    @patch("cool_urls.coolers.videos.YoutubeDL")
    def test_cool_is_already_processing(self, m):
        cooler = VideoCooler(
            CoolUrl.objects.create(
                url="https://youtube.com/watch?v=test",
                is_processing=True,
            )
        )
        with patch.object(VideoCooler.logger, "warning") as lg:
            cooler.cool()
            self.assertEqual(lg.call_count, 1)
            self.assertIn("already in progress", lg.call_args[0][0])
        self.assertEqual(m.call_count, 0)

    @patch("cool_urls.coolers.videos.YoutubeDL")
    def test_cool_is_already_failed(self, m):
        cooler = VideoCooler(
            CoolUrl.objects.create(
                url="https://youtube.com/watch?v=test",
                is_failed=True,
            )
        )
        with patch.object(VideoCooler.logger, "warning") as lg:
            cooler.cool()
            self.assertEqual(lg.call_count, 1)
            self.assertIn("failed last time", lg.call_args[0][0])
        self.assertEqual(m.call_count, 0)

    @patch("cool_urls.coolers.videos.YoutubeDL")
    def test_cool_is_already_downloaded(self, m):
        url = "https://youtube.com/watch?v=test"
        hsh = "d3569d4e77d39b5c28e6111206653718"
        cu = CoolUrl.objects.create(url=url)

        with TemporaryDirectory() as d:
            d = Path(d)

            target_dir = d / hsh
            target_dir.mkdir(parents=True)

            webm = target_dir / "video.webm"
            webm.touch()

            with patch("cool_urls.coolers.videos.VideoCooler.MEDIA_ROOT", d):
                cooler = VideoCooler(cu)
                with patch.object(VideoCooler.logger, "warning") as lg:
                    cooler.cool()
                    self.assertEqual(lg.call_count, 1)

            self.assertEqual(
                m.call_count,
                1,
                "We should only try to download the mp4 version as the webm "
                "version should be detected locally.",
            )

            cu.refresh_from_db()
            self.assertTrue(cu.is_ready)
            self.assertFalse(cu.is_processing)
            self.assertFalse(cu.is_failed)
            self.assertIsNotNone(cu.archived_at)

    @patch("cool_urls.coolers.videos.YoutubeDL")
    def test_cool_success(self, m):
        url = "https://youtube.com/watch?v=test"
        hsh = "d3569d4e77d39b5c28e6111206653718"
        cu = CoolUrl.objects.create(url=url)

        with TemporaryDirectory() as d:
            d = Path(d)
            with patch("cool_urls.coolers.videos.VideoCooler.MEDIA_ROOT", d):
                cooler = VideoCooler(cu)
                cooler.cool()

            self.assertEqual(m.call_count, 2)
            self.assertEqual(
                m.call_args_list[0][0][0],
                {
                    "color": {"stderr": "no_color", "stdout": "no_color"},
                    "extract_flat": "discard_in_playlist",
                    "format": "bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]",  # NOQA: E501
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
                    "outtmpl": str(d / hsh / "video.%(ext)s"),
                },
            )
            self.assertEqual(
                m.call_args_list[1][0][0],
                {
                    "color": {"stderr": "no_color", "stdout": "no_color"},
                    "extract_flat": "discard_in_playlist",
                    "format": "bestvideo[ext=mp4]+bestaudio[ext=mp4]/best[ext=mp4]",  # NOQA: E501
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
                    "outtmpl": str(d / hsh / "video.%(ext)s"),
                },
            )

            cu.refresh_from_db()
            self.assertTrue(cu.is_ready)
            self.assertFalse(cu.is_processing)
            self.assertFalse(cu.is_failed)
            self.assertIsNotNone(cu.archived_at)

    @patch("cool_urls.coolers.videos.YoutubeDL")
    def test_cool_failure(self, m):
        url = "https://youtube.com/watch?v=test"
        cu = CoolUrl.objects.create(url=url)

        m.side_effect = YoutubeDLError("test")
        with TemporaryDirectory() as d:
            d = Path(d)
            with patch("cool_urls.coolers.videos.VideoCooler.MEDIA_ROOT", d):
                cooler = VideoCooler(cu)
                with patch.object(cooler.logger, "warning") as lw:
                    with patch.object(cooler.logger, "error") as le:
                        with patch.object(cu.logger, "error") as cule:
                            cooler.cool()
                            self.assertEqual(cule.call_count, 1)
                        self.assertEqual(le.call_count, 1)
                    self.assertEqual(lw.call_count, 2)

            self.assertEqual(m.call_count, 2)

            cu.refresh_from_db()
            self.assertFalse(cu.is_ready)
            self.assertFalse(cu.is_processing)
            self.assertTrue(cu.is_failed)
            self.assertIsNone(cu.archived_at)
