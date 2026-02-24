"""Tests for manufacturing models."""
import pytest
from django.utils import timezone

from manufacturing.models import BillOfMaterials, BOMLine, ProductionOrder


@pytest.mark.django_db
class TestBillOfMaterials:
    """BillOfMaterials model tests."""

    def test_create(self, bill_of_materials):
        """Test BillOfMaterials creation."""
        assert bill_of_materials.pk is not None
        assert bill_of_materials.is_deleted is False

    def test_str(self, bill_of_materials):
        """Test string representation."""
        assert str(bill_of_materials) is not None
        assert len(str(bill_of_materials)) > 0

    def test_soft_delete(self, bill_of_materials):
        """Test soft delete."""
        pk = bill_of_materials.pk
        bill_of_materials.is_deleted = True
        bill_of_materials.deleted_at = timezone.now()
        bill_of_materials.save()
        assert not BillOfMaterials.objects.filter(pk=pk).exists()
        assert BillOfMaterials.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, bill_of_materials):
        """Test default queryset excludes deleted."""
        bill_of_materials.is_deleted = True
        bill_of_materials.deleted_at = timezone.now()
        bill_of_materials.save()
        assert BillOfMaterials.objects.filter(hub_id=hub_id).count() == 0

    def test_toggle_active(self, bill_of_materials):
        """Test toggling is_active."""
        original = bill_of_materials.is_active
        bill_of_materials.is_active = not original
        bill_of_materials.save()
        bill_of_materials.refresh_from_db()
        assert bill_of_materials.is_active != original


@pytest.mark.django_db
class TestBOMLine:
    """BOMLine model tests."""

    def test_create(self, bom_line):
        """Test BOMLine creation."""
        assert bom_line.pk is not None
        assert bom_line.is_deleted is False

    def test_soft_delete(self, bom_line):
        """Test soft delete."""
        pk = bom_line.pk
        bom_line.is_deleted = True
        bom_line.deleted_at = timezone.now()
        bom_line.save()
        assert not BOMLine.objects.filter(pk=pk).exists()
        assert BOMLine.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, bom_line):
        """Test default queryset excludes deleted."""
        bom_line.is_deleted = True
        bom_line.deleted_at = timezone.now()
        bom_line.save()
        assert BOMLine.objects.filter(hub_id=hub_id).count() == 0


@pytest.mark.django_db
class TestProductionOrder:
    """ProductionOrder model tests."""

    def test_create(self, production_order):
        """Test ProductionOrder creation."""
        assert production_order.pk is not None
        assert production_order.is_deleted is False

    def test_str(self, production_order):
        """Test string representation."""
        assert str(production_order) is not None
        assert len(str(production_order)) > 0

    def test_soft_delete(self, production_order):
        """Test soft delete."""
        pk = production_order.pk
        production_order.is_deleted = True
        production_order.deleted_at = timezone.now()
        production_order.save()
        assert not ProductionOrder.objects.filter(pk=pk).exists()
        assert ProductionOrder.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, production_order):
        """Test default queryset excludes deleted."""
        production_order.is_deleted = True
        production_order.deleted_at = timezone.now()
        production_order.save()
        assert ProductionOrder.objects.filter(hub_id=hub_id).count() == 0


