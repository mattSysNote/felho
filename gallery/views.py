from django.shortcuts import render, redirect, get_object_or_404
from .models import Photo
from .forms import PhotoUploadForm, RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# 1. Fényképek listázása és rendezése
def photo_list(request):
    sort_by = request.GET.get('sort', 'name') # Alapértelmezett: név szerint
    
    if sort_by == 'date':
        photos = Photo.objects.order_by('-uploaded_at') # Dátum (legfrissebb elől)
    else:
        photos = Photo.objects.order_by('title') # Név szerint növekvő

    return render(request, 'gallery/photo_list.html', {'photos': photos})

# 2. Részletes nézet (kép megtekintése)
def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'gallery/photo_detail.html', {'photo': photo})

# 3. Feltöltés (Csak belépve)
@login_required
def photo_upload(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploader = request.user # Hozzákötjük a felhasználóhoz
            photo.save()
            return redirect('photo_list')
    else:
        form = PhotoUploadForm()
    return render(request, 'gallery/photo_upload.html', {'form': form})

# 4. Törlés (Csak belépve)
@login_required
def photo_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    # Opcionális biztonsági extra: csak a saját képet törölheti
    if request.method == 'POST':
        photo.delete()
        return redirect('photo_list')
    return render(request, 'gallery/photo_confirm_delete.html', {'photo': photo})

# 5. Regisztráció
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Automatikus beléptetés regisztráció után
            return redirect('photo_list')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})