from hashlib import md5
from shutil import rmtree
from urllib.parse import ParseResult, urlparse

from django.db.models import (
    BooleanField,
    CheckConstraint,
    DateTimeField,
    Model,
    PositiveIntegerField,
    Q,
    URLField,
)
from django.utils import timezone
from django.utils.functional import cached_property

from .coolers import Cooler
from .logging import Loggable
from .signals import (
    has_failed,
    is_processing,
    is_ready,
    new_url_created,
    show_local_was_enabled,
)


class CoolUrl(Loggable, Model):
    """
    Where we keep the state of the URL-cooling process.
    """

    url = URLField(unique=True, editable=False)

    is_ready = BooleanField(default=False, db_index=True, editable=False)
    is_processing = BooleanField(default=False, db_index=True, editable=False)
    is_failed = BooleanField(default=False, db_index=True, editable=False)

    archived_at = DateTimeField(
        blank=True,
        null=True,
        db_index=True,
        editable=False,
    )
    show_local = BooleanField(
        default=False,
        db_index=True,
        help_text=(
            "Whether we want to use the local copy or continue to refer to "
            "the remote one."
        ),
    )
    is_embedded = BooleanField(
        default=False,
        db_index=True,
        editable=False,
        help_text=(
            "If this is true, we'll attempt to pull down the audio or video "
            "from the page so it can be embedded rather than a copy of the "
            "page itself."
        ),
    )

    last_http_check_state = PositiveIntegerField(
        blank=True,
        null=True,
        db_index=True,
        editable=False,
    )
    last_http_check_time = DateTimeField(
        blank=True,
        null=True,
        db_index=True,
        editable=False,
    )

    class Meta:
        verbose_name = "Cool URL"
        verbose_name_plural = "Cool URLs"
        constraints = (
            # is_ready can't be True if is_processing or is_failed are True
            # is_processing can't be True if is_ready or is_failed are True
            # is_failed can't be True if is_ready or is_processing are True
            CheckConstraint(
                name="coolurl_status_permutations",
                check=(
                    Q(is_ready=True, is_processing=False, is_failed=False)
                    | Q(is_ready=False, is_processing=True, is_failed=False)
                    | Q(is_ready=False, is_processing=False, is_failed=True)
                    | Q(is_ready=False, is_processing=False, is_failed=False)
                ),
            ),
            # archived_at can't be NULL if is_ready is True
            CheckConstraint(
                check=(
                    Q(archived_at__isnull=False, is_ready=True)
                    | Q(archived_at__isnull=True, is_ready=False)
                ),
                name="coolurl_archived_at_vs_ready",
            ),
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__show_local_before_save = self.show_local

    def __str__(self) -> str:
        return self.url

    @cached_property
    def cooler(self) -> Cooler:
        return Cooler.build(self)

    @cached_property
    def hash(self) -> str:
        return md5(self.url.encode()).hexdigest()

    @cached_property
    def parsed(self) -> ParseResult:
        return urlparse(self.url)

    @property
    def as_local(self) -> str:
        return self.cooler.local_markup

    @property
    def as_remote(self) -> str:
        return self.cooler.remote_markup

    @property
    def markup(self) -> str:
        if self.is_ready and self.show_local:
            return self.as_local
        return self.as_remote

    def cool(self) -> None:  # pragma: no cover
        return self.cooler.cool()

    def mark_as_ready(self) -> None:
        self.is_ready = True
        self.is_failed = False
        self.is_processing = False
        self.archived_at = timezone.now()
        self.save(
            update_fields=(
                "is_ready",
                "is_failed",
                "is_processing",
                "archived_at",
            )
        )
        self.logger.info("URL successfully cooled: %s", self)
        self.logger.info("Triggering is_ready() signal")
        is_ready.send(sender=self.__class__, cool_url=self)

    def mark_as_processing(self) -> None:
        self.is_ready = False
        self.is_failed = False
        self.is_processing = True
        self.archived_at = None
        self.save(
            update_fields=(
                "is_ready",
                "is_failed",
                "is_processing",
                "archived_at",
            )
        )
        self.logger.info("Triggering is_processing() signal")
        is_processing.send(sender=self.__class__, cool_url=self)

    def mark_as_failed(self) -> None:
        self.logger.error("Failed to cool %s", self)
        self.is_ready = False
        self.is_failed = True
        self.is_processing = False
        self.archived_at = None
        self.save(
            update_fields=(
                "is_ready",
                "is_failed",
                "is_processing",
                "archived_at",
            )
        )
        self.logger.info("Triggering has_failed() signal")
        has_failed.send(sender=self.__class__, cool_url=self)

    def reset(self) -> None:
        self.is_ready = False
        self.is_failed = False
        self.is_processing = False
        self.archived_at = None
        self.save(
            update_fields=(
                "is_ready",
                "is_failed",
                "is_processing",
                "archived_at",
            )
        )
        rmtree(self.cooler.target_dir)

    def save(self, *args, **kwargs):
        """
        We override .save() so we can issue signals about any change of state.
        """

        was_created = not bool(self.pk)

        show_local_enabled = False
        if self.__show_local_before_save is False and self.show_local is True:
            show_local_enabled = True

        super().save(*args, **kwargs)

        if was_created:
            new_url_created.send(sender=self.__class__, cool_url=self)

        if show_local_enabled:
            show_local_was_enabled.send(sender=self.__class__, cool_url=self)
            self.__show_local_before_save = True
