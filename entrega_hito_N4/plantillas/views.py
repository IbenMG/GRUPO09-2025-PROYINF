from django.shortcuts import render, redirect, get_object_or_404
from .models import ArchivoEntrada, DocumentoGenerado, Plantilla
from .forms import ArchivoEntradaForm, PlantillaForm
from transformers import GPT2Tokenizer, TFGPT2Model, TFGPT2LMHeadModel,GPT2LMHeadModel,TFAutoModelForCausalLM,AutoTokenizer
import os
import tensorflow as tf
from django.conf import settings

# Configurar explícitamente el uso de CPU
tf.config.set_visible_devices([], 'GPU')

# Cargar modelo y tokenizer de GPT-2
model = TFAutoModelForCausalLM.from_pretrained('gpt2')
tokenizer = AutoTokenizer.from_pretrained('gpt2')

def process_text(request):
    if request.method == 'POST':
        input_text = request.POST.get('input_text').strip()

        if not input_text:
            return render(request, 'plantillas/entrada_texto.html', {
                'error_message': 'Por favor, introduce texto válido.',
            })
        
        encoded_input = tokenizer(input_text, return_tensors='tf')
        output = model.generate(
            encoded_input['input_ids'],
            max_new_tokens=100,
            temperature=0.7,
            top_k=50,
            top_p=0.9,
            repetition_penalty=1.2
        )
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        
        return render(request, 'plantillas/resultados.html', {
            'input_text': input_text,
            'output_text': generated_text,
        })
    return render(request, 'plantillas/entrada_texto.html')


def index_plantillas(request):
    return render(request, 'plantillas/index.html')

# Vista para listar las plantillas
def lista_plantillas(request):
    plantillas = Plantilla.objects.all()
    return render(request, 'plantillas/lista_plantillas.html', {'plantillas': plantillas})

# Vista para cargar un archivo y seleccionar plantilla
def cargar_archivo(request):
    if request.method == 'POST':
        form = ArchivoEntradaForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.save()
            # Extraer texto del archivo o procesar según sea necesario
            texto_procesado = "Texto procesado (simulado)"  # Aquí extraerías texto del archivo
            archivo.texto_procesado = texto_procesado
            archivo.save()
            return redirect('seleccionar_plantilla', archivo_id=archivo.id)
    else:
        form = ArchivoEntradaForm()
    return render(request, 'plantillas/cargar_archivo.html', {'form': form})

# Vista para seleccionar plantilla y generar documento
def seleccionar_plantilla(request, archivo_id):
    archivo = get_object_or_404(ArchivoEntrada, id=archivo_id)
    plantillas = Plantilla.objects.all()
    if request.method == 'POST':
        plantilla_id = request.POST.get('plantilla')
        formato = request.POST.get('formato', 'PDF')
        plantilla = get_object_or_404(Plantilla, id=plantilla_id)

        # Generar documento con GPT-2
        texto_generado = model.generate(
            tokenizer.encode(archivo.texto_procesado, return_tensors='tf'),
            max_length=200
        )
        
        # Decodificar el texto generado
        texto_generado = tokenizer.decode(texto_generado[0], skip_special_tokens=True)
        
        # Simulación: Guardar texto generado como PDF o LaTeX (a implementar según formato)
        archivo_resultado_path = os.path.join(settings.MEDIA_ROOT, 'documentos_generados', f'documento_{archivo.id}.pdf')
        with open(archivo_resultado_path, 'w') as archivo_resultado:
            archivo_resultado.write(texto_generado)

        # Guardar registro en base de datos
        DocumentoGenerado.objects.create(
            archivo_entrada=archivo,
            plantilla_usada=plantilla,
            archivo_resultado=os.path.relpath(archivo_resultado_path, settings.MEDIA_ROOT),
            formato=formato
        )

        return redirect('ver_documento', archivo_id=archivo.id)

    return render(request, 'plantillas/seleccionar_plantilla.html', {'archivo': archivo, 'plantillas': plantillas})

# Vista para ver un documento generado
def ver_documento(request, archivo_id):
    documento = get_object_or_404(DocumentoGenerado, archivo_entrada_id=archivo_id)
    return render(request, 'plantillas/ver_documento.html', {'documento': documento})
