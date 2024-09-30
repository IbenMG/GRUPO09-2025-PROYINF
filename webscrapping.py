import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

url = "https://opia.fia.cl/601/w3-propertyvalue-148969.html"


palabras_clave = [
    "recursos hídricos", 
    "cultivos sostenibles", 
    "cambio climático",
    "Agricultura sustentable", 
    "Innovación agrícola", 
    "Biodiversidad", 
    "Gestión de recursos naturales"
]

try:
    # Realizar la solicitud a la página web
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    print("Página accedida correctamente")

except requests.exceptions.RequestException as e:
    print(f"Error al acceder a la página: {e}")
    exit()

# Buscar todos los enlaces en la página
enlaces = soup.find_all('a')

# Filtrar los enlaces que contienen las palabras clave
documentos_encontrados = []
for enlace in enlaces:
    texto = enlace.get_text().lower()
    for palabra in palabras_clave:
        if palabra.lower() in texto:
            href = enlace.get('href', '')
            if href:
                href_completo = urljoin(url, href)
                documentos_encontrados.append((texto, href_completo, palabra))
                print(f"Documento encontrado para '{palabra}': {texto} - {href_completo}")

# Comprobar si se encontraron documentos
if not documentos_encontrados:
    print("No se encontraron documentos con las palabras clave")
    exit()

# Crear un directorio para guardar los documentos
directorio = "documentos"
if not os.path.exists(directorio):
    os.makedirs(directorio)

# Función para obtener el enlace del PDF desde la página de destino
def obtener_enlace_pdf(pagina_destino):
    try:
        response = requests.get(pagina_destino)
        response.raise_for_status()
        soup_destino = BeautifulSoup(response.text, 'html.parser')

        pdf_enlace = soup_destino.find('a', href=lambda href: href and href.endswith('.pdf'))
        if pdf_enlace:
            return urljoin(pagina_destino, pdf_enlace['href'])  
        else:
            print("No se encontró un enlace PDF en la página de destino.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a la página de destino: {e}")
        return None

# Descargar los documentos
for i, (nombre, enlace, palabra_clave) in enumerate(documentos_encontrados):
    pdf_url = obtener_enlace_pdf(enlace)  # Obtener el enlace real del PDF
    if pdf_url:
        try:
            print(f"Descargando el documento desde: {pdf_url}")
            doc_response = requests.get(pdf_url)
            doc_response.raise_for_status()

            nombre_archivo = f"documento_{i+1}.pdf"
            ruta_completa = os.path.join(directorio, nombre_archivo)

            with open(ruta_completa, 'wb') as f:
                f.write(doc_response.content)

            print(f"Descargado: {nombre_archivo} para la palabra clave '{palabra_clave}'")
        except requests.exceptions.RequestException as e:
            print(f"Error al descargar {pdf_url}: {e}")
    else:
        print(f"No se pudo obtener el enlace PDF para '{nombre}'")

