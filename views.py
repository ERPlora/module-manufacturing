"""
Manufacturing & BOM Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import BillOfMaterials, BOMLine, ProductionOrder

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('manufacturing', 'dashboard')
@htmx_view('manufacturing/pages/index.html', 'manufacturing/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_bill_of_materialses': BillOfMaterials.objects.filter(hub_id=hub_id, is_deleted=False).count(),
        'total_bom_lines': BOMLine.objects.filter(hub_id=hub_id, is_deleted=False).count(),
        'total_production_orders': ProductionOrder.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# BillOfMaterials
# ======================================================================

BILL_OF_MATERIALS_SORT_FIELDS = {
    'code': 'code',
    'name': 'name',
    'is_active': 'is_active',
    'output_quantity': 'output_quantity',
    'notes': 'notes',
    'created_at': 'created_at',
}

def _build_bill_of_materialses_context(hub_id, per_page=10):
    qs = BillOfMaterials.objects.filter(hub_id=hub_id, is_deleted=False).order_by('code')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'bill_of_materialses': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'code',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_bill_of_materialses_list(request, hub_id, per_page=10):
    ctx = _build_bill_of_materialses_context(hub_id, per_page)
    return django_render(request, 'manufacturing/partials/bill_of_materialses_list.html', ctx)

@login_required
@with_module_nav('manufacturing', 'bom')
@htmx_view('manufacturing/pages/bill_of_materialses.html', 'manufacturing/partials/bill_of_materialses_content.html')
def bill_of_materialses_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'code')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = BillOfMaterials.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(name__icontains=search_query) | Q(code__icontains=search_query) | Q(notes__icontains=search_query))

    order_by = BILL_OF_MATERIALS_SORT_FIELDS.get(sort_field, 'code')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['code', 'name', 'is_active', 'output_quantity', 'notes']
        headers = ['Code', 'Name', 'Is Active', 'Output Quantity', 'Notes']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='bill_of_materialses.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='bill_of_materialses.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'manufacturing/partials/bill_of_materialses_list.html', {
            'bill_of_materialses': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'bill_of_materialses': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def bill_of_materials_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        code = request.POST.get('code', '').strip()
        output_quantity = request.POST.get('output_quantity', '0') or '0'
        notes = request.POST.get('notes', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        obj = BillOfMaterials(hub_id=hub_id)
        obj.name = name
        obj.code = code
        obj.output_quantity = output_quantity
        obj.notes = notes
        obj.is_active = is_active
        obj.save()
        return _render_bill_of_materialses_list(request, hub_id)
    return django_render(request, 'manufacturing/partials/panel_bill_of_materials_add.html', {})

@login_required
def bill_of_materials_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(BillOfMaterials, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '').strip()
        obj.code = request.POST.get('code', '').strip()
        obj.output_quantity = request.POST.get('output_quantity', '0') or '0'
        obj.notes = request.POST.get('notes', '').strip()
        obj.is_active = request.POST.get('is_active') == 'on'
        obj.save()
        return _render_bill_of_materialses_list(request, hub_id)
    return django_render(request, 'manufacturing/partials/panel_bill_of_materials_edit.html', {'obj': obj})

@login_required
@require_POST
def bill_of_materials_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(BillOfMaterials, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_bill_of_materialses_list(request, hub_id)

@login_required
@require_POST
def bill_of_materials_toggle_status(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(BillOfMaterials, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_active = not obj.is_active
    obj.save(update_fields=['is_active', 'updated_at'])
    return _render_bill_of_materialses_list(request, hub_id)

@login_required
@require_POST
def bill_of_materialses_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = BillOfMaterials.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'activate':
        qs.update(is_active=True)
    elif action == 'deactivate':
        qs.update(is_active=False)
    elif action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_bill_of_materialses_list(request, hub_id)


# ======================================================================
# BOMLine
# ======================================================================

BOM_LINE_SORT_FIELDS = {
    'bom': 'bom',
    'quantity': 'quantity',
    'description': 'description',
    'unit': 'unit',
    'created_at': 'created_at',
}

def _build_bom_lines_context(hub_id, per_page=10):
    qs = BOMLine.objects.filter(hub_id=hub_id, is_deleted=False).order_by('bom')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'bom_lines': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'bom',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_bom_lines_list(request, hub_id, per_page=10):
    ctx = _build_bom_lines_context(hub_id, per_page)
    return django_render(request, 'manufacturing/partials/bom_lines_list.html', ctx)

@login_required
@with_module_nav('manufacturing', 'bom')
@htmx_view('manufacturing/pages/bom_lines.html', 'manufacturing/partials/bom_lines_content.html')
def bom_lines_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'bom')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = BOMLine.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(description__icontains=search_query) | Q(unit__icontains=search_query))

    order_by = BOM_LINE_SORT_FIELDS.get(sort_field, 'bom')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['bom', 'quantity', 'description', 'unit']
        headers = ['BillOfMaterials', 'Quantity', 'Description', 'Unit']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='bom_lines.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='bom_lines.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'manufacturing/partials/bom_lines_list.html', {
            'bom_lines': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'bom_lines': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def bom_line_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        description = request.POST.get('description', '').strip()
        quantity = request.POST.get('quantity', '0') or '0'
        unit = request.POST.get('unit', '').strip()
        obj = BOMLine(hub_id=hub_id)
        obj.description = description
        obj.quantity = quantity
        obj.unit = unit
        obj.save()
        return _render_bom_lines_list(request, hub_id)
    return django_render(request, 'manufacturing/partials/panel_bom_line_add.html', {})

@login_required
def bom_line_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(BOMLine, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.description = request.POST.get('description', '').strip()
        obj.quantity = request.POST.get('quantity', '0') or '0'
        obj.unit = request.POST.get('unit', '').strip()
        obj.save()
        return _render_bom_lines_list(request, hub_id)
    return django_render(request, 'manufacturing/partials/panel_bom_line_edit.html', {'obj': obj})

@login_required
@require_POST
def bom_line_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(BOMLine, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_bom_lines_list(request, hub_id)

@login_required
@require_POST
def bom_lines_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = BOMLine.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_bom_lines_list(request, hub_id)


# ======================================================================
# ProductionOrder
# ======================================================================

PRODUCTION_ORDER_SORT_FIELDS = {
    'order_number': 'order_number',
    'bom': 'bom',
    'status': 'status',
    'quantity': 'quantity',
    'start_date': 'start_date',
    'end_date': 'end_date',
    'created_at': 'created_at',
}

def _build_production_orders_context(hub_id, per_page=10):
    qs = ProductionOrder.objects.filter(hub_id=hub_id, is_deleted=False).order_by('order_number')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'production_orders': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'order_number',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_production_orders_list(request, hub_id, per_page=10):
    ctx = _build_production_orders_context(hub_id, per_page)
    return django_render(request, 'manufacturing/partials/production_orders_list.html', ctx)

@login_required
@with_module_nav('manufacturing', 'production')
@htmx_view('manufacturing/pages/production_orders.html', 'manufacturing/partials/production_orders_content.html')
def production_orders_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'order_number')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = ProductionOrder.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(order_number__icontains=search_query) | Q(status__icontains=search_query) | Q(notes__icontains=search_query))

    order_by = PRODUCTION_ORDER_SORT_FIELDS.get(sort_field, 'order_number')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['order_number', 'bom', 'status', 'quantity', 'start_date', 'end_date']
        headers = ['Order Number', 'BillOfMaterials', 'Status', 'Quantity', 'Start Date', 'End Date']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='production_orders.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='production_orders.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'manufacturing/partials/production_orders_list.html', {
            'production_orders': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'production_orders': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def production_order_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        order_number = request.POST.get('order_number', '').strip()
        quantity = request.POST.get('quantity', '0') or '0'
        status = request.POST.get('status', '').strip()
        start_date = request.POST.get('start_date') or None
        end_date = request.POST.get('end_date') or None
        notes = request.POST.get('notes', '').strip()
        obj = ProductionOrder(hub_id=hub_id)
        obj.order_number = order_number
        obj.quantity = quantity
        obj.status = status
        obj.start_date = start_date
        obj.end_date = end_date
        obj.notes = notes
        obj.save()
        return _render_production_orders_list(request, hub_id)
    return django_render(request, 'manufacturing/partials/panel_production_order_add.html', {})

@login_required
def production_order_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(ProductionOrder, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.order_number = request.POST.get('order_number', '').strip()
        obj.quantity = request.POST.get('quantity', '0') or '0'
        obj.status = request.POST.get('status', '').strip()
        obj.start_date = request.POST.get('start_date') or None
        obj.end_date = request.POST.get('end_date') or None
        obj.notes = request.POST.get('notes', '').strip()
        obj.save()
        return _render_production_orders_list(request, hub_id)
    return django_render(request, 'manufacturing/partials/panel_production_order_edit.html', {'obj': obj})

@login_required
@require_POST
def production_order_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(ProductionOrder, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_production_orders_list(request, hub_id)

@login_required
@require_POST
def production_orders_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = ProductionOrder.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_production_orders_list(request, hub_id)


@login_required
@with_module_nav('manufacturing', 'settings')
@htmx_view('manufacturing/pages/settings.html', 'manufacturing/partials/settings_content.html')
def settings_view(request):
    return {}

