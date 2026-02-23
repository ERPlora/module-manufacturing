    from django.utils.translation import gettext_lazy as _

    MODULE_ID = 'manufacturing'
    MODULE_NAME = _('Manufacturing & BOM')
    MODULE_VERSION = '1.0.0'
    MODULE_ICON = 'cog-outline'
    MODULE_DESCRIPTION = _('Bill of materials, production orders and recipes')
    MODULE_AUTHOR = 'ERPlora'
    MODULE_CATEGORY = 'commerce'

    MENU = {
        'label': _('Manufacturing & BOM'),
        'icon': 'cog-outline',
        'order': 17,
    }

    NAVIGATION = [
        {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('BOM'), 'icon': 'layers-outline', 'id': 'bom'},
{'label': _('Production'), 'icon': 'cog-outline', 'id': 'production'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
    ]

    DEPENDENCIES = []

    PERMISSIONS = [
        'manufacturing.view_billofmaterials',
'manufacturing.add_billofmaterials',
'manufacturing.change_billofmaterials',
'manufacturing.delete_billofmaterials',
'manufacturing.view_productionorder',
'manufacturing.add_productionorder',
'manufacturing.change_productionorder',
'manufacturing.manage_settings',
    ]
