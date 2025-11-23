# TecguIA - Sistema de Procesamiento de Videos Educativos

Sistema automatizado para convertir videos educativos en materiales de estudio usando IA, desarrollado para la hackathon "Educación Superior sin Deserción Estudiantil".

## 🎯 Características

- **Descarga y procesamiento de videos** desde múltiples fuentes
- **Transcripción automática** usando Gemini AI
- **Resúmenes inteligentes** de contenido educativo
- **Generación de materiales de estudio**:
  - 📄 Guías de estudio en PDF
  - 🗺️ Mapas conceptuales visuales
  - 🎙️ Podcasts de resumen
- **Almacenamiento en la nube** (Azure Blob Storage)
- **Evaluación de fidelidad** de transcripciones

## 🚀 Instalación

```bash
# Clonar repositorio
git clone <repository-url>
cd TecguIA

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales
```

## 📋 Configuración

1. Obtener API keys:
   - Gemini API: https://makersuite.google.com/app/apikey
   - Mistral API: https://console.mistral.ai/

2. Configurar Azure Blob Storage (opcional):
   - Crear cuenta de Azure Storage
   - Obtener connection string
   - Configurar en .env

## 🎓 Uso

### 🌟 Modo UI Web (Recomendado para Demo)

```bash
./start_ui.sh
```

O manualmente:
```bash
streamlit run app.py
```

Acceder a **http://localhost:8501** para la interfaz web completa con:
- 🎨 Interfaz visual atractiva e intuitiva
- 📊 Barra de progreso en tiempo real
- 📥 Drag & drop para videos
- 👁️ Preview de resultados
- 📱 Responsive (funciona en móviles)

**Perfecto para la demo de la hackathon!**

### Modo API (FastAPI)

```bash
python main.py
```

Acceder a http://localhost:8000/docs para ver la documentación interactiva.

### Modo CLI

```bash
python cli.py --video-url "https://youtube.com/watch?v=..." --artifacts pdf,map,podcast
```

## 📁 Estructura del Proyecto

```
TecguIA/
├── src/
│   ├── video_processor.py      # Descarga y extracción de audio
│   ├── transcription.py        # Transcripción con Gemini
│   ├── summarization.py        # Resumen de contenido
│   ├── fidelity_evaluator.py  # Evaluación de calidad
│   ├── generators/
│   │   ├── pdf_generator.py   # Generación de PDFs
│   │   ├── map_generator.py   # Mapas conceptuales
│   │   └── podcast_generator.py # Podcasts
│   ├── storage.py              # Azure Blob Storage
│   └── database.py             # Modelos de BD
├── app.py                      # 🌟 Interfaz Web (Streamlit)
├── main.py                     # API FastAPI
├── cli.py                      # Interfaz de línea de comandos
├── start_ui.sh                 # Script para iniciar UI
├── UI_GUIDE.md                 # Guía completa de la UI
└── requirements.txt
```

## 🔄 Flujo de Procesamiento

1. **Descarga video y extrae audio** → `video.mp4` + `audio.mp3`
2. **Transcribe audio** → `transcription.txt`
3. **Resume transcripción** → `summary.txt`
4. **Evalúa fidelidad** → Porcentaje guardado en BD
5. **Usuario selecciona artefactos** → [PDF, Mapa, Podcast]
6. **Genera materiales** → Archivos subidos a Azure Blob

## 📝 Licencia

MIT License
