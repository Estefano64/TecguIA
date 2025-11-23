# TecguIA - Guía Rápida

## 🚀 Inicio Rápido

### 1. Instalación

```bash
# Clonar el repositorio
git clone <repository-url>
cd TecguIA

# Ejecutar el script de configuración
./run.sh
```

### 2. Configuración de APIs

Edita el archivo `.env` con tus credenciales:

```bash
# APIs (YA CONFIGURADAS)
GEMINI_API_KEY=AIzaSyBd7ekrJNRhjyq_e6yImQHYuAQeWcpNA6Q
MISTRAL_API_KEY=0TMDdNoLFZ0q0sIPPhKQhfRJZjy7NJGK

# Azure Storage (CONFIGURAR SI QUIERES ALMACENAMIENTO EN LA NUBE)
AZURE_STORAGE_CONNECTION_STRING=tu_connection_string_aqui
AZURE_STORAGE_CONTAINER_NAME=educational-content
```

### 3. Uso Básico - CLI

```bash
# Procesar un video de YouTube
python cli.py \
  --video-url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --artifacts pdf,map,podcast \
  --title "Mi Clase de Programación"

# Procesar un video local
python cli.py \
  --video-path "/ruta/a/mi/video.mp4" \
  --artifacts pdf,map
```

### 4. Uso Básico - API

```bash
# Iniciar el servidor
python main.py

# El servidor estará en http://localhost:8000
# Documentación interactiva en http://localhost:8000/docs
```

**Ejemplo de llamada API:**

```bash
curl -X POST "http://localhost:8000/process-video" \
  -H "Content-Type: application/json" \
  -d '{
    "video_url": "https://www.youtube.com/watch?v=VIDEO_ID",
    "artifacts": ["pdf", "map", "podcast"],
    "title": "Mi Clase"
  }'
```

## 📋 Flujo del Programa

1. **Descarga y Extrae Audio** → `video.mp4` + `audio.mp3`
2. **Transcribe** → `transcription.txt`
3. **Resume** → `summary.txt`
4. **Evalúa Fidelidad** → Puntuación 0-100%
5. **Selecciona Artefactos** → [PDF, Mapa, Podcast]
6. **Genera Materiales:**
   - 📄 PDF → `study_guide_TIMESTAMP.pdf`
   - 🗺️ Mapa → `concept_map_TIMESTAMP.png`
   - 🎙️ Podcast → `podcast_TIMESTAMP.mp3`
7. **Sube a Azure** (opcional) → URLs en la nube

## 📁 Archivos Generados

Todos los archivos se guardan en la carpeta `output/`:

```
output/
├── video_123.mp4
├── audio_123.mp3
├── transcription_123.txt
├── summary_123.txt
├── study_guide_20250123_143022.pdf
├── concept_map_20250123_143022.png
└── podcast_20250123_143022.mp3
```

## 🔧 Solución de Problemas

### Error: "GEMINI_API_KEY no encontrada"
- Verifica que el archivo `.env` existe
- Confirma que la clave API está configurada correctamente

### Error al descargar video
- Verifica que la URL es válida
- Algunos videos pueden tener restricciones de descarga
- Prueba con un video diferente o usa un archivo local

### Error al generar podcast
- El sistema creará un archivo de audio básico si falla la generación
- Para mejor calidad, instala `google-cloud-texttospeech`

### Azure Storage no funciona
- El sistema funciona sin Azure (modo local)
- Para habilitar Azure, configura `AZURE_STORAGE_CONNECTION_STRING` en `.env`

## 🎯 Para la Hackathon

Este sistema te permite:

1. **Procesar clases grabadas** automáticamente
2. **Generar materiales de estudio** en segundos
3. **Ayudar a estudiantes** con contenido personalizado
4. **Reducir deserción** facilitando el aprendizaje

**Ejemplo de uso para la demo:**

```bash
# Procesar una clase de ejemplo
python cli.py \
  --video-url "URL_DE_TU_CLASE" \
  --artifacts pdf,map,podcast \
  --title "Introducción a Python - Clase 1"
```

## 📞 Soporte

- Documentación completa: `README.md`
- Documentación API: http://localhost:8000/docs (cuando el servidor esté corriendo)
- Código fuente: Todo en carpeta `src/`

## 🎉 Tips para la Presentación

1. Muestra el flujo completo con un video corto (2-3 minutos)
2. Destaca los PDFs generados como material de estudio
3. Muestra el mapa conceptual (es muy visual)
4. Menciona que todo es automático y escalable
5. Resalta el impacto en reducción de deserción estudiantil

¡Buena suerte en la hackathon! 🚀
