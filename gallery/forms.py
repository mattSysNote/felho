from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Photo
from django import forms
from PIL import Image

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'image']

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if not image:
            raise ValidationError("Nincs feltöltött kép.")
        
        max_size_mb = 10
        if image.size > max_size_mb * 1024 * 1024:
            raise ValidationError(f"A kép túl nagy! A maximum méret: {max_size_mb}MB")
        
        try:
            img = Image.open(image)
            
            img.verify() 
            
            image.file.seek(0)
            img = Image.open(image)

            max_dimension = 4000
            if img.width > max_dimension or img.height > max_dimension:
                raise ValidationError("A kép felbontása túl nagy (max 4000x4000 pixel).")
            
            allowed_formats = ['JPEG', 'PNG', 'GIF', 'WEBP']
            if img.format not in allowed_formats:
                raise ValidationError(f"Nem támogatott képformátum: {img.format}. Csak JPG, PNG, GIF engedélyezett.")

        except (IOError, SyntaxError) as e:
            raise ValidationError("A feltöltött fájl nem érvényes kép, vagy sérült.")
            
        return image

class RegistrationForm(UserCreationForm):
    pass