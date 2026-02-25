from django.urls import path
from . import views

app_name = 'manufacturing'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Navigation tabs
    path('bom/', views.bill_of_materialses_list, name='bom'),
    path('production/', views.production_orders_list, name='production'),

    # BillOfMaterials
    path('bill_of_materialses/', views.bill_of_materialses_list, name='bill_of_materialses_list'),
    path('bill_of_materialses/add/', views.bill_of_materials_add, name='bill_of_materials_add'),
    path('bill_of_materialses/<uuid:pk>/edit/', views.bill_of_materials_edit, name='bill_of_materials_edit'),
    path('bill_of_materialses/<uuid:pk>/delete/', views.bill_of_materials_delete, name='bill_of_materials_delete'),
    path('bill_of_materialses/<uuid:pk>/toggle/', views.bill_of_materials_toggle_status, name='bill_of_materials_toggle_status'),
    path('bill_of_materialses/bulk/', views.bill_of_materialses_bulk_action, name='bill_of_materialses_bulk_action'),

    # BOMLine
    path('bom_lines/', views.bom_lines_list, name='bom_lines_list'),
    path('bom_lines/add/', views.bom_line_add, name='bom_line_add'),
    path('bom_lines/<uuid:pk>/edit/', views.bom_line_edit, name='bom_line_edit'),
    path('bom_lines/<uuid:pk>/delete/', views.bom_line_delete, name='bom_line_delete'),
    path('bom_lines/bulk/', views.bom_lines_bulk_action, name='bom_lines_bulk_action'),

    # ProductionOrder
    path('production_orders/', views.production_orders_list, name='production_orders_list'),
    path('production_orders/add/', views.production_order_add, name='production_order_add'),
    path('production_orders/<uuid:pk>/edit/', views.production_order_edit, name='production_order_edit'),
    path('production_orders/<uuid:pk>/delete/', views.production_order_delete, name='production_order_delete'),
    path('production_orders/bulk/', views.production_orders_bulk_action, name='production_orders_bulk_action'),

    # Production Order Detail
    path('production/<uuid:pk>/', views.production_order_detail, name='production_order_detail'),

    # Batches
    path('production/<uuid:pk>/batches/add/', views.batch_add, name='batch_add'),
    path('production/<uuid:pk>/batches/panel/', views.batch_add_panel, name='batch_add_panel'),
    path('production/<uuid:pk>/batches/<uuid:batch_pk>/delete/', views.batch_delete, name='batch_delete'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
