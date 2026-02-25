from django.contrib import admin

from .models import BillOfMaterials, BOMLine, ProductionOrder, ProductionBatch, BatchIngredient

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
    list_display = ['order_number', 'batch_number', 'bom', 'quantity', 'status', 'start_date', 'created_at']
    search_fields = ['order_number', 'batch_number', 'status', 'notes']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ProductionBatch)
class ProductionBatchAdmin(admin.ModelAdmin):
    list_display = ['batch_number', 'production_order', 'quantity_produced', 'production_date', 'quality_status', 'created_at']
    search_fields = ['batch_number', 'notes']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(BatchIngredient)
class BatchIngredientAdmin(admin.ModelAdmin):
    list_display = ['batch', 'description', 'supplier_lot', 'quantity_used', 'unit', 'created_at']
    search_fields = ['description', 'supplier_lot']
    readonly_fields = ['created_at', 'updated_at']
