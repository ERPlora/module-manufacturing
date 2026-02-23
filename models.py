from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

PROD_STATUS = [
    ('draft', _('Draft')),
    ('confirmed', _('Confirmed')),
    ('in_progress', _('In Progress')),
    ('done', _('Done')),
    ('cancelled', _('Cancelled')),
]

class BillOfMaterials(HubBaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    code = models.CharField(max_length=50, blank=True, verbose_name=_('Code'))
    output_quantity = models.DecimalField(max_digits=10, decimal_places=2, default='1', verbose_name=_('Output Quantity'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta(HubBaseModel.Meta):
        db_table = 'manufacturing_billofmaterials'

    def __str__(self):
        return self.name


class BOMLine(HubBaseModel):
    bom = models.ForeignKey('BillOfMaterials', on_delete=models.CASCADE, related_name='lines')
    description = models.CharField(max_length=255, verbose_name=_('Description'))
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default='1', verbose_name=_('Quantity'))
    unit = models.CharField(max_length=20, blank=True, verbose_name=_('Unit'))

    class Meta(HubBaseModel.Meta):
        db_table = 'manufacturing_bomline'

    def __str__(self):
        return str(self.id)


class ProductionOrder(HubBaseModel):
    order_number = models.CharField(max_length=50, verbose_name=_('Order Number'))
    bom = models.ForeignKey('BillOfMaterials', on_delete=models.SET_NULL, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default='1', verbose_name=_('Quantity'))
    status = models.CharField(max_length=20, default='draft', choices=PROD_STATUS, verbose_name=_('Status'))
    start_date = models.DateField(null=True, blank=True, verbose_name=_('Start Date'))
    end_date = models.DateField(null=True, blank=True, verbose_name=_('End Date'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    class Meta(HubBaseModel.Meta):
        db_table = 'manufacturing_productionorder'

    def __str__(self):
        return str(self.id)

