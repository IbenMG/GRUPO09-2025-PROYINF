from django.db import models

class DocumentoPDF(models.Model):
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='pdfs/')
    etiquetas = models.CharField(max_length=255, blank=True)
    publicado = models.BooleanField(default=False)  # Indica si estÃ¡ publicado/finalizado
    fecha_publicacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nombre
