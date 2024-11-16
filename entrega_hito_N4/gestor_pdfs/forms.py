from django import forms
from .models import DocumentoPDF

class DocumentoPDFForm(forms.ModelForm):
    class Meta:
        model = DocumentoPDF
        fields = ['nombre', 'archivo', 'etiquetas']  # Incluyendo el campo 'etiquetas'

    def __init__(self, *args, **kwargs):
        super(DocumentoPDFForm, self).__init__(*args, **kwargs)
        # Añadir clases a los campos
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['archivo'].widget.attrs.update({'class': 'form-control'})
        self.fields['etiquetas'].widget.attrs.update({'class': 'form-control'})
