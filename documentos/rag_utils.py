from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from anthropic import Anthropic
import os
from pgvector.django import CosineDistance
# Cargamos el modelo una sola vez, a nivel de modulo (no dentro de cada funcion)
# para no recargarlo en cada llamada - es una operacion costosa

_model = None
_client = None

def obtener_cliente():
    global _client
    if _client is None:
        _client = Anthropic(api_key= os.getenv("ANTHROPIC_API_KEY"))
    return _client

def obtener_modelo(): # MODELO 
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

def buscar_fragmentos_relevantes(documento, pregunta, k=3):
    #     Devuelve los k fragmentos mas relevantes semanticamente a la pregunta"""
    from .models import Fragmento
    # 1 obtenemos modelo de AI
    model = obtener_modelo()
    vector_pregunta = model.encode(pregunta)

    # 2 Realizar QUERY al model (tabla) que contiene los fragmentos
    resultados=(
        Fragmento.objects
        .filter(documento=documento)
        #.order_by(embedding.cosine_distance(vector_pregunta) for embedding in [Fragmento._meta.get_field('embedding')]) # esto era en sqlachemy
        .annotate(distancia=CosineDistance('embedding', vector_pregunta))
        .order_by('distancia')[:k]
    )
    
    # 3 Retornamos resultados
    #return list(resultados[:k])
    return list(resultados)

def generar_respuesta_chat(pregunta, fragmentos):
    # 4. Obtenemos los fragmentos 
    contexto = "\n\n".join(f.contenido for f in fragmentos)
    #5. anexamos todo a un prompt tanto que va a responder la ia, el contexto, y la pregunta que le hagamos
    prompt = f"""Respondé la pregunta usando ÚNICAMENTE la información del contexto.
    Si el contexto no tiene la respuesta, decí que no tenés esa información.
    
    Contexto:
    {contexto}
    
    Pregunta: {pregunta}"""

    # 6. Obtenemos el modelo  de ia osea la llave que creamos 
    client = obtener_cliente()
   
    # 7. creamos un tipo query de la respuesta que nos va a dar el modelo cliente
    respuesta = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    return respuesta.content[0].text

    