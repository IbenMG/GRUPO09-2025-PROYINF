from django import forms
from .models import ArchivoEntrada, Plantilla

class ArchivoEntradaForm(forms.ModelForm):
    class Meta:
        model = ArchivoEntrada
        fields = ['archivo']

class PlantillaForm(forms.ModelForm):
    class Meta:
        model = Plantilla
        fields = ['nombre', 'descripcion', 'archivo_referencia']
