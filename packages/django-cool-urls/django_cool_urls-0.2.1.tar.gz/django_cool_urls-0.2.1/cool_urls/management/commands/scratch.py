from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import URLPattern, URLResolver


class Command(BaseCommand):  # pragma: no cover
    def handle(self, *args, **options):
        urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [""])
        for p in list_urls(urlconf.urlpatterns):
            print("".join(p))


def list_urls(lis, acc=None):
    if acc is None:
        acc = []
    if not lis:
        return
    l = lis[0]
    if isinstance(l, URLPattern):
        yield acc + [str(l.pattern)]
    elif isinstance(l, URLResolver):
        yield from list_urls(l.url_patterns, acc + [str(l.pattern)])
    yield from list_urls(lis[1:], acc)
