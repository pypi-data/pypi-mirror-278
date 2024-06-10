from django.core.management.base import BaseCommand

from ...models import CoolUrl


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("url", help="URL to cool")
        parser.add_argument(
            "--embed",
            action="store_true",
            help="Archive it as embedded media",
        )
        parser.add_argument(
            "--show-local",
            action="store_true",
            help="Set show_local=True if cooling is successful",
        )

    def handle(self, *args, **options) -> None:
        cu, was_created = CoolUrl.objects.get_or_create(
            url=options["url"],
            defaults={
                "is_embedded": options["embed"],
                "show_local": options["show_local"],
            },
        )

        if not was_created:
            self.stdout.write(
                "Looks like this URL "
                f"has already been cooled: {cu.cooler.target_dir}"
            )
            return

        cu.cool()
        self.stdout.write(f"Cooling complete: {cu.cooler.target_dir}")
