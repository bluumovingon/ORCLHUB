from django.db import models

class Artikel(models.Model):
    KATEGORI_CHOICES = [
        ('Berita Tim', 'Berita Tim'),
        ('Analisis Balapan', 'Analisis Balapan'),
        ('Pembaruan Teknis', 'Pembaruan Teknis'),
        ('Opini Fans', 'Opini Fans'),
    ]

    judul = models.CharField(max_length=200)
    penulis = models.CharField(max_length=100)
    kategori = models.CharField(max_length=50, choices=KATEGORI_CHOICES, default='Berita Tim')
    ringkasan = models.TextField(max_length=500, help_text="Ringkasan singkat artikel")
    konten = models.TextField()
    gambar_url = models.URLField(max_length=500, blank=True, help_text="Link URL gambar artikel")
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul

    class Meta:
        verbose_name = "Artikel"
        verbose_name_plural = "Daftar Artikel"
        ordering = ['-tanggal_dibuat']
