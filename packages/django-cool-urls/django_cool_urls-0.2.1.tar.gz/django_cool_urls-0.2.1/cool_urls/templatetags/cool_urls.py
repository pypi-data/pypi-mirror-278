from collections.abc import Callable
from importlib import import_module

from django import template
from django.conf import settings

from ..models import CoolUrl


register = template.Library()


@register.simple_tag()
def cool_embed(url: str) -> str:
    """
    Attempts to embed the URL, assuming it's a video of some kind.
    """
    __policy_handler: Callable[[str, bool], bool] = __determine_policy()
    return CoolUrl.objects.get_or_create(
        url=url,
        defaults={
            "show_local": __policy_handler(url=url, is_embedded=True),
            "is_embedded": True,
        },
    )[0].markup


@register.simple_tag()
def cool_url(url: str) -> str:
    __policy_handler: Callable[[str, bool], bool] = __determine_policy()
    return CoolUrl.objects.get_or_create(
        url=url,
        defaults={
            "show_local": __policy_handler(url=url, is_embedded=False),
        },
    )[0].markup


def __determine_policy() -> Callable:
    """
    Return a callable that will return `True` when you want to show the locally
    archived copy as soon as it's available, and `False` when you want to show
    the remote version until you set `show_local=True` some other way.

    This callable will receive two arguments:

    url          (str)   The URL being cooled
    is_embedded  (bool)  Whether the request was to cool an embedded URL or a
                         plain one.
    """

    defined = getattr(settings, "COOL_URLS_POLICY", "REMOTE")

    if defined == "REMOTE":
        return lambda **kwargs: False

    if defined == "LOCAL":
        return lambda **kwargs: True

    parts = defined.rsplit(".", 1)
    return getattr(import_module(parts[0]), parts[1])
