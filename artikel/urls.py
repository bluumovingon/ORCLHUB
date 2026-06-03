from django.urls import path
from . import views

app_name = 'artikel'

urlpatterns = [
    # Public Routes
    path('', views.artikel_list, name='artikel_list'),
    path('<int:artikel_id>/', views.artikel_detail, name='artikel_detail'),
    
    # Article CRUD (Admin & Editor)
    path('tulis/', views.artikel_tulis, name='artikel_tulis'),
    path('<int:artikel_id>/edit/', views.artikel_edit, name='artikel_edit'),
    path('<int:artikel_id>/hapus/', views.artikel_delete, name='artikel_delete'),
    
    # Admin Routes - Kategori CRUD
    path('kategori/', views.admin_kategori_list, name='admin_kategori_list'),
    path('kategori/buat/', views.admin_kategori_create, name='admin_kategori_create'),
    path('kategori/<slug:slug>/edit/', views.admin_kategori_edit, name='admin_kategori_edit'),
    path('kategori/<slug:slug>/hapus/', views.admin_kategori_delete, name='admin_kategori_delete'),
    
    # Admin Routes - User Management
    path('users/', views.admin_user_list, name='admin_user_list'),
    path('users/<int:user_id>/edit/', views.admin_user_edit, name='admin_user_edit'),
    path('users/<int:user_id>/hapus/', views.admin_user_delete, name='admin_user_delete'),
]
