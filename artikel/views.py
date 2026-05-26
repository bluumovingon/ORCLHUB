from django.shortcuts import render, get_object_or_404, redirect
from .models import Artikel
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='accounts:login')
def artikel_list(request):
    query = request.GET.get('q', '')
    kategori = request.GET.get('category', '')
    artikels = Artikel.objects.all()

    if query:
        artikels = artikels.filter(judul__icontains=query) | artikels.filter(ringkasan__icontains=query) | artikels.filter(konten__icontains=query)
    if kategori:
        artikels = artikels.filter(kategori=kategori)

    return render(request, 'artikel_list.html', {
        'artikels': artikels,
        'query': query,
        'selected_category': kategori,
        'categories': [c[0] for c in Artikel.KATEGORI_CHOICES]
    })

@login_required(login_url='accounts:login')
def artikel_detail(request, artikel_id):
    artikel = get_object_or_404(Artikel, id=artikel_id)
    # Get related articles
    related_artikels = Artikel.objects.exclude(id=artikel_id)[:3]
    return render(request, 'artikel_detail.html', {
        'artikel': artikel,
        'related_artikels': related_artikels
    })

@login_required(login_url='accounts:login')
def artikel_tulis(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        penulis = request.POST.get('penulis')
        kategori = request.POST.get('kategori')
        ringkasan = request.POST.get('ringkasan')
        konten = request.POST.get('konten')
        gambar_url = request.POST.get('gambar_url')

        if not gambar_url:
            # Gambar fallback Red Bull
            gambar_url = "https://images.unsplash.com/photo-1610427771746-860882e36785?q=80&w=800&auto=format&fit=crop"

        try:
            Artikel.objects.create(
                judul=judul,
                penulis=penulis,
                kategori=kategori,
                ringkasan=ringkasan,
                konten=konten,
                gambar_url=gambar_url
            )
            messages.success(request, f"Sukses! Artikel '{judul}' berhasil diterbitkan di Paddock Hub!")
            return redirect('artikel:artikel_list')
        except Exception as e:
            messages.error(request, f"Gagal menerbitkan artikel: {e}")
            
    return render(request, 'artikel_tulis.html', {
        'categories': [c[0] for c in Artikel.KATEGORI_CHOICES]
    })

@login_required(login_url='accounts:login')
def artikel_edit(request, artikel_id):
    artikel = get_object_or_404(Artikel, id=artikel_id)
    
    if request.method == 'POST':
        artikel.judul = request.POST.get('judul')
        artikel.penulis = request.POST.get('penulis')
        artikel.kategori = request.POST.get('kategori')
        artikel.ringkasan = request.POST.get('ringkasan')
        artikel.konten = request.POST.get('konten')
        
        gambar_url = request.POST.get('gambar_url')
        if not gambar_url:
            gambar_url = "https://images.unsplash.com/photo-1610427771746-860882e36785?q=80&w=800&auto=format&fit=crop"
        artikel.gambar_url = gambar_url
        
        try:
            artikel.save()
            messages.success(request, f"Artikel '{artikel.judul}' berhasil diperbarui!")
            return redirect('artikel:artikel_detail', artikel_id=artikel.id)
        except Exception as e:
            messages.error(request, f"Gagal memperbarui artikel: {e}")
            
    return render(request, 'artikel_tulis.html', {
        'artikel': artikel,
        'categories': [c[0] for c in Artikel.KATEGORI_CHOICES]
    })

@login_required(login_url='accounts:login')
def artikel_delete(request, artikel_id):
    artikel = get_object_or_404(Artikel, id=artikel_id)
    if request.method == 'POST':
        judul = artikel.judul
        artikel.delete()
        messages.success(request, f"Artikel '{judul}' telah berhasil dihapus.")
        return redirect('artikel:artikel_list')
        
    return render(request, 'artikel_delete.html', {'artikel': artikel})
