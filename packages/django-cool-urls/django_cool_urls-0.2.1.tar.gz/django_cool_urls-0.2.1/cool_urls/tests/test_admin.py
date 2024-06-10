from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from ..models import CoolUrl


class AdminTestCase(TestCase):
    def test_pages_loads_ok(self):
        cu = CoolUrl.objects.create(url="https://example.org/")
        self.client.force_login(
            User.objects.create(
                username="test",
                is_staff=True,
                is_superuser=True,
            )
        )

        url = reverse("admin:cool_urls_coolurl_changelist")
        self.assertEqual(self.client.get(url).status_code, 200)

        url = reverse(
            "admin:cool_urls_coolurl_change",
            kwargs={"object_id": cu.pk},
        )
        self.assertEqual(self.client.get(url).status_code, 200)
