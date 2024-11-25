from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from .models import ArchivoEntrada, DocumentoGenerado, Plantilla
from .forms import ArchivoEntradaForm
from transformers import BartForConditionalGeneration, BartTokenizer
import os
import subprocess
import re

def sanitize_filename(filename):
    """
    Limpia el nombre del archivo, eliminando caracteres especiales.
    """
    return re.sub(r'[^\w\s-]', '', filename).replace(' ', '_')

# Inicializar el modelo y el tokenizador de BART
model_name = "facebook/bart-large-cnn"
bart_tokenizer = BartTokenizer.from_pretrained(model_name)
bart_model = BartForConditionalGeneration.from_pretrained(model_name)

def summarize_paragraphs(text, tokenizer, model, max_length=512, min_length=50):
    """
    Divide el texto en párrafos, genera resúmenes por párrafo y los combina.
    """
    paragraphs = text.split('\n')  # Dividir en párrafos
    summaries = []

    for paragraph in paragraphs:
        if paragraph.strip():  # Ignorar párrafos vacíos
            # Tokenizar y truncar el párrafo
            inputs = tokenizer(paragraph, return_tensors="pt", truncation=True, max_length=1024)
            outputs = model.generate(
                inputs.input_ids, 
                max_length=max_length, 
                min_length=min_length, 
                no_repeat_ngram_size=2, 
                length_penalty=2.0, 
                num_beams=4
            )
            summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
            summaries.append(summary)

    return "\n".join(summaries)

def process_text(request):
    """
    Procesa el texto ingresado por el usuario, genera un archivo PDF y muestra el resultado.
    """
    if request.method == 'GET':
        return render(request, 'plantillas/entrada_texto.html')

    elif request.method == 'POST':
        # Capturar datos del formulario
        titulo = request.POST.get('titulo', 'Título desconocido')
        fecha = request.POST.get('fecha', 'Fecha desconocida')  # Usar la fecha proporcionada por el usuario
        link = request.POST.get('link', '#')
        contenido = request.POST.get('contenido', '')

        try:
            resumen = summarize_paragraphs(contenido, bart_tokenizer, bart_model)
        except Exception:
            resumen = "No se pudo generar el resumen debido a un error interno."

        latex_dir = os.path.join(settings.MEDIA_ROOT, 'latex_files')
        pdf_dir = os.path.join(settings.MEDIA_ROOT, 'pdf_files')
        os.makedirs(latex_dir, exist_ok=True)
        os.makedirs(pdf_dir, exist_ok=True)




        # Generar contenido LaTeX
        latex_content = generate_latex_document(
            titulo,  
            resumen,  
            link,
            fecha
        )

        # Rutas para guardar archivos
        

        tex_filename = f"{sanitize_filename(titulo)}.tex"
        tex_file_path = os.path.join(latex_dir, tex_filename)
        pdf_filename = f"{sanitize_filename(titulo)}.pdf"
        pdf_file_path = os.path.join(pdf_dir, pdf_filename)

        # Guardar archivo LaTeX
        with open(tex_file_path, 'w') as tex_file:
            tex_file.write(latex_content)

        # Generar PDF
        try:
            subprocess.run(
                ['pdflatex', '-interaction=batchmode', '-output-directory', pdf_dir, tex_file_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError:
            return HttpResponse("Error al generar el PDF.", status=500)

        # Contexto para la plantilla
        context = {
            'titulo': titulo,
            'fecha_publicacion': fecha,
            'contenido': resumen,
            'link': link,
            'latex_file': os.path.join(settings.MEDIA_URL, 'latex_files', tex_filename),
            'pdf_file': os.path.join(settings.MEDIA_URL, 'pdf_files', pdf_filename)
        }

        return render(request, 'plantillas/resultados.html', context)

    return HttpResponse("Método no permitido", status=405)


def lista_plantillas(request):
    plantillas = Plantilla.objects.all()
    return render(request, 'plantillas/lista_plantillas.html', {'plantillas': plantillas})

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

def seleccionar_plantilla(request, archivo_id):
    return render(request, 'plantillas/seleccionar_plantilla.html')

def ver_documento(request, archivo_id):
    documento = get_object_or_404(DocumentoGenerado, archivo_entrada_id=archivo_id)
    return render(request, 'plantillas/ver_documento.html', {'documento': documento})

def generate_latex_document(title, content, link_url, date):
    """
    Genera un documento LaTeX con título, contenido, imagen, enlace y fecha.
    """
    escaped_title = escape_latex(title)
    escaped_content = escape_latex(content)
    escaped_date = escape_latex(date)  # Escapar la fecha

    link_latex = generate_latex_link(link_url)

    latex_document = f"""
    \\documentclass{{article}}
    \\usepackage[utf8]{{inputenc}}
    \\usepackage{{graphicx}}
    \\usepackage{{geometry}}
    \\usepackage{{hyperref}}

    \\geometry{{top=1in, bottom=1in, left=1in, right=1in}}

    \\title{{{escaped_title}}}
    \\author{{}}
    \\date{{{escaped_date}}}  % Fecha agregada aquí

    \\begin{{document}}

    \\maketitle

    \\begin{{flushleft}}
    {escaped_content}
    \\end{{flushleft}}

    \\vspace{{10mm}}

    \\noindent
    \\textbf{{Enlace a la noticia:}} \\\\
    {link_latex}

    \\end{{document}}
    """
    return latex_document


def escape_latex(text):
    """
    Escapa caracteres especiales de LaTeX.
    """
    special_chars = {
        '\\': r'\textbackslash{}',
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
    }
    for char, replacement in special_chars.items():
        text = text.replace(char, replacement)
    return text



def generate_latex_link(url, text=None):
    """
    Genera el código LaTeX para un enlace.
    """
    escaped_url = url
    display_text = escape_latex(text) if text else escaped_url
    return f"\\href{{{escaped_url}}}{{{display_text}}}"
