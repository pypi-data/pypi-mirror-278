from django.test import TestCase

from ...coolers import (
    Cooler,
    FileCooler,
    InstagramCooler,
    PageCooler,
    VimeoCooler,
    YoutubeCooler,
)
from ...models import CoolUrl


class CoolerTestCase(TestCase):
    def test_build_file(self):
        urls = (
            "http://example.com/file.webp",
            "https://example.com/file.webp",
            "https://example.com/path/to/something/interesting.pdf",
            "https://example.com/path/to/video.mkv?some=arg",
            "ftp://example.com/path/to/file.png",
        )
        for url in urls:
            with self.subTest(url=url):
                cooler = Cooler.build(CoolUrl(url=url))
                self.assertIsInstance(cooler, FileCooler)

    def test_build_page(self):
        urls = (
            "http://example.com/",
            "https://example.com/",
            "https://example.com/something/",
            "https://example.com/something",
            "https://example.com/something.with.dots/",
            "https://example.com/something.with.dots/?answer=42",
            "https://example.com/something.htm",
            "https://example.com/something.html",
            "https://example.com/something.php",
            "https://example.com/something.asp",
            "https://example.com/something.aspx",
            "https://example.com/something.HTM",
            "https://example.com/something.HTML",
            "https://example.com/something.PHP",
            "https://example.com/something.ASPX",
            "https://example.com/something.ASP",
        )
        for url in urls:
            with self.subTest(url=url):
                cooler = Cooler.build(CoolUrl(url=url))
                self.assertIsInstance(cooler, PageCooler)

    def test_build_youtube(self):
        urls = (
            "https://youtube.com/watch?v=test",
            "https://www.youtube.com/watch?v=test",
            "https://www.youtube.com/watch?v=test&some=other&argument=s",
        )
        for url in urls:
            with self.subTest(url=url):
                cooler = Cooler.build(CoolUrl(url=url))
                self.assertIsInstance(cooler, YoutubeCooler)
                self.assertEqual(cooler.video_id, "test")

    def test_build_instagram(self):
        urls = (
            "https://instagram.com/some-user/reel/test/",
            "https://www.instagram.com/some-user/reel/test/",
            "https://instagram.com/some-user/reel/test",
        )
        for url in urls:
            with self.subTest(url=url):
                cooler = Cooler.build(CoolUrl(url=url))
                self.assertIsInstance(cooler, InstagramCooler)
                self.assertEqual(cooler.video_id, "test")

    def test_build_vimeo(self):
        urls = (
            "https://vimeo.com/123456/",
            "https://www.vimeo.com/123456/",
            "https://vimeo.com/123456",
        )
        for url in urls:
            with self.subTest(url=url):
                cooler = Cooler.build(CoolUrl(url=url))
                self.assertIsInstance(cooler, VimeoCooler)
                self.assertEqual(cooler.video_id, "123456")
