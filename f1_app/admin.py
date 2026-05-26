from django.contrib import admin
from artikel.models import Artikel
from galeri.models import Helm

@admin.register(Artikel)
class ArtikelAdmin(admin.ModelAdmin):
    list_display = ('judul', 'penulis', 'kategori', 'tanggal_dibuat')
    list_filter = ('kategori', 'tanggal_dibuat')
    search_fields = ('judul', 'penulis', 'konten')
    ordering = ('-tanggal_dibuat',)

@admin.register(Helm)
class HelmAdmin(admin.ModelAdmin):
    list_display = ('nama_pembalap', 'judul_desain', 'tahun', 'sasis', 'balapan_berkesan')
    list_filter = ('nama_pembalap', 'tahun', 'sasis')
    search_fields = ('nama_pembalap', 'judul_desain', 'deskripsi')
    ordering = ('-tahun',)
