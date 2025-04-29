import streamlit as st
import os
import fitz  # PyMuPDF
import re

# Ruta fija de los PDFs
CARPETA_PDFS = "documentos_pdfs"

# Función para buscar el IMEI
def buscar_imei_en_pdfs(imei_objetivo):
    imei_objetivo = imei_objetivo.strip()
    resultados = []

    for archivo in os.listdir(CARPETA_PDFS):
        if archivo.lower().endswith(".pdf"):
            ruta_pdf = os.path.join(CARPETA_PDFS, archivo)
            try:
                doc = fitz.open(ruta_pdf)
                texto = ""
                for pagina in doc:
                    texto += pagina.get_text()

                # Extraer bloques posibles y comparar
                palabras = texto.replace('/', ' ').replace(';', ' ').replace('|', ' ').replace(':', ' ').replace(',', ' ').split()
                i = 0
                while i < len(palabras):
                    palabra = re.sub(r'\D', '', palabras[i])
                    if len(palabra) == 15 and palabra == imei_objetivo:
                        return archivo
                    elif len(palabra) < 15 and i + 1 < len(palabras):
                        siguiente = re.sub(r'\D', '', palabras[i+1])
                        combinado = palabra + siguiente
                        if len(combinado) == 15 and combinado == imei_objetivo:
                            return archivo
                        i += 1
                    i += 1
            except:
                continue
    return None

# UI
st.set_page_config(page_title="Verificador IMEI - Mr. Móvil", page_icon="🔍", layout="centered")

st.title("Verificador de IMEI Importaciones - Mr. Móvil")
st.caption("Los archivos PDF deben estar en la carpeta `documentos_pdfs/`.")

imei_input = st.text_input("Ingrese el IMEI (15 dígitos)", max_chars=15)

if st.button("Verificar"):
    if not imei_input.isdigit() or len(imei_input) != 15:
        st.error("Por favor ingrese un IMEI válido de 15 dígitos.")
    else:
        resultado = buscar_imei_en_pdfs(imei_input)
        if resultado:
            st.success(f"IMEI encontrado en: **{resultado}**")
            st.markdown(f"[Abrir PDF]({CARPETA_PDFS}/{resultado})")
        else:
            st.warning("IMEI no encontrado en ningún archivo.")