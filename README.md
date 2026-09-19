# 🧠 Inteligencia de Documentos

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.1-092E20?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-4169E1?logo=postgresql&logoColor=white)
![Claude](https://img.shields.io/badge/Claude_API-Haiku_4.5-D97757)
![Status](https://img.shields.io/badge/status-en%20desarrollo-yellow)

Aplicación web que permite subir documentos PDF, procesarlos automáticamente
mediante *chunking* y *embeddings*, y consultarlos en lenguaje natural
usando un pipeline de RAG (*Retrieval-Augmented Generation*) con Claude.

---

## 📋 Tabla de contenidos

- [¿Qué hace?](#-qué-hace)
- [Stack técnico](#-stack-técnico)
- [Arquitectura](#-arquitectura)
- [Instalación local](#-instalación-local)
- [Estado del proyecto](#-estado-del-proyecto)

---

## 🚀 ¿Qué hace?

1. Un usuario sube un documento PDF desde el navegador
2. El sistema extrae el texto, lo trocea en fragmentos, y genera un
   embedding vectorial de cada uno (con `sentence-transformers`)
3. Los fragmentos y sus vectores se guardan en PostgreSQL usando
   la extensión `pgvector`
4. El usuario puede hacer preguntas sobre el documento: el sistema
   recupera los fragmentos más relevantes por similitud semántica
   y usa la API de Claude para generar una respuesta basada en ellos

<!-- Cuando tengas un GIF de demo, va acá:
![demo](ruta/al/gif.gif)
-->

## 🛠️ Stack técnico

| Capa | Tecnología |
|---|---|
| Backend | Django 6 |
| Base de datos | PostgreSQL + pgvector |
| Embeddings | sentence-transformers (`paraphrase-multilingual-MiniLM-L12-v2`) |
| Generación | API de Claude (Anthropic), modelo Haiku |
| Extracción PDF | pypdf |

## 🏗️ Arquitectura

El proyecto separa dos flujos principales:

- **Ingesta:** subida de PDF → chunking → embeddings → almacenamiento
- **Consulta:** pregunta del usuario → retrieval semántico → generación
  de respuesta con contexto

<details>
<summary>📐 Ver esquema de base de datos</summary>

- `Documento` — PDF subido, con su área/departamento y estado de procesamiento
- `Fragmento` — cada chunk de texto con su embedding, ligado a un `Documento`
- `Conversacion` — historial de chat, ligado a un `Documento` y un usuario
- `Mensaje` — cada pregunta/respuesta dentro de una `Conversacion`

</details>

## ⚙️ Instalación local

### 1. Base de datos (PostgreSQL + pgvector, vía Docker)

Necesitás [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y corriendo.

Creá un archivo `docker-compose.yml` en la raíz del proyecto:

\`\`\`yaml
services:
  postgres:
    image: pgvector/pgvector:pg16
    container_name: inteligencia_docs_postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: tu_usuario
      POSTGRES_PASSWORD: tu_password
      POSTGRES_DB: inteligencia_docs_db
    ports:
      - "5433:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
\`\`\`

Levantá el contenedor:

\`\`\`bash
docker compose up -d
\`\`\`

Activá la extensión `vector` dentro de la base (con `psql`, pgAdmin, o el cliente que prefieras):

\`\`\`sql
CREATE EXTENSION IF NOT EXISTS vector;
\`\`\`

### 2. Backend (Django)

\`\`\`bash
git clone https://github.com/CiberNefty/inteligencia-documentos.git
cd inteligencia-documentos
python -m venv venv
source venv/Scripts/activate  # Windows (Git Bash)
pip install -r requirements.txt
\`\`\`

Creá un archivo `.env` en la raíz con:

\`\`\`
DB_NAME=inteligencia_docs_db
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5433
ANTHROPIC_API_KEY=sk-ant-tu-key
\`\`\`

\`\`\`bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
\`\`\`

La app queda disponible en `http://127.0.0.1:8000/`.

## ✅ Estado del proyecto

**Funcionalidades core:**
- [x] Modelado de datos (Documento, Fragmento, Conversación, Mensaje)
- [x] Panel de administración
- [x] Subida y procesamiento automático de PDFs (chunking + embeddings)
- [x] Chat con retrieval semántico + generación con Claude
- [x] Manejo de errores (ingesta y chat)
- [x] Diseño visual
- [ ] Eliminar documentos

**Ideas para próximas iteraciones:**
- [ ] Elegir el método de distancia vectorial desde la interfaz (coseno / euclidiana / producto interno)
- [ ] Chat que consulte varios documentos a la vez, no solo uno
- [ ] Paginación en la lista de documentos
- [ ] Pruebas automatizadas (pytest)
- [ ] Dockerizar la app completa (no solo la base de datos)
- [ ] Capturas de pantalla / demo en vivo
- [ ] Despliegue

## 👤 Autor

D — [github.com/CiberNefty](https://github.com/CiberNefty)