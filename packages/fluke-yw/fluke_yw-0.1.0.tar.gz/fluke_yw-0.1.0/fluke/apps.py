from django.apps import AppConfig
from django.core import checks
from django.utils.translation import ugettext_lazy as _
import fluke

# XAdminConfig
# FlukeConfig

class FlukeConfig(AppConfig):
    """Simple AppConfig which does not do automatic discovery."""

    name = 'fluke'
    verbose_name = _("Administration")

    def ready(self):
        self.module.autodiscover()
        setattr(fluke, 'site', fluke.site)
