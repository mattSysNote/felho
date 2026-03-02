from django.db import models
from django.contrib.auth.models import User


class FileBlob(models.Model):
    bytes = models.TextField()
    filename = models.CharField(max_length=255) 
    mimetype = models.CharField(max_length=50)

    def __str__(self):
        return self.filename

class Photo(models.Model):
    # CHANGED: You MUST use this string string. Do not use a function here.
    image = models.ImageField(upload_to='gallery.FileBlob/bytes/filename/mimetype')
    
    title = models.CharField(max_length=40, verbose_name="Kép címe")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title