#!/bin/bash

# Ingresar a la shell de Django y ejecutar comandos para mostrar el contenido de la tabla "Fuente"
python3 manage.py shell << EOF
from buscador_fuentes.models import Fuente
fuentes = Fuente.objects.all()
for fuente in fuentes:
    print(f"Nombre: {fuente.nombre}, Link: {fuente.url}, Etiquetas: {fuente.etiquetas}")
EOF
