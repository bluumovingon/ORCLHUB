from django.shortcuts import render, get_object_or_404, redirect
from .models import Artikel, Kategori
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from accounts.templatetags.auth_extras import is_admin, is_editor, is_admin_or_editor

# ----------------- PUBLIC VIEWS -----------------

def artikel_list(request):
    query = request.GET.get('q', '')
    kategori_name = request.GET.get('category', '')
    artikels = Artikel.objects.all()

    if query:
        artikels = (
            artikels.filter(judul__icontains=query) | 
            artikels.filter(ringkasan__icontains=query) | 
            artikels.filter(konten__icontains=query)
        )
    if kategori_name:
        artikels = artikels.filter(kategori__nama=kategori_name)

    return render(request, 'artikel_list.html', {
        'artikels': artikels,
        'query': query,
        'selected_category': kategori_name,
        'categories': Kategori.objects.all()
    })

def artikel_detail(request, artikel_id):
    artikel = get_object_or_404(Artikel, id=artikel_id)
    # Get related articles
    related_artikels = Artikel.objects.exclude(id=artikel_id)[:3]
    return render(request, 'artikel_detail.html', {
        'artikel': artikel,
        'related_artikels': related_artikels
    })


# ----------------- ARTICLE CRUD (Admin/Editor) -----------------

@login_required(login_url='accounts:login')
@user_passes_test(is_admin_or_editor, login_url='/')
def artikel_tulis(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        penulis = request.POST.get('penulis')
        kategori_name = request.POST.get('kategori')
        ringkasan = request.POST.get('ringkasan')
        konten = request.POST.get('konten')
        gambar_url = request.POST.get('gambar_url')
    
        if not gambar_url:
            # Gambar fallback Red Bull
            gambar_url = "https://images.unsplash.com/photo-1610427771746-860882e36785?q=80&w=800&auto=format&fit=crop"

        kategori_obj = Kategori.objects.filter(nama=kategori_name).first()

        try:
            Artikel.objects.create(
                judul=judul,
                penulis=penulis,
                kategori=kategori_obj,
                ringkasan=ringkasan,
                konten=konten,
                gambar_url=gambar_url
            )
            messages.success(request, f"Sukses! Artikel '{judul}' berhasil diterbitkan di Paddock Hub!")
            return redirect('artikel:artikel_list')
        except Exception as e:
            messages.error(request, f"Gagal menerbitkan artikel: {e}")
            
    return render(request, 'artikel_tulis.html', {
        'categories': Kategori.objects.all()
    })

@login_required(login_url='accounts:login')
@user_passes_test(is_admin_or_editor, login_url='/')
def artikel_edit(request, artikel_id):
    artikel = get_object_or_404(Artikel, id=artikel_id)
    
    if request.method == 'POST':
        artikel.judul = request.POST.get('judul')
        artikel.penulis = request.POST.get('penulis')
        kategori_name = request.POST.get('kategori')
        artikel.ringkasan = request.POST.get('ringkasan')
        artikel.konten = request.POST.get('konten')
        
        gambar_url = request.POST.get('gambar_url')
        if not gambar_url:
            gambar_url = "https://images.unsplash.com/photo-1610427771746-860882e36785?q=80&w=800&auto=format&fit=crop"
        artikel.gambar_url = gambar_url
        
        kategori_obj = Kategori.objects.filter(nama=kategori_name).first()
        artikel.kategori = kategori_obj
        
        try:
            artikel.save()
            messages.success(request, f"Artikel '{artikel.judul}' berhasil diperbarui!")
            return redirect('artikel:artikel_detail', artikel_id=artikel.id)
        except Exception as e:
            messages.error(request, f"Gagal memperbarui artikel: {e}")
            
    return render(request, 'artikel_tulis.html', {
        'artikel': artikel,
        'categories': Kategori.objects.all()
    })

@login_required(login_url='accounts:login')
@user_passes_test(is_admin_or_editor, login_url='/')
def artikel_delete(request, artikel_id):
    artikel = get_object_or_404(Artikel, id=artikel_id)
    if request.method == 'POST':
        judul = artikel.judul
        artikel.delete()
        messages.success(request, f"Artikel '{judul}' telah berhasil dihapus.")
        return redirect('artikel:artikel_list')
        
    return render(request, 'artikel_delete.html', {'artikel': artikel})


# ----------------- KATEGORI CRUD (Admin Only) -----------------

@login_required(login_url='accounts:login')
@user_passes_test(is_admin, login_url='/')
def admin_kategori_list(request):
    kategoris = Kategori.objects.all().order_by('nama')
    return render(request, 'kategori_list.html', {'kategoris': kategoris})

@login_required(login_url='accounts:login')
@user_passes_test(is_admin, login_url='/')
def admin_kategori_create(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        if nama:
            try:
                Kategori.objects.create(nama=nama)
                messages.success(request, f"Kategori '{nama}' berhasil dibuat!")
                return redirect('artikel:admin_kategori_list')
            except Exception as e:
                messages.error(request, f"Gagal membuat kategori: {e}")
        else:
            messages.error(request, "Nama kategori tidak boleh kosong.")
            
    return render(request, 'kategori_form.html')

@login_required(login_url='accounts:login')
@user_passes_test(is_admin, login_url='/')
def admin_kategori_edit(request, slug):
    kategori = get_object_or_404(Kategori, slug=slug)
    if request.method == 'POST':
        nama = request.POST.get('nama')
        if nama:
            kategori.nama = nama
            # force slug update on save
            kategori.slug = ""
            try:
                kategori.save()
                messages.success(request, f"Kategori berhasil diperbarui menjadi '{nama}'!")
                return redirect('artikel:admin_kategori_list')
            except Exception as e:
                messages.error(request, f"Gagal memperbarui kategori: {e}")
        else:
            messages.error(request, "Nama kategori tidak boleh kosong.")
            
    return render(request, 'kategori_form.html', {'kategori': kategori})

@login_required(login_url='accounts:login')
@user_passes_test(is_admin, login_url='/')
def admin_kategori_delete(request, slug):
    kategori = get_object_or_404(Kategori, slug=slug)
    if request.method == 'POST':
        nama = kategori.nama
        try:
            kategori.delete()
            messages.success(request, f"Kategori '{nama}' berhasil dihapus.")
            return redirect('artikel:admin_kategori_list')
        except Exception as e:
            messages.error(request, f"Gagal menghapus kategori: {e}")
            
    return render(request, 'kategori_delete.html', {'kategori': kategori})


# ----------------- USER MANAGEMENT (Admin Only) -----------------

@login_required(login_url='accounts:login')
@user_passes_test(is_admin, login_url='/')
def admin_user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'user_list.html', {'users': users})

@login_required(login_url='accounts:login')
@user_passes_test(is_admin, login_url='/')
def admin_user_edit(request, user_id):
    edit_user = get_object_or_404(User, id=user_id)
    
    # Get user's current group/role
    current_group = edit_user.groups.first()
    current_role = current_group.name if current_group else None

    if request.method == 'POST':
        role_name = request.POST.get('role')
        is_staff = request.POST.get('is_staff') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on'

        # Update staff and superuser status
        edit_user.is_staff = is_staff
        edit_user.is_superuser = is_superuser
        edit_user.save()

        # Update Django group role
        edit_user.groups.clear()
        if role_name in ['Admin', 'Editor', 'User']:
            group_obj = Group.objects.get(name=role_name)
            edit_user.groups.add(group_obj)
            
        messages.success(request, f"Status dan Role pengguna '{edit_user.username}' berhasil diperbarui!")
        return redirect('artikel:admin_user_list')

    return render(request, 'user_edit.html', {
        'edit_user': edit_user,
        'current_role': current_role,
        'available_roles': ['Admin', 'Editor', 'User']
    })

@login_required(login_url='accounts:login')
@user_passes_test(is_admin, login_url='/')
def admin_user_delete(request, user_id):
    edit_user = get_object_or_404(User, id=user_id)
    if edit_user == request.user:
        messages.error(request, "Anda tidak dapat menghapus akun Anda sendiri!")
        return redirect('artikel:admin_user_list')
        
    if request.method == 'POST':
        username = edit_user.username
        edit_user.delete()
        messages.success(request, f"Pengguna '{username}' berhasil dihapus.")
        return redirect('artikel:admin_user_list')
        
    return render(request, 'artikel_delete.html', {
        'user_to_delete': edit_user
    })
