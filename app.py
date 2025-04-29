import streamlit as st
import os
import fitz  # PyMuPDF
import re
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="Verificador IMEI - Mr. Móvil",
    page_icon="🔍",
    layout="centered"
)

# Mostrar logo
try:
    logo = Image.open("logo_mr_movil.png")
    st.image(logo, width=250)
except:
    st.caption("Logo no disponible.")

# Título y descripción
st.title("Verificador de IMEI Importaciones - Mr. Móvil")
st.caption("Los archivos PDF deben estar en la carpeta `documentos_pdfs/` del repositorio.")

# Carpeta fija de los PDFs
CARPETA_PDFS = "documentos_pdfs"

# Crear carpeta si no existe
if not os.path.exists(CARPETA_PDFS):
    os.makedirs(CARPETA_PDFS)

# Función para buscar el IMEI
def buscar_imei_en_pdfs(imei_objetivo):
    imei_objetivo = imei_objetivo.strip()
    for archivo in os.listdir(CARPETA_PDFS):
        if archivo.lower().endswith(".pdf"):
            ruta_pdf = os.path.join(CARPETA_PDFS, archivo)
            try:
                doc = fitz.open(ruta_pdf)
                texto = ""
                for pagina in doc:
                    texto += pagina.get_text()
                palabras = texto.replace('/', ' ').replace(';', ' ').replace('|', ' ').replace(':', ' ').replace(',', ' ').split()
                i = 0
                while i < len(palabras):
                    palabra = re.sub(r'\D', '', palabras[i])
                    if len(palabra) == 15 and palabra == imei_objetivo:
                        return archivo
                    elif len(palabra) < 15 and i + 1 < len(palabras):
                        siguiente = re.sub(r'\D', '', palabras[i + 1])
                        combinado = palabra + siguiente
                        if len(combinado) == 15 and combinado == imei_objetivo:
                            return archivo
                        i += 1
                    i += 1
            except:
                continue
    return None

# Campo para ingresar IMEI
imei_input = st.text_input("Ingrese el IMEI (15 dígitos)", max_chars=15)

# Botón de verificación
if st.button("Verificar"):
    if not imei_input.isdigit() or len(imei_input) != 15:
        st.error("Por favor ingrese un IMEI válido de 15 dígitos.")
    elif not os.listdir(CARPETA_PDFS):
        st.warning("No hay archivos PDF en la carpeta `documentos_pdfs/`.")
    else:
        resultado = buscar_imei_en_pdfs(imei_input)
        if resultado:
            st.success(f"IMEI encontrado en: **{resultado}**")
            ruta_pdf = os.path.join(CARPETA_PDFS, resultado)
            try:
                with open(ruta_pdf, "rb") as f:
                    st.download_button(
                        label="Descargar PDF",
                        data=f,
                        file_name=resultado,
                        mime="application/pdf"
                    )
            except:
                st.warning("El archivo fue encontrado, pero no puede descargarse desde esta app.")
        else:
            st.warning("IMEI no encontrado en ningún archivo.")