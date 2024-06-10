from django.contrib import admin
from django.templatetags.static import static
from django.utils.html import format_html

from .models import CoolUrl


class CoolUrlAdmin(admin.ModelAdmin):
    list_display = (
        "url",
        "link_",
        "is_processing",
        "is_ready",
        "is_failed",
        "archived_at",
        "show_local",
        "is_embedded",
        "last_http_check_state",
        "last_http_check_time",
    )
    list_filter = (
        "is_processing",
        "is_ready",
        "is_failed",
        "show_local",
        "is_embedded",
        "last_http_check_state",
        "last_http_check_time",
    )
    ordering = ("-pk",)
    search_fields = ("url",)
    list_per_page = 150

    def get_readonly_fields(
        self,
        request,
        obj: CoolUrl | None = None,
    ) -> tuple[str, ...]:
        r = []
        for field in CoolUrl._meta.fields:
            if not field.editable:
                r.append(field.name)
        return tuple(r)

    def link_(self, obj: CoolUrl) -> str:
        return format_html(
            '<a href="{}"><img src="{}" alt="An eye icon" title="View link" /></a>',  # NOQA: E501
            obj.url,
            static("admin/img/icon-viewlink.svg"),
        )


admin.site.register(CoolUrl, CoolUrlAdmin)
