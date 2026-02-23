from django.contrib import admin

from .models import BillOfMaterials, BOMLine, ProductionOrder

@admin.register(BillOfMaterials)
class BillOfMaterialsAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'output_quantity', 'notes', 'is_active']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(BOMLine)
class BOMLineAdmin(admin.ModelAdmin):
    list_display = ['bom', 'description', 'quantity', 'unit']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(ProductionOrder)
class ProductionOrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'bom', 'quantity', 'status', 'start_date']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']

