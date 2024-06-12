from cms.models.pluginmodel import CMSPlugin
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from .settings import POPUP_LIST_TEMPLATES


class PopupPluginModel(CMSPlugin):
    display_delay = models.IntegerField(_("Display after X seconds"), default=0)
    can_reopen_popup = models.BooleanField(
        _("Allow the popup to be reopened if it is closed"), default=False
    )

    popup_template = models.CharField(
        verbose_name=_("Popup template"),
        choices=POPUP_LIST_TEMPLATES,
        max_length=300,
        blank=False,
    )

    def get_page_url(self):
        language = f"[{self.language}]" if self.language else ""
        try:
            page_or_placeholder_slot = mark_safe(
                '<a href="'
                + self.page.get_absolute_url()
                + '">'
                + self.page.get_page_title()
                + "</a>"
            )
        except AttributeError:
            if self.placeholder:
                page_or_placeholder_slot = self.placeholder.get_label()
                if self.placeholder.static_public.exists():
                    page_or_placeholder_slot += " (" + _("published") + ")"
                else:
                    page_or_placeholder_slot += " (" + _("draft") + ")"
            else:
                page_or_placeholder_slot = _("(unknown)")
        return f"{language} {page_or_placeholder_slot}"

    get_page_url.short_description = _("Page or static placeholder")

    class Meta:
        verbose_name = _("Popup")
        verbose_name_plural = _("Popups")

    def __unicode__(self):
        return _("Popup ({})").format(self.get_popup_template_display())
