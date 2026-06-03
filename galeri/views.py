from django.shortcuts import render, get_object_or_404, redirect
from .models import Helm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def galeri_list(request):
    query = request.GET.get('q', '')
    helms = Helm.objects.all()

    if query:
        helms = helms.filter(nama_pembalap__icontains=query) | helms.filter(judul_desain__icontains=query) | helms.filter(sasis__icontains=query)

    return render(request, 'galeri_list.html', {
        'helms': helms,
        'query': query
    })

@login_required(login_url='accounts:login')
def galeri_tambah(request):
    if request.method == 'POST':
        nama_pembalap = request.POST.get('nama_pembalap')
        judul_desain = request.POST.get('judul_desain')
        tahun = request.POST.get('tahun')
        sasis = request.POST.get('sasis')
        balapan_berkesan = request.POST.get('balapan_berkesan')
        deskripsi = request.POST.get('deskripsi')
        gambar_url = request.POST.get('gambar_url')

        if not gambar_url:
            gambar_url = "https://images.unsplash.com/photo-1610427771746-860882e36785?q=80&w=800&auto=format&fit=crop"

        try:
            Helm.objects.create(
                nama_pembalap=nama_pembalap,
                judul_desain=judul_desain,
                tahun=tahun,
                sasis=sasis,
                balapan_berkesan=balapan_berkesan,
                deskripsi=deskripsi,
                gambar_url=gambar_url
            )
            messages.success(request, f"Sukses! Helm '{judul_desain}' berhasil ditambahkan ke Galeri!")
            return redirect('galeri:galeri_list')
        except Exception as e:
            messages.error(request, f"Gagal menambahkan helm: {e}")
            
    return render(request, 'galeri_tambah.html')

@login_required(login_url='accounts:login')
def galeri_edit(request, helm_id):
    helm = get_object_or_404(Helm, id=helm_id)
    
    if request.method == 'POST':
        helm.nama_pembalap = request.POST.get('nama_pembalap')
        helm.judul_desain = request.POST.get('judul_desain')
        helm.tahun = request.POST.get('tahun')
        helm.sasis = request.POST.get('sasis')
        helm.balapan_berkesan = request.POST.get('balapan_berkesan')
        helm.deskripsi = request.POST.get('deskripsi')
        
        gambar_url = request.POST.get('gambar_url')
        if not gambar_url:
            gambar_url = "https://images.unsplash.com/photo-1610427771746-860882e36785?q=80&w=800&auto=format&fit=crop"
        helm.gambar_url = gambar_url
        
        try:
            helm.save()
            messages.success(request, f"Data helm '{helm.judul_desain}' berhasil diperbarui!")
            return redirect('galeri:galeri_list')
        except Exception as e:
            messages.error(request, f"Gagal memperbarui helm: {e}")
            
    return render(request, 'galeri_tambah.html', {'helm': helm})

@login_required(login_url='accounts:login')
def galeri_delete(request, helm_id):
    helm = get_object_or_404(Helm, id=helm_id)
    if request.method == 'POST':
        judul = helm.judul_desain
        helm.delete()
        messages.success(request, f"Data helm '{judul}' telah berhasil dihapus.")
        return redirect('galeri:galeri_list')
        
    return render(request, 'galeri_delete.html', {'helm': helm})

