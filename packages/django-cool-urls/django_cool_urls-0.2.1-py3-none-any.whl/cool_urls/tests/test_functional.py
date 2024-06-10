from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase, tag
from django.urls import reverse

from ..models import CoolUrl


@tag("functional")
class FunctionalTestCase(TestCase):
    def test_cool_url(self):
        url = "https://gitlab.com/danielquinn/django-cool-urls/"

        # First we render the page to trigger the creation of the CoolURL
        # object.

        response = self.client.get(reverse("tests-url"))
        self.assertIn(f'<a href="{url}">', response.content.decode())
        self.assertEqual(CoolUrl.objects.count(), 1)

        # Confirm it's there in the state we expect.

        cu = CoolUrl.objects.get()
        self.assertEqual(cu.url, url)
        self.assertFalse(cu.is_processing)
        self.assertFalse(cu.is_ready)
        self.assertFalse(cu.is_failed)
        self.assertFalse(cu.show_local)

        # Trigger the cool_urls management command that should archive the URL.

        with TemporaryDirectory() as d:
            d = Path(d)
            with patch("cool_urls.coolers.pages.PageCooler.MEDIA_ROOT", d):
                call_command("cool_urls")
                expected_path = cu.cooler.target_dir / "index.html"
                self.assertTrue(expected_path.exists())

                # Confirm it's completed happily and that `show_local` is still
                # False.

                cu = CoolUrl.objects.get()
                self.assertEqual(cu.url, url)
                self.assertFalse(cu.is_processing)
                self.assertTrue(cu.is_ready)
                self.assertFalse(cu.is_failed)
                self.assertFalse(cu.show_local)

                # As show_local is still False, we should still see the remote
                # URL in the template rendering.

                response = self.client.get(reverse("tests-url"))
                self.assertIn(f'<a href="{url}">', response.content.decode())

                # Finally, set show_local to True and confirm that the local
                # URL shows up in the template rendering.

                cu.show_local = True
                cu.save()

                response = self.client.get(reverse("tests-url"))
                self.assertIn(
                    '<a href="{media_url}archives/{hash}/index.html">'.format(
                        media_url=settings.MEDIA_URL,
                        hash="d16b49be58f68e8d6da21fc0a9c3651f",
                    ),
                    response.content.decode(),
                )

    def test_cool_embed(self):
        url = "https://www.youtube.com/watch?v=88GOVPswhjc"

        # First we render the page to trigger the creation of the CoolURL
        # object.

        response = self.client.get(reverse("tests-embed"))
        self.assertIn(
            '<div class="cool-urls-video-container-remote">',
            response.content.decode(),
        )
        self.assertIn(
            'src="https://www.youtube-nocookie.com/embed/88GOVPswhjc"',
            response.content.decode(),
        )
        self.assertEqual(CoolUrl.objects.count(), 1)

        # Confirm it's there in the state we expect.

        cu = CoolUrl.objects.get()
        self.assertEqual(cu.url, url)
        self.assertFalse(cu.is_processing)
        self.assertFalse(cu.is_ready)
        self.assertFalse(cu.is_failed)
        self.assertFalse(cu.show_local)

        # Trigger the cool_urls management command that should archive the URL.

        with TemporaryDirectory() as d:
            d = Path(d)
            with patch("cool_urls.coolers.videos.VideoCooler.MEDIA_ROOT", d):
                call_command("cool_urls")
                self.assertTrue((cu.cooler.target_dir / "video.webp").exists())
                self.assertTrue((cu.cooler.target_dir / "video.mp4").exists())
                self.assertTrue((cu.cooler.target_dir / "video.webm").exists())

                # Confirm it's completed happily and that `show_local` is still
                # False.

                cu = CoolUrl.objects.get()
                self.assertEqual(cu.url, url)
                self.assertFalse(cu.is_processing)
                self.assertTrue(cu.is_ready)
                self.assertFalse(cu.is_failed)
                self.assertFalse(cu.show_local)

                # As show_local is still False, we should still see the remote
                # URL in the template rendering.

                response = self.client.get(reverse("tests-embed"))
                self.assertIn(
                    '<div class="cool-urls-video-container-remote">',
                    response.content.decode(),
                )
                self.assertIn(
                    'src="https://www.youtube-nocookie.com/embed/88GOVPswhjc"',
                    response.content.decode(),
                )

                # Finally, set show_local to True and confirm that the local
                # URL shows up in the template rendering.

                cu.show_local = True
                cu.save()

                response = self.client.get(reverse("tests-embed"))
                self.assertIn(
                    '<div class="cool-urls-video-container-local">',
                    response.content.decode(),
                )
                for fmt in ("webm", "mp4"):
                    self.assertIn(
                        '<source src="{media_url}archives/{hash}/video.{fmt}" type="video/{fmt}" />'.format(  # NOQA: E501
                            media_url=settings.MEDIA_URL,
                            hash="0b6e330ac7e8e2d66d89b73a833a487e",
                            fmt=fmt,
                        ),
                        response.content.decode(),
                    )
