from django.core.management.base import BaseCommand

from ...models import CoolUrl


class Command(BaseCommand):  # pragma: no cover
    def handle(self, *args, **options):
        cool_urls = CoolUrl.objects.filter(
            is_ready=False,
            is_processing=False,
            is_failed=False,
        )
        for cool_url in cool_urls.iterator():
            cool_url.cooler.cool()
