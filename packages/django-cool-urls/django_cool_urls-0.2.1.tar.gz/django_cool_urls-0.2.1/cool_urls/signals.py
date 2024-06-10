from django.dispatch import Signal


new_url_created = Signal()
is_processing = Signal()
is_ready = Signal()
has_failed = Signal()
show_local_was_enabled = Signal()
