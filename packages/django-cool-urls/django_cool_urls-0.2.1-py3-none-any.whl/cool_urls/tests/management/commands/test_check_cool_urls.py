from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from freezegun import freeze_time

from ....models import CoolUrl


@freeze_time("2020-01-01")
class CommandTestCase(TestCase):
    MOCK_HTTPX_GET = "cool_urls.management.commands.check_cool_urls.httpx.get"

    def setUp(self):
        self.now = timezone.now()

    # HTTP 200

    def test_not_ready_with_200(self):
        """
        If the URL isn't ready, we shouldn't be acting on it at all.
        """

        # Arrange
        cu = CoolUrl.objects.create(
            url="https://example.com/",
            is_ready=False,
            show_local=False,
        )

        # Act
        with patch(self.MOCK_HTTPX_GET) as m:
            m.return_value = Mock(status_code=200)
            call_command("check_cool_urls")
            self.assertEqual(m.call_count, 0)

        # Assert
        cu.refresh_from_db()
        self.assertFalse(cu.is_ready)
        self.assertFalse(cu.show_local)
        self.assertIsNone(cu.last_http_check_state)
        self.assertIsNone(cu.last_http_check_time)

    def test_ready_with_show_local_and_with_200(self):
        """
        If the URL is ready and show_local is already set, we shouldn't act on
        it at all.
        """

        # Arrange
        check_time = timezone.make_aware(datetime(2019, 1, 1))
        cu = CoolUrl.objects.create(
            url="https://example.com/",
            is_ready=True,
            show_local=True,
            archived_at=timezone.now(),
            last_http_check_time=check_time,
            last_http_check_state=502,
        )

        # Act
        with patch(self.MOCK_HTTPX_GET) as m:
            m.return_value = Mock(status_code=200)
            call_command("check_cool_urls")
            self.assertEqual(m.call_count, 0)

        # Assert
        cu.refresh_from_db()
        self.assertTrue(cu.is_ready)
        self.assertTrue(cu.show_local)
        self.assertEqual(cu.last_http_check_time, check_time)
        self.assertEqual(cu.last_http_check_state, 502)

    def test_ready_without_show_local_and_with_200(self):
        """
        A page that doesn't yet have show_local set to True should be acted
        upon, but with a return status of 200, nothing should change except for
        the last_http_check_* values.
        """

        # Arrange
        cu = CoolUrl.objects.create(
            url="https://example.com/",
            is_ready=True,
            show_local=False,
            archived_at=timezone.now(),
        )

        # Act
        with patch(self.MOCK_HTTPX_GET) as m:
            m.return_value = Mock(status_code=200)
            call_command("check_cool_urls")
            self.assertEqual(m.call_count, 1)

        # Assert
        cu.refresh_from_db()
        self.assertTrue(cu.is_ready)
        self.assertFalse(cu.show_local)
        self.assertEqual(cu.last_http_check_time, self.now)
        self.assertEqual(cu.last_http_check_state, 200)

    def test_ready_with_200_inside_window(self):
        """
        If the page is ready and has been checked inside the check window, then
        we shouldn't be re-checking it yet.
        """

        # Arrange
        check_time = timezone.now() - timedelta(days=5)
        cu = CoolUrl.objects.create(
            url="https://example.com/",
            is_ready=True,
            show_local=False,
            archived_at=check_time,
            last_http_check_state=200,
            last_http_check_time=check_time,
        )

        # Act
        with patch(self.MOCK_HTTPX_GET) as m:
            m.return_value = Mock(status_code=200)
            call_command("check_cool_urls")
            self.assertEqual(m.call_count, 0)

        # Assert
        cu.refresh_from_db()
        self.assertTrue(cu.is_ready)
        self.assertFalse(cu.show_local)
        self.assertEqual(cu.last_http_check_time, check_time)
        self.assertEqual(cu.last_http_check_state, 200)

    def test_ready_with_200_outside_window(self):
        """
        If the page is ready and was last checked outside the check window,
        then we should re-check it now.
        """

        # Arrange
        check_time = timezone.now() - timedelta(days=60)
        cu = CoolUrl.objects.create(
            url="https://example.com/",
            is_ready=True,
            show_local=False,
            archived_at=check_time,
            last_http_check_state=200,
            last_http_check_time=check_time,
        )

        # Act
        with patch(self.MOCK_HTTPX_GET) as m:
            m.return_value = Mock(status_code=200)
            call_command("check_cool_urls")
            self.assertEqual(m.call_count, 1)

        # Assert
        cu.refresh_from_db()
        self.assertTrue(cu.is_ready)
        self.assertFalse(cu.show_local)
        self.assertEqual(cu.last_http_check_time, self.now)
        self.assertEqual(cu.last_http_check_state, 200)

    # HTTP 404

    def test_ready_without_show_local_and_with_404(self):
        """
        A page that doesn't yet have show_local set to True should be acted
        upon, and with a return status of 404 show_local should be set to True
        """

        # Arrange
        cu = CoolUrl.objects.create(
            url="https://example.com/",
            is_ready=True,
            show_local=False,
            archived_at=timezone.now(),
        )

        # Act
        with patch(self.MOCK_HTTPX_GET) as m:
            m.return_value = Mock(status_code=404)
            call_command("check_cool_urls")
            self.assertEqual(m.call_count, 1)

        # Assert
        cu.refresh_from_db()
        self.assertTrue(cu.is_ready)
        self.assertTrue(cu.show_local)
        self.assertEqual(cu.last_http_check_time, self.now)
        self.assertEqual(cu.last_http_check_state, 404)

    def test_ready_with_404_outside_window(self):
        """
        If the page is ready and was last checked outside the check window,
        then we should re-check it now.
        """

        # Arrange
        check_time = timezone.now() - timedelta(days=60)
        cu = CoolUrl.objects.create(
            url="https://example.com/",
            is_ready=True,
            show_local=False,
            archived_at=check_time,
            last_http_check_state=200,
            last_http_check_time=check_time,
        )

        # Act
        with patch(self.MOCK_HTTPX_GET) as m:
            m.return_value = Mock(status_code=404)
            call_command("check_cool_urls")
            self.assertEqual(m.call_count, 1)

        # Assert
        cu.refresh_from_db()
        self.assertTrue(cu.is_ready)
        self.assertTrue(cu.show_local)
        self.assertEqual(cu.last_http_check_time, self.now)
        self.assertEqual(cu.last_http_check_state, 404)
