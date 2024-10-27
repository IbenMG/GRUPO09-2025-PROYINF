# En buscador_fuentes/services/gestor_fuentes.py

import json

JSON_FILE = 'etiquetas_fuentes.json'

class GestorFuentes:
    @staticmethod
    def cargar_etiquetas():
        try:
            with open(JSON_FILE, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    @staticmethod
    def guardar_etiquetas(fuentes_por_etiqueta):
        with open(JSON_FILE, 'w') as file:
            json.dump(fuentes_por_etiqueta, file, indent=4)

    @staticmethod
    def agregar_fuente(nombre, link, etiquetas):
        fuentes_por_etiqueta = GestorFuentes.cargar_etiquetas()
        for etiqueta in etiquetas:
            if etiqueta not in fuentes_por_etiqueta:
                fuentes_por_etiqueta[etiqueta] = []
            fuente = {"nombre": nombre, "link": link}
            fuentes_por_etiqueta[etiqueta].append(fuente)
        GestorFuentes.guardar_etiquetas(fuentes_por_etiqueta)

    @staticmethod
    def buscar_fuentes_por_etiqueta(etiqueta):
        fuentes_por_etiqueta = GestorFuentes.cargar_etiquetas()
        return fuentes_por_etiqueta.get(etiqueta, [])

    @staticmethod
    def modificar_fuente(nombre, nuevo_nombre=None, nuevo_link=None, nuevas_etiquetas=None):
        fuentes_por_etiqueta = GestorFuentes.cargar_etiquetas()
        fuente_encontrada = False

        for etiqueta, fuentes in fuentes_por_etiqueta.items():
            for fuente in fuentes:
                if fuente["nombre"] == nombre:
                    fuente_encontrada = True
                    if nuevo_nombre:
                        fuente["nombre"] = nuevo_nombre
                    if nuevo_link:
                        fuente["link"] = nuevo_link

        if nuevas_etiquetas:
            GestorFuentes.eliminar_fuente(nombre)
            GestorFuentes.agregar_fuente(nuevo_nombre or nombre, nuevo_link or fuente["link"], nuevas_etiquetas)

        if fuente_encontrada:
            GestorFuentes.guardar_etiquetas(fuentes_por_etiqueta)

    @staticmethod
    def eliminar_fuente(nombre):
        fuentes_por_etiqueta = GestorFuentes.cargar_etiquetas()
        for etiqueta, fuentes in fuentes_por_etiqueta.items():
            fuentes_por_etiqueta[etiqueta] = [fuente for fuente in fuentes if fuente["nombre"] != nombre]
        GestorFuentes.guardar_etiquetas(fuentes_por_etiqueta)

    @staticmethod
    def mostrar_fuentes():
        fuentes_por_etiqueta = GestorFuentes.cargar_etiquetas()
        return fuentes_por_etiqueta