# Inteligencia de Documentos

Aplicación web que permite subir documentos PDF, procesarlos automáticamente
mediante *chunking* y *embeddings*, y consultarlos en lenguaje natural
usando un pipeline de RAG (*Retrieval-Augmented Generation*) con Claude.

## ¿Qué hace?

1. Un usuario sube un documento PDF desde el navegador
2. El sistema extrae el texto, lo trocea en fragmentos, y genera un
   embedding vectorial de cada uno (con `sentence-transformers`)
3. Los fragmentos y sus vectores se guardan en PostgreSQL usando
   la extensión `pgvector`
4. El usuario puede hacer preguntas sobre el documento: el sistema
   recupera los fragmentos más relevantes por similitud semántica
   y usa la API de Claude para generar una respuesta basada en ellos

## Stack técnico

- **Backend:** Django 5
- **Base de datos:** PostgreSQL + pgvector
- **Embeddings:** sentence-transformers (`paraphrase-multilingual-MiniLM-L12-v2`)
- **Generación de respuestas:** API de Claude (Anthropic), modelo Haiku
- **Extracción de PDF:** pypdf

## Arquitectura

El proyecto separa dos flujos principales:

- **Ingesta:** subida de PDF → chunking → embeddings → almacenamiento
- **Consulta:** pregunta del usuario → retrieval semántico → generación
  de respuesta con contexto

## Instalación local

\`\`\`bash (GitBash)
git clone https://github.com/CiberNefty/inteligencia-documentos.git
cd inteligencia-documentos
python -m venv venv
source venv/Scripts/activate  # Windows (Git Bash)
pip install -r requirements.txt
\`\`\`

Crear un archivo `.env` en la raíz con:

\`\`\`
DB_NAME=inteligencia_docs_db
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5433 # Ó el puerto que desees segun tu gestor DB
ANTHROPIC_API_KEY=sk-ant-tu-key (tendrias que cargar creditos en Claud Platform y crear una llave)
\`\`\`

Requiere PostgreSQL con la extensión `vector` instalada (recomendado:
imagen Docker `pgvector/pgvector`).

\`\`\`bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
\`\`\`

## Estado del proyecto

🚧 En desarrollo activo — proyecto de aprendizaje y portafolio.

- [x] Modelado de datos (Documento, Fragmento, Conversación, Mensaje)
- [x] Panel de administración
- [x] Subida y procesamiento automático de PDFs (chunking + embeddings)
- [ ] Chat con retrieval semántico + generación con Claude
- [ ] Interfaz visual pulida
- [ ] Despliegue

## Autor

D — [github.com/CiberNefty](https://github.com/CiberNefty)