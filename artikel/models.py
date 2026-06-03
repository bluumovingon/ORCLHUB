from django.db import models

class Kategori(models.Model):
    nama = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.nama)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Daftar Kategori"

class Artikel(models.Model):
    judul = models.CharField(max_length=200)
    penulis = models.CharField(max_length=100)
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True, blank=True, related_name='artikels')
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

