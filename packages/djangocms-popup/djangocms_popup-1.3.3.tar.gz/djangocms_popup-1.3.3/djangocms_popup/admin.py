from django.contrib import admin

from .models import PopupPluginModel


@admin.register(PopupPluginModel)
class DjangocmsPopupAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_page_url",
        "display_delay",
        "can_reopen_popup",
        "popup_template",
    )

    def get_queryset(self, request):
        qs = (
            super()
            .get_queryset(request)
            .exclude(placeholder__page__publisher_is_draft=True)
        )
        return qs

    def has_add_permission(self, request, obj=None):
        return False
