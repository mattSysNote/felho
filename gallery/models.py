import os
import uuid
from django.db import models
from django.contrib.auth.models import User


# uuid for security
def unique_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('photos', filename)

class Photo(models.Model):
    # Itt használjuk a fenti függvényt az 'upload_to' paraméternél
    image = models.ImageField(upload_to=unique_file_path)
    
    # Eredeti név megtartása (opcionális, de hasznos a megjelenítéshez)
    title = models.CharField(max_length=100, verbose_name="Kép címe")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title