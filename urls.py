from django.urls import path
from . import views

app_name = 'manufacturing'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('bom/', views.bom, name='bom'),
    path('production/', views.production, name='production'),
    path('settings/', views.settings, name='settings'),
]
