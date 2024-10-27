from django.shortcuts import render, redirect
import json
from .models import Fuente  # Importa el modelo Fuente que creaste
from buscador_fuentes.services.gestor_fuentes import GestorFuentes

def index(request):
    fuentes = Fuente.objects.all()  # Obtiene todas las fuentes
    return render(request, 'buscador_fuentes/index.html', {'fuentes': fuentes})

def agregar_fuentes(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        url = request.POST.get("url")
        etiquetas = request.POST.get("etiquetas").split(",")

        # Crea una nueva fuente
        nueva_fuente = Fuente(nombre=nombre, url=url, etiquetas=json.dumps(etiquetas))
        nueva_fuente.save()
        return redirect("index")
    return render(request, 'buscador_fuentes/agregar_fuentes.html')

# Búsqueda de fuentes para modificar
def buscar_para_modificar(request):
    query = request.GET.get("query")
    resultados = Fuente.objects.filter(nombre__icontains=query) | Fuente.objects.filter(etiquetas__contains=query)
    return render(request, "buscador_fuentes/modificar_fuentes.html", {"resultados": resultados})

# Búsqueda de fuentes para borrar
def buscar_para_borrar(request):
    query = request.GET.get("query")
    resultados = Fuente.objects.filter(nombre__icontains=query) | Fuente.objects.filter(etiquetas__contains=query)
    return render(request, "buscador_fuentes/borrar_fuentes.html", {"resultados": resultados})

# Modificar una fuente
def modificar_fuentes(request, fuente_id):
    fuente = Fuente.objects.get(id=fuente_id)
    if request.method == "POST":
        fuente.nombre = request.POST.get("nombre")
        fuente.link = request.POST.get("link")
        fuente.etiquetas = json.dumps(request.POST.get("etiquetas").split(","))
        fuente.save()
        return redirect("index")
    return render(request, "buscador_fuentes/modificar_detalle.html", {"fuente": fuente})

# Borrar una fuente
def borrar_fuentes(request, fuente_id):
    fuente = Fuente.objects.get(id=fuente_id)
    if request.method == "POST":
        fuente.delete()
        return redirect("index")
    return render(request, "buscador_fuentes/borrar_confirmar.html", {"fuente": fuente})
def vistas_fuentes(request):
    return render(request, 'buscador_fuentes/vistas_fuentes.html')
def buscar_fuentes(request):
    etiquetas = request.GET.get("etiquetas")
    resultados = Fuente.objects.filter(etiquetas__contains=etiquetas) if etiquetas else []
    return render(request, "buscador_fuentes/buscar_fuentes.html", {"resultados": resultados})

"""
def agregar_fuente(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        link = request.POST['link']
        etiquetas = request.POST['etiquetas'].split(',')
        GestorFuentes.agregar_fuente(nombre, link, etiquetas)
        return redirect('vista_fuentes')

    return render(request, 'buscador_fuentes/agregar_fuente.html')

def buscar_fuentes(request):
    etiqueta = request.GET.get('etiqueta', '')
    fuentes = GestorFuentes.buscar_fuentes_por_etiqueta(etiqueta)
    return render(request, 'buscador_fuentes/buscar_fuentes.html', {'fuentes': fuentes})

def modificar_fuente(request, nombre):
    if request.method == 'POST':
        nuevo_nombre = request.POST.get('nuevo_nombre')
        nuevo_link = request.POST.get('nuevo_link')
        nuevas_etiquetas = request.POST.get('nuevas_etiquetas').split(',')
        GestorFuentes.modificar_fuente(nombre, nuevo_nombre, nuevo_link, nuevas_etiquetas)
        return redirect('vista_fuentes')

    return render(request, 'buscador_fuentes/modificar_fuente.html', {'nombre': nombre})

def eliminar_fuente(request, nombre):
    GestorFuentes.eliminar_fuente(nombre)
    return redirect('vista_fuentes')

def vista_fuentes(request):
    fuentes = GestorFuentes.mostrar_fuentes()
    return render(request, 'buscador_fuentes/vista_fuentes.html', {'fuentes': fuentes})
"""