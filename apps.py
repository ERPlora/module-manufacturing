from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ManufacturingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'manufacturing'
    label = 'manufacturing'
    verbose_name = _('Manufacturing & BOM')

    def ready(self):
        pass
