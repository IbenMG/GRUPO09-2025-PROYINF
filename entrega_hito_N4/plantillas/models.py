from django.db import models

class Plantilla(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    archivo_referencia = models.FileField(upload_to='plantillas_referencia/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class ArchivoEntrada(models.Model):
    usuario = models.CharField(max_length=255, blank=True, null=True)  # Opcional, si quieres registrar quién sube el archivo
    archivo = models.FileField(upload_to='archivos_entrada/', blank=True, null=True)
    texto_procesado = models.TextField(blank=True, null=True)  # Texto extraído del archivo
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Archivo subido el {self.fecha_subida}"

class DocumentoGenerado(models.Model):
    archivo_entrada = models.ForeignKey(ArchivoEntrada, on_delete=models.CASCADE)
    plantilla_usada = models.ForeignKey(Plantilla, on_delete=models.SET_NULL, null=True)
    archivo_resultado = models.FileField(upload_to='documentos_generados/')
    formato = models.CharField(max_length=50, choices=[('PDF', 'PDF'), ('LATEX', 'LaTeX')], default='PDF')
    fecha_generacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Documento generado el {self.fecha_generacion}"
