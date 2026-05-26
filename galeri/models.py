from django.db import models

class Helm(models.Model):
    nama_pembalap = models.CharField(max_length=100)
    judul_desain = models.CharField(max_length=200)
    tahun = models.IntegerField()
    sasis = models.CharField(max_length=50)
    balapan_berkesan = models.CharField(max_length=200)
    gambar_url = models.URLField(max_length=500, help_text="Link URL gambar helm")
    deskripsi = models.TextField()

    def __str__(self):
        return f"{self.nama_pembalap} - {self.judul_desain} ({self.tahun})"

    class Meta:
        verbose_name = "Helm Pembalap"
        verbose_name_plural = "Daftar Helm Pembalap"
        ordering = ['-tahun']
