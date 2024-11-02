from django.db import models

class DocumentoPDF(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    archivo = models.FileField(upload_to='pdfs/')

    def __str__(self):
      return self.nombre
