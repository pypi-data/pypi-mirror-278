from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.test import TestCase

import httpx

from ...coolers import FileCooler
from ...coolers.exceptions import CoolingError
from ...models import CoolUrl


class FileCoolerTestCase(TestCase):
    def setUp(self):
        self.url = "https://example.com/test.webp"
        self.hash = "08ab96577722cb5138eb86f1ad80714e"
        self.cu = CoolUrl.objects.create(url=self.url)

    def test_remote_markup(self):
        self.assertEqual(FileCooler(self.cu).remote_markup, self.url)

    def test_local_markup(self):
        self.assertEqual(
            FileCooler(self.cu).local_markup,
            f"/media/archives/{self.hash}/{self.hash}.webp",
        )

    @patch("cool_urls.coolers.files.httpx.stream")
    def test_cool_success(self, m):
        m.return_value.__enter__.return_value.status_code = httpx.codes.OK
        m.return_value.__enter__.return_value.iter_bytes.return_value = [b"0"]

        with TemporaryDirectory() as d:
            d = Path(d)
            with patch("cool_urls.coolers.files.FileCooler.MEDIA_ROOT", d):
                cooler = FileCooler(self.cu)
                cooler.cool()
            self.assertTrue((d / self.hash / f"{self.hash}.webp").exists())

        self.cu.refresh_from_db()
        self.assertTrue(self.cu.is_ready)
        self.assertFalse(self.cu.is_processing)
        self.assertFalse(self.cu.is_failed)

    @patch("cool_urls.coolers.files.httpx.stream")
    def test_cool_failure(self, m):
        m.return_value.__enter__.return_value.status_code = (
            httpx.codes.NOT_FOUND
        )
        m.return_value.__enter__.return_value.iter_bytes.return_value = [b"0"]

        with TemporaryDirectory() as d:
            d = Path(d)
            with patch("cool_urls.coolers.files.FileCooler.MEDIA_ROOT", d):
                cooler = FileCooler(self.cu)
                with patch.object(self.cu.logger, "error") as le:
                    self.assertRaises(CoolingError, cooler.cool)
                    self.assertEqual(le.call_count, 1)
            self.assertFalse((d / self.hash / f"{self.hash}.webp").exists())

        self.cu.refresh_from_db()
        self.assertFalse(self.cu.is_ready)
        self.assertFalse(self.cu.is_processing)
        self.assertTrue(self.cu.is_failed)
