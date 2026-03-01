from django.shortcuts import render, redirect, get_object_or_404
from .models import Photo
from .forms import PhotoUploadForm, RegistrationForm # Feltételezve, hogy léteznek
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponseForbidden

# 1. Fényképek listázása
def photo_list(request):
    sort_by = request.GET.get('sort', 'name')
    
    if sort_by == 'date':
        photos = Photo.objects.order_by('-uploaded_at')
    else:
        # Figyelj: a modellben 'title'-t írtam, ha nálad 'name', akkor javítsd át!
        photos = Photo.objects.order_by('title') 

    return render(request, 'gallery/photo_list.html', {'photos': photos})

# 2. Részletes nézet
def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'gallery/photo_detail.html', {'photo': photo})

# 3. Feltöltés (Javítva és biztonságosabb)
@login_required
def photo_upload(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            # JAVÍTVA: egységesen 'uploaded_by' használata
            photo.uploaded_by = request.user 
            photo.save()
            return redirect('photo_list')
    else:
        form = PhotoUploadForm()
    return render(request, 'gallery/photo_upload.html', {'form': form})

# 4. Törlés (Biztonsági ellenőrzéssel)
@login_required
def photo_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    
    # BIZTONSÁG: Csak a tulajdonos vagy admin törölhet
    if request.user != photo.uploaded_by and not request.user.is_superuser:
        return HttpResponseForbidden("Nincs jogosultsága törölni ezt a képet.")
    
    if request.method == 'POST':
        photo.delete()
        return redirect('photo_list')
        
    return render(request, 'gallery/photo_confirm_delete.html', {'photo': photo})

# 5. Regisztráció
def register(request):
    if request.user.is_authenticated:
        return redirect('photo_list') # Ha már be van lépve, ne regisztráljon újra

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('photo_list')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})