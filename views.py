"""
Manufacturing & BOM Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('manufacturing', 'dashboard')
@htmx_view('manufacturing/pages/dashboard.html', 'manufacturing/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('manufacturing', 'bom')
@htmx_view('manufacturing/pages/bom.html', 'manufacturing/partials/bom_content.html')
def bom(request):
    """BOM view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('manufacturing', 'production')
@htmx_view('manufacturing/pages/production.html', 'manufacturing/partials/production_content.html')
def production(request):
    """Production view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('manufacturing', 'settings')
@htmx_view('manufacturing/pages/settings.html', 'manufacturing/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

