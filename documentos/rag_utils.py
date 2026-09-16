from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

# Cargamos el modelo una sola vez, a nivel de modulo (no dentro de cada funcion)
# para no recargarlo en cada llamada - es una operacion costosa

_model = None

def obtener_modelo():
    global _model
    if _model is None:
        _model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    return _model

def extraer_texto_pdf(ruta_archivo):
    "Estrae tdo el texto de un pdf, pagina por pagina"
    lector = PdfReader(ruta_archivo)
    texto_completo = ""
    for pagina in lector.pages:
        texto_completo += pagina.extract_text() + "\n\n"
    return texto_completo

def trocear_texto(texto, tamano_chunk = 500, superposicion=50):
    """
    Trocear el texto en fragmentos de tamano_chunk caracteres,
    con superposicion caracteres compartidos entre chunks consecutivos."""

    chunks = []
    inicio = 0
    while inicio < len(texto):
        fin = inicio + tamano_chunk
        chunk = texto[inicio:fin].strip()
        if chunk:
            chunks.append(chunk)
        inicio += tamano_chunk - superposicion

    return chunks

def procesar_documento(documento):
    """
    Recibe un objeto Documento de Django, extrae su texto,
    lo trocea, genera embeddings, y crea los Fragmento asociados.
    """
    from .models import Fragmento 

    texto = extraer_texto_pdf(documento.archivo.path)
    chunks = trocear_texto(texto)

    model = obtener_modelo()
    embeddings = model.encode(chunks)

    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        Fragmento.objects.create(
            documento=documento,
            contenido =chunk,
            embedding=emb,
            order=i
        )

    documento.procesado = True
    documento.save()

    return len(chunks)