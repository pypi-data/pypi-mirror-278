from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

from django.test import TestCase

from ...coolers import PageCooler
from ...coolers.exceptions import CoolingError
from ...models import CoolUrl


class FakeWhich:
    def __init__(self, successful_names=()):
        self.successful_names = successful_names

    def __call__(self, name: str) -> str | None:
        if name in self.successful_names:
            return f"/test/{name}"
        return None


class PageCoolerTestCase(TestCase):
    def setUp(self):
        self.url = "https://example.com/"
        self.cu = CoolUrl.objects.create(url=self.url)

    def test___init__(self):
        with patch("cool_urls.coolers.pages.which", FakeWhich(("monolith",))):
            cooler = PageCooler(self.cu)
        self.assertEqual(cooler._monolith, "/test/monolith")
        self.assertIsNone(cooler._chromium)

    def test_remote_markup(self):
        self.assertEqual(PageCooler(self.cu).remote_markup, self.url)

    def test_local_markup(self):
        self.assertEqual(
            PageCooler(self.cu).local_markup,
            "/media/archives/182ccedb33a9e03fbf1079b209da1a31/index.html",
        )

    def test_monolith_options(self):
        self.assertEqual(
            PageCooler(self.cu).monolith_options,
            (
                "--isolate",
                f"--base-url={self.url}",
                "--output=.media/archives/182ccedb33a9e03fbf1079b209da1a31/index.html",  # NOQA: E501
                "--no-audio",
                "--no-video",
            ),
        )

    def test_cool_already_exists(self):
        fake_which = FakeWhich(("monolith",))
        with TemporaryDirectory() as d:
            d = Path(d)
            file = d / "182ccedb33a9e03fbf1079b209da1a31/index.html"
            file.parent.mkdir(parents=True)
            file.touch()
            with patch("cool_urls.coolers.pages.PageCooler.MEDIA_ROOT", d):
                with patch("cool_urls.coolers.pages.which", fake_which):
                    cooler = PageCooler(self.cu)
                    with patch.object(cooler.logger, "warning") as m:
                        cooler.cool()
                        self.assertEqual(m.call_count, 1)
                        self.assertIn("already been cooled", m.call_args[0][0])

    def test_cool_without_monolith(self):
        fake_which = FakeWhich(())
        with TemporaryDirectory() as d:
            d = Path(d)
            with patch("cool_urls.coolers.pages.PageCooler.MEDIA_ROOT", d):
                with patch("cool_urls.coolers.pages.which", fake_which):
                    cooler = PageCooler(self.cu)
                    self.assertRaises(CoolingError, cooler.cool)

    def test_cool_without_chromium_success(self):
        fake_which = FakeWhich(("monolith",))
        with TemporaryDirectory() as d:
            d = Path(d)
            with patch("cool_urls.coolers.pages.PageCooler.MEDIA_ROOT", d):
                with patch("cool_urls.coolers.pages.which", fake_which):
                    cooler = PageCooler(self.cu)
                    with patch.object(cooler.logger, "warning") as lg:
                        with patch("cool_urls.coolers.pages.run") as m:
                            m.return_value = Mock(returncode=0)
                            cooler.cool()
                            self.assertEqual(m.call_count, 1)
                        self.assertEqual(lg.call_count, 1)

        self.cu.refresh_from_db()
        self.assertTrue(self.cu.is_ready)

    def test_cool_without_chromium_failure(self):
        fake_which = FakeWhich(("monolith",))
        with TemporaryDirectory() as d:
            d = Path(d)
            with patch("cool_urls.coolers.pages.PageCooler.MEDIA_ROOT", d):
                with patch("cool_urls.coolers.pages.which", fake_which):
                    cooler = PageCooler(self.cu)
                    with patch.object(cooler.logger, "warning") as lw:
                        with patch.object(self.cu.logger, "error") as le:
                            with patch("cool_urls.coolers.pages.run") as m:
                                m.return_value = Mock(returncode=1)
                                self.assertRaises(CoolingError, cooler.cool)
                                self.assertEqual(m.call_count, 1)
                            self.assertEqual(le.call_count, 1)
                        self.assertEqual(lw.call_count, 1)

        self.cu.refresh_from_db()
        self.assertFalse(self.cu.is_ready)
        self.assertTrue(self.cu.is_failed)

    def test_cool_with_chromium_success(self):
        fake_which = FakeWhich(("monolith", "chromium"))
        with TemporaryDirectory() as d:
            d = Path(d)
            with patch("cool_urls.coolers.pages.PageCooler.MEDIA_ROOT", d):
                with patch("cool_urls.coolers.pages.which", fake_which):
                    cooler = PageCooler(self.cu)
                    with patch("cool_urls.coolers.pages.Popen") as m:
                        m.return_value = Mock(returncode=0)
                        cooler.cool()
                        self.assertEqual(m.call_count, 2)

        self.cu.refresh_from_db()
        self.assertTrue(self.cu.is_ready)

    def test_cool_with_chromium_failure(self):
        fake_which = FakeWhich(("monolith", "chromium"))
        with TemporaryDirectory() as d:
            d = Path(d)
            with patch("cool_urls.coolers.pages.PageCooler.MEDIA_ROOT", d):
                with patch("cool_urls.coolers.pages.which", fake_which):
                    cooler = PageCooler(self.cu)
                    with patch.object(self.cu.logger, "error") as le:
                        with patch("cool_urls.coolers.pages.Popen") as m:
                            m.return_value = Mock(returncode=1)
                            self.assertRaises(CoolingError, cooler.cool)
                            self.assertEqual(m.call_count, 2)
                        self.assertEqual(le.call_count, 1)

        self.cu.refresh_from_db()
        self.assertFalse(self.cu.is_ready)
        self.assertTrue(self.cu.is_failed)
