
from django.test import TestCase, override_settings

from ..models import CoolUrl
from ..templatetags.cool_urls import cool_embed, cool_url


def fake_policy(url: str, is_embedded: bool) -> bool:
    return "test" in url


class CoolEmbedTestCase(TestCase):
    def test_without_policy(self):
        url = "https://youtube.com/watch?v=test"
        cool_embed(url)
        self.assertEqual(CoolUrl.objects.count(), 1)
        cu = CoolUrl.objects.get(url=url)
        self.assertEqual(cu.url, url)
        self.assertFalse(cu.show_local)
        self.assertTrue(cu.is_embedded)

    @override_settings(COOL_URLS_POLICY="LOCAL")
    def test_with_local_policy(self):
        url = "https://youtube.com/watch?v=test"
        cool_embed(url)
        self.assertEqual(CoolUrl.objects.count(), 1)
        cu = CoolUrl.objects.get(url=url)
        self.assertEqual(cu.url, url)
        self.assertTrue(cu.show_local)
        self.assertTrue(cu.is_embedded)

    @override_settings(COOL_URLS_POLICY="REMOTE")
    def test_with_policy(self):
        url = "https://youtube.com/watch?v=test"
        cool_embed(url)
        self.assertEqual(CoolUrl.objects.count(), 1)
        cu = CoolUrl.objects.get(url=url)
        self.assertEqual(cu.url, url)
        self.assertFalse(cu.show_local)
        self.assertTrue(cu.is_embedded)

    @override_settings(
        COOL_URLS_POLICY="cool_urls.tests.test_templatetags.fake_policy"
    )
    def test_with_callable_policy(self):
        url1 = "https://youtube.com/watch?v=test"
        cool_embed(url1)
        self.assertEqual(CoolUrl.objects.count(), 1)
        cu = CoolUrl.objects.get(url=url1)
        self.assertEqual(cu.url, url1)
        self.assertTrue(cu.show_local)
        self.assertTrue(cu.is_embedded)

        url2 = "https://youtube.com/watch?v=no"
        cool_embed(url2)
        self.assertEqual(CoolUrl.objects.count(), 2)
        cu = CoolUrl.objects.get(url=url2)
        self.assertEqual(cu.url, url2)
        self.assertFalse(cu.show_local)
        self.assertTrue(cu.is_embedded)

    def test_multiple_invocations(self):
        url = "https://youtube.com/watch?v=test"
        cool_embed(url)
        cool_embed(url)
        self.assertEqual(CoolUrl.objects.count(), 1)


class CoolUrlTestCase(TestCase):
    def test_without_policy(self):
        url = "https://example.com/"
        cool_url(url)
        self.assertEqual(CoolUrl.objects.count(), 1)
        cu = CoolUrl.objects.get(url=url)
        self.assertEqual(cu.url, url)
        self.assertFalse(cu.show_local)
        self.assertFalse(cu.is_embedded)

    @override_settings(COOL_URLS_POLICY="LOCAL")
    def test_with_policy(self):
        url = "https://example.com/"
        cool_url(url)
        self.assertEqual(CoolUrl.objects.count(), 1)
        cu = CoolUrl.objects.get(url=url)
        self.assertEqual(cu.url, url)
        self.assertTrue(cu.show_local)
        self.assertFalse(cu.is_embedded)

    def test_multiple_invocations(self):
        url = "https://example.com/"
        cool_url(url)
        cool_url(url)
        self.assertEqual(CoolUrl.objects.count(), 1)
