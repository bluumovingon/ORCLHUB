from django.urls import path
from . import views

app_name = 'galeri'

urlpatterns = [
    path('', views.galeri_list, name='galeri_list'),
    path('tambah/', views.galeri_tambah, name='galeri_tambah'),
    path('<int:helm_id>/edit/', views.galeri_edit, name='galeri_edit'),
    path('<int:helm_id>/hapus/', views.galeri_delete, name='galeri_delete'),
]
