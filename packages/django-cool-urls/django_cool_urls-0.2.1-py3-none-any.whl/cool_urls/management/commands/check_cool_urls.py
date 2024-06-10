from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

import httpx

from ...logging import Loggable
from ...models import CoolUrl


class Command(Loggable, BaseCommand):
    """
    Go through all CoolUrl entries and check if the site is still responding
    properly.  If not, set `show_local` to `True` so we prefer the local copy.

    This is the sort of thing you'd probably want to run in a weekly cron or
    something.
    """

    # The time during which you don't want to re-check a URL
    WINDOW = timedelta(days=getattr(settings, "COOL_URLS_CHECK_WINDOW", 30))

    def handle(self, *args, **options):
        window = timezone.now() - self.WINDOW
        urls = CoolUrl.objects.filter(is_ready=True, show_local=False).exclude(
            last_http_check_time__gt=window
        )

        for cu in urls.iterator():
            update_fields = ["last_http_check_state", "last_http_check_time"]
            cu.last_http_check_state = httpx.get(cu.url).status_code
            cu.last_http_check_time = timezone.now()

            if cu.last_http_check_state != httpx.codes.OK:
                self.logger.info(
                    "URL %s had an HTTP response of %s, so we're marking "
                    "it to render the local archived copy.",
                    cu.url,
                    cu.last_http_check_state,
                )
                cu.show_local = True
                update_fields.append("show_local")

            cu.save(update_fields=tuple(update_fields))
