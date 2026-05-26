from django.urls import path
from . import views

app_name = 'artikel'

urlpatterns = [
    path('', views.artikel_list, name='artikel_list'),
    path('<int:artikel_id>/', views.artikel_detail, name='artikel_detail'),
    path('tulis/', views.artikel_tulis, name='artikel_tulis'),
    path('<int:artikel_id>/edit/', views.artikel_edit, name='artikel_edit'),
    path('<int:artikel_id>/hapus/', views.artikel_delete, name='artikel_delete'),
]
