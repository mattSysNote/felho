from django.db import models
from django.contrib.auth.models import User

class Photo(models.Model):
    # Név: max 40 karakter
    title = models.CharField(max_length=40, verbose_name="Fénykép neve")
    # A képfájl tárolása
    image = models.ImageField(upload_to='photos/', verbose_name="Képfájl")
    # Feltöltés dátuma (automatikus)
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Feltöltve")
    # Opcionális funkció: összekötjük a feltöltővel
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, verbose_name="Feltöltő")

    def __str__(self):
        return self.title