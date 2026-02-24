from django.contrib import admin

from .models import BillOfMaterials, BOMLine, ProductionOrder

@admin.register(BillOfMaterials)
class BillOfMaterialsAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'output_quantity', 'is_active', 'created_at']
    search_fields = ['name', 'code', 'notes']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(BOMLine)
class BOMLineAdmin(admin.ModelAdmin):
    list_display = ['bom', 'description', 'quantity', 'unit', 'created_at']
    search_fields = ['description', 'unit']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ProductionOrder)
class ProductionOrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'bom', 'quantity', 'status', 'start_date', 'created_at']
    search_fields = ['order_number', 'status', 'notes']
    readonly_fields = ['created_at', 'updated_at']

