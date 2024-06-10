from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from ..coolers import (
    FileCooler,
    InstagramCooler,
    PageCooler,
    VimeoCooler,
    YoutubeCooler,
)
from ..models import CoolUrl


class CoolUrlTestCase(TestCase):
    def test___str__(self):
        self.assertEqual(
            str(CoolUrl.objects.create(url="https://example.com/")),
            "https://example.com/",
        )

    def test_cooler_for_page(self):
        cu = CoolUrl.objects.create(url="https://example.com/")
        self.assertIsInstance(cu.cooler, PageCooler)

    def test_cooler_for_file(self):
        cu = CoolUrl.objects.create(url="https://example.com/test.webp")
        self.assertIsInstance(cu.cooler, FileCooler)

    def test_cooler_for_youtube(self):
        cu = CoolUrl.objects.create(url="https://youtube.com/watch?v=test")
        self.assertIsInstance(cu.cooler, YoutubeCooler)

    def test_cooler_for_instagram(self):
        cu = CoolUrl.objects.create(
            url="https://instagram.com/username/reel/test"
        )
        self.assertIsInstance(cu.cooler, InstagramCooler)

    def test_cooler_for_vimeo(self):
        cu = CoolUrl.objects.create(url="https://vimeo.com/0000")
        self.assertIsInstance(cu.cooler, VimeoCooler)

    def test_properties(self):
        cu = CoolUrl.objects.create(url="https://example.com/")
        self.assertEqual(cu.hash, "182ccedb33a9e03fbf1079b209da1a31")
        self.assertEqual(cu.parsed.scheme, "https")
        self.assertEqual(
            cu.as_local,
            "/media/archives/182ccedb33a9e03fbf1079b209da1a31/index.html",
        )
        self.assertEqual(cu.as_remote, "https://example.com/")

    def test_markup_with_local_on_and_ready_on(self):
        cu = CoolUrl.objects.create(
            url="https://example.com/",
            show_local=True,
            is_ready=True,
            archived_at=timezone.now(),
        )
        self.assertEqual(
            cu.markup,
            "/media/archives/182ccedb33a9e03fbf1079b209da1a31/index.html",
        )

    def test_markup_with_local_off_and_ready_on(self):
        self.assertEqual(
            CoolUrl.objects.create(
                url="https://example.com/",
                show_local=False,
                is_ready=True,
                archived_at=timezone.now(),
            ).markup,
            "https://example.com/",
        )

    def test_markup_with_local_on_and_ready_off(self):
        self.assertEqual(
            CoolUrl.objects.create(
                url="https://example.com/",
                show_local=True,
                is_ready=False,
            ).markup,
            "https://example.com/",
        )

    @patch("cool_urls.models.is_processing.send")
    def test_mark_as_processing(self, m):
        cu = CoolUrl.objects.create(url="https://example.com/")
        cu.mark_as_processing()
        cu.refresh_from_db()
        self.assertFalse(cu.is_ready)
        self.assertFalse(cu.is_failed)
        self.assertTrue(cu.is_processing)
        self.assertIsNone(cu.archived_at)
        self.assertEqual(m.call_count, 1)

    @patch("cool_urls.models.is_ready.send")
    def test_mark_as_ready(self, m):
        cu = CoolUrl.objects.create(url="https://example.com/")
        cu.mark_as_ready()
        cu.refresh_from_db()
        self.assertTrue(cu.is_ready)
        self.assertFalse(cu.is_failed)
        self.assertFalse(cu.is_processing)
        self.assertIsNotNone(cu.archived_at)
        self.assertEqual(m.call_count, 1)

    @patch("cool_urls.models.has_failed.send")
    def test_mark_as_failed(self, m):
        cu = CoolUrl.objects.create(url="https://example.com/")
        with patch.object(cu.logger, "error") as lg:
            cu.mark_as_failed()
            self.assertEqual(lg.call_count, 1)

        cu.refresh_from_db()
        self.assertFalse(cu.is_ready)
        self.assertTrue(cu.is_failed)
        self.assertFalse(cu.is_processing)
        self.assertIsNone(cu.archived_at)
        self.assertEqual(m.call_count, 1)

    def test_reset(self):
        with TemporaryDirectory() as d:
            cu = CoolUrl.objects.create(
                url="https://example.com/",
                is_ready=True,
                archived_at=timezone.now(),
            )
            test_file = Path(d) / "test"
            test_file.touch()
            self.assertTrue(test_file.exists())
            with patch.object(cu.cooler, "target_dir", d):
                cu.reset()
            self.assertFalse(test_file.exists())

        cu.refresh_from_db()
        self.assertFalse(cu.is_ready)
        self.assertFalse(cu.is_failed)
        self.assertFalse(cu.is_processing)
        self.assertIsNone(cu.archived_at)

    @patch("cool_urls.models.new_url_created.send")
    def test_save_uses_created_signal_properly(self, m):
        CoolUrl(url="https://example.com/")
        self.assertEqual(m.call_count, 0)

        cu = CoolUrl.objects.create(url="https://example.com/")
        self.assertEqual(m.call_count, 1)

        cu.save()
        self.assertEqual(m.call_count, 1)

    @patch("cool_urls.models.show_local_was_enabled.send")
    def test_save_creation_signal_sent(self, m):
        cu = CoolUrl.objects.create(
            url="https://example.com/", show_local=False
        )
        self.assertEqual(m.call_count, 0)

        cu.save()
        self.assertEqual(m.call_count, 0)

        cu.show_local = True
        cu.save()
        self.assertEqual(m.call_count, 1)

        cu.save()
        self.assertEqual(m.call_count, 1)
