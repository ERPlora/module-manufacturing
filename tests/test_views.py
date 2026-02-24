"""Tests for manufacturing views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('manufacturing:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('manufacturing:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('manufacturing:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestBillOfMaterialsViews:
    """BillOfMaterials view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('manufacturing:bill_of_materialses_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('manufacturing:bill_of_materialses_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('manufacturing:bill_of_materialses_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('manufacturing:bill_of_materialses_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('manufacturing:bill_of_materialses_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('manufacturing:bill_of_materialses_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('manufacturing:bill_of_materials_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('manufacturing:bill_of_materials_add')
        data = {
            'name': 'New Name',
            'code': 'New Code',
            'output_quantity': '100.00',
            'notes': 'Test description',
            'is_active': 'on',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, bill_of_materials):
        """Test edit form loads."""
        url = reverse('manufacturing:bill_of_materials_edit', args=[bill_of_materials.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, bill_of_materials):
        """Test editing via POST."""
        url = reverse('manufacturing:bill_of_materials_edit', args=[bill_of_materials.pk])
        data = {
            'name': 'Updated Name',
            'code': 'Updated Code',
            'output_quantity': '100.00',
            'notes': 'Test description',
            'is_active': '',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, bill_of_materials):
        """Test soft delete via POST."""
        url = reverse('manufacturing:bill_of_materials_delete', args=[bill_of_materials.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        bill_of_materials.refresh_from_db()
        assert bill_of_materials.is_deleted is True

    def test_toggle_status(self, auth_client, bill_of_materials):
        """Test toggle active status."""
        url = reverse('manufacturing:bill_of_materials_toggle_status', args=[bill_of_materials.pk])
        original = bill_of_materials.is_active
        response = auth_client.post(url)
        assert response.status_code == 200
        bill_of_materials.refresh_from_db()
        assert bill_of_materials.is_active != original

    def test_bulk_delete(self, auth_client, bill_of_materials):
        """Test bulk delete."""
        url = reverse('manufacturing:bill_of_materialses_bulk_action')
        response = auth_client.post(url, {'ids': str(bill_of_materials.pk), 'action': 'delete'})
        assert response.status_code == 200
        bill_of_materials.refresh_from_db()
        assert bill_of_materials.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('manufacturing:bill_of_materialses_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestBOMLineViews:
    """BOMLine view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('manufacturing:bom_lines_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('manufacturing:bom_lines_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('manufacturing:bom_lines_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('manufacturing:bom_lines_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('manufacturing:bom_lines_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('manufacturing:bom_lines_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('manufacturing:bom_line_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('manufacturing:bom_line_add')
        data = {
            'description': 'New Description',
            'quantity': '100.00',
            'unit': 'New Unit',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, bom_line):
        """Test edit form loads."""
        url = reverse('manufacturing:bom_line_edit', args=[bom_line.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, bom_line):
        """Test editing via POST."""
        url = reverse('manufacturing:bom_line_edit', args=[bom_line.pk])
        data = {
            'description': 'Updated Description',
            'quantity': '100.00',
            'unit': 'Updated Unit',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, bom_line):
        """Test soft delete via POST."""
        url = reverse('manufacturing:bom_line_delete', args=[bom_line.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        bom_line.refresh_from_db()
        assert bom_line.is_deleted is True

    def test_bulk_delete(self, auth_client, bom_line):
        """Test bulk delete."""
        url = reverse('manufacturing:bom_lines_bulk_action')
        response = auth_client.post(url, {'ids': str(bom_line.pk), 'action': 'delete'})
        assert response.status_code == 200
        bom_line.refresh_from_db()
        assert bom_line.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('manufacturing:bom_lines_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestProductionOrderViews:
    """ProductionOrder view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('manufacturing:production_orders_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('manufacturing:production_orders_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('manufacturing:production_orders_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('manufacturing:production_orders_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('manufacturing:production_orders_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('manufacturing:production_orders_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('manufacturing:production_order_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('manufacturing:production_order_add')
        data = {
            'order_number': 'New Order Number',
            'quantity': '100.00',
            'status': 'New Status',
            'start_date': '2025-01-15',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, production_order):
        """Test edit form loads."""
        url = reverse('manufacturing:production_order_edit', args=[production_order.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, production_order):
        """Test editing via POST."""
        url = reverse('manufacturing:production_order_edit', args=[production_order.pk])
        data = {
            'order_number': 'Updated Order Number',
            'quantity': '100.00',
            'status': 'Updated Status',
            'start_date': '2025-01-15',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, production_order):
        """Test soft delete via POST."""
        url = reverse('manufacturing:production_order_delete', args=[production_order.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        production_order.refresh_from_db()
        assert production_order.is_deleted is True

    def test_bulk_delete(self, auth_client, production_order):
        """Test bulk delete."""
        url = reverse('manufacturing:production_orders_bulk_action')
        response = auth_client.post(url, {'ids': str(production_order.pk), 'action': 'delete'})
        assert response.status_code == 200
        production_order.refresh_from_db()
        assert production_order.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('manufacturing:production_orders_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('manufacturing:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('manufacturing:settings')
        response = client.get(url)
        assert response.status_code == 302

