from django import forms
from django.utils.translation import gettext_lazy as _

from .models import BillOfMaterials, BOMLine, ProductionOrder, ProductionBatch, BatchIngredient

class BillOfMaterialsForm(forms.ModelForm):
    class Meta:
        model = BillOfMaterials
        fields = ['name', 'code', 'output_quantity', 'notes', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'code': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'output_quantity': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'notes': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle'}),
        }

class BOMLineForm(forms.ModelForm):
    class Meta:
        model = BOMLine
        fields = ['bom', 'description', 'quantity', 'unit']
        widgets = {
            'bom': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'description': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'quantity': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'unit': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
        }

class ProductionOrderForm(forms.ModelForm):
    class Meta:
        model = ProductionOrder
        fields = ['order_number', 'bom', 'quantity', 'batch_number', 'expiry_date', 'status', 'start_date', 'end_date', 'notes']
        widgets = {
            'order_number': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'bom': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'quantity': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'batch_number': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'expiry_date': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'start_date': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'date'}),
            'end_date': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
        }

class ProductionBatchForm(forms.ModelForm):
    class Meta:
        model = ProductionBatch
        fields = ['batch_number', 'production_order', 'bom', 'quantity_produced', 'production_date', 'expiry_date', 'quality_status', 'notes']
        widgets = {
            'batch_number': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'production_order': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'bom': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'quantity_produced': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number', 'step': '0.01'}),
            'production_date': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'date'}),
            'expiry_date': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'date'}),
            'quality_status': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'notes': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
        }

class BatchIngredientForm(forms.ModelForm):
    class Meta:
        model = BatchIngredient
        fields = ['batch', 'description', 'supplier_lot', 'quantity_used', 'unit']
        widgets = {
            'batch': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'description': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'supplier_lot': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'quantity_used': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number', 'step': '0.01'}),
            'unit': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
        }
