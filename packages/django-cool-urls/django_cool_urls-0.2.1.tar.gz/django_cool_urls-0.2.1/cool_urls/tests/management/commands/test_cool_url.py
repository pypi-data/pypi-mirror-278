from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from ....models import CoolUrl


class CommandTestCase(TestCase):
    @patch("cool_urls.models.CoolUrl.cool")
    def test_with_embed(self, m):
        self._call("https://youtube.com/watch?v=test", "--embed")

        self.assertEqual(m.call_count, 1)

        cu = CoolUrl.objects.get()
        self.assertEqual(cu.url, "https://youtube.com/watch?v=test")
        self.assertTrue(cu.is_embedded)

    @patch("cool_urls.models.CoolUrl.cool")
    def test_with_show_local(self, m):
        self._call("https://example.com/", "--show-local")

        self.assertEqual(m.call_count, 1)

        cu = CoolUrl.objects.get()
        self.assertEqual(cu.url, "https://example.com/")
        self.assertTrue(cu.show_local)

    @patch("cool_urls.models.CoolUrl.cool")
    def test_with_prexisting(self, m):
        # Arrange
        CoolUrl.objects.create(url="https://example.com/", is_embedded=False)

        # Act
        self._call("https://example.com/", "--embed")

        # Assert
        self.assertEqual(m.call_count, 0)

        cu = CoolUrl.objects.get()
        self.assertEqual(cu.url, "https://example.com/")
        self.assertFalse(
            cu.is_embedded,
            "The original value shouldn't be overwritten",
        )

    @staticmethod
    def _call(*args):
        out = StringIO()
        call_command("cool_url", *args, stdout=out, stderr=StringIO())
        return out.getvalue()
