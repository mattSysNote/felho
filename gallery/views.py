from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PhotoUploadForm, RegistrationForm
from django.core.files.base import ContentFile
from django.http import HttpResponseForbidden
from django.contrib.auth import login
from .models import Photo
from PIL import Image
import io

# list images
def photo_list(request):
    sort_by = request.GET.get('sort', 'name')
    
    if sort_by == 'date':
        photos = Photo.objects.order_by('-uploaded_at')
    else:
        photos = Photo.objects.order_by('title') 

    return render(request, 'gallery/photo_list.html', {'photos': photos})

# detail view
def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'gallery/photo_detail.html', {'photo': photo})

# upload
@login_required
def photo_upload(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            uploaded_image = form.cleaned_data['image']
            img = Image.open(uploaded_image)
            data = list(img.getdata())
            image_without_exif = Image.new(img.mode, img.size)
            image_without_exif.putdata(data)

            buffer = io.BytesIO()

            image_without_exif.save(buffer, format=img.format) 
            photo.image.save(uploaded_image.name, ContentFile(buffer.getvalue()), save=False)

            photo.uploaded_by = request.user
            photo.save()
            return redirect('photo_list')
    else:
        form = PhotoUploadForm()
    return render(request, 'gallery/photo_upload.html', {'form': form})

# delete
@login_required
def photo_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    
    # security only the owner or the admin can delet image
    if request.user != photo.uploaded_by and not request.user.is_superuser:
        return HttpResponseForbidden("Nincs jogosultsága törölni ezt a képet.")
    
    if request.method == 'POST':
        photo.delete()
        return redirect('photo_list')
        
    return render(request, 'gallery/photo_confirm_delete.html', {'photo': photo})

# register
def register(request):
    if request.user.is_authenticated:
        return redirect('photo_list')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('photo_list')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})