# 🎓 TECSUP - Sistema de Generación de Materiales Educativos con IA

## Hackathon: Educación Superior sin Deserción Estudiantil

Sistema mejorado y profesional para convertir grabaciones de clases de TECSUP en materiales educativos automáticamente.

---

## ✨ Características Principales

### 🎯 Funcionalidades

1. **Drag & Drop Intuitivo**
   - Arrastra archivos de audio directamente
   - Soporte para múltiples formatos (MP3, WAV, AAC, OGG, FLAC, M4A)
   - Validación automática de archivos

2. **Procesamiento Inteligente**
   - 📝 Transcripción automática con Gemini AI
   - 📊 Análisis de contenido educativo
   - 📋 Generación de resumen estructurado
   - 🎙️ Creación de podcast profesional con ElevenLabs

3. **Visualización de Progreso**
   - 5 pasos visuales claramente marcados
   - Barra de progreso animada
   - Indicadores de estado en tiempo real
   - Animaciones profesionales

4. **Resultados Completos**
   - Transcripción completa del audio
   - Resumen educativo estructurado:
     * Tema principal
     * Objetivos de aprendizaje
     * Conceptos clave
     * Puntos importantes
     * Términos técnicos
   - Guion del podcast
   - Audio MP3 del podcast
   - Reproductor integrado
   - Descarga de todos los archivos

5. **Interfaz Profesional**
   - Diseño moderno con gradientes
   - Colores corporativos de TECSUP
   - Responsive (móvil, tablet, desktop)
   - Animaciones suaves
   - Notificaciones visuales

---

## 🚀 Instalación

### Requisitos Previos

```bash
# Python 3.8+
python --version

# pip
pip --version
```

### Paso 1: Instalar Dependencias

```bash
pip install flask flask-cors google-generativeai elevenlabs werkzeug
```

### Paso 2: Crear Carpetas Necesarias

El sistema creará automáticamente las carpetas, pero puedes crearlas manualmente:

```bash
mkdir uploads
mkdir output
```

---

## 🎮 Uso

### Paso 1: Iniciar el Backend

```bash
python tecsup_backend.py
```

Deberías ver:
```
================================================================================
🎓 TECSUP - SISTEMA DE GENERACIÓN DE MATERIALES EDUCATIVOS CON IA
================================================================================
Hackathon: Educación Superior sin Deserción Estudiantil

Servidor disponible en: http://localhost:5000
Carpeta de uploads: uploads
Carpeta de output: output

Endpoints disponibles:
  - POST /upload_audio  : Subir archivo de audio
  - POST /process_audio : Procesar audio y generar materiales
  - GET  /download/<file>: Descargar archivo generado
  - GET  /health        : Estado del servidor
  - GET  /stats         : Estadísticas del sistema
================================================================================
```

### Paso 2: Abrir la Interfaz Web

Abre el archivo `tecsup_interface.html` en tu navegador:

- **Chrome/Edge**: Haz doble clic en el archivo
- **Directo**: `file:///ruta/completa/tecsup_interface.html`

---

## 📱 Cómo Usar la Interfaz

### Opción 1: Drag & Drop (Recomendado)

1. **Arrastra** tu archivo de audio a la zona de drop
2. Espera confirmación de carga exitosa
3. Click en **"Generar Materiales Educativos"**
4. Observa el progreso en tiempo real (5 pasos)
5. Descarga los materiales generados

### Opción 2: Selección Manual

1. Click en **"Seleccionar Archivo"**
2. Busca y selecciona tu archivo de audio
3. Click en **"Generar Materiales Educativos"**
4. Espera el procesamiento
5. Descarga resultados

---

## 🎨 Características Visuales

### Progreso en 5 Pasos

1. **📤 Subiendo** - Carga del archivo al servidor
2. **🎤 Transcribiendo** - Gemini AI transcribe el audio
3. **🧠 Analizando** - Análisis del contenido educativo
4. **🎙️ Generando** - Creación del podcast con ElevenLabs
5. **✅ Completado** - Materiales listos

### Animaciones

- ✨ Fade in/out suaves
- 🎯 Pulse en elementos activos
- 📊 Barras de progreso animadas
- 🔄 Transiciones fluidas
- 💫 Efectos hover interactivos

### Colores TECSUP

- **Primario**: #FF6B35 (Naranja)
- **Secundario**: #004E89 (Azul)
- **Acento**: #F77F00 (Naranja claro)
- **Éxito**: #06A77D (Verde)

---

## 📊 Estructura de Archivos Generados

```
output/
├── transcription_20241124_143022.txt  # Transcripción completa
├── summary_20241124_143022.txt        # Resumen educativo
├── script_20241124_143022.txt         # Guion del podcast
└── podcast_20241124_143022.mp3        # Audio del podcast
```

---

## 🔧 API Endpoints

### POST /upload_audio

Sube un archivo de audio.

**Body:** FormData con campo `audio`

**Response:**
```json
{
  "success": true,
  "filename": "20241124_143022_clase.mp3",
  "filepath": "uploads/20241124_143022_clase.mp3",
  "size_mb": 5.23,
  "message": "Archivo subido exitosamente"
}
```

### POST /process_audio

Procesa el audio y genera materiales.

**Body:**
```json
{
  "audio_path": "uploads/20241124_143022_clase.mp3"
}
```

**Response:**
```json
{
  "success": true,
  "transcription": "Transcripción completa...",
  "summary": "Resumen estructurado...",
  "script": "Guion del podcast...",
  "files": {
    "transcription": "transcription_20241124_143022.txt",
    "summary": "summary_20241124_143022.txt",
    "script": "script_20241124_143022.txt",
    "podcast": "podcast_20241124_143022.mp3"
  },
  "metadata": {
    "file_size_mb": 5.23,
    "processing_time_seconds": 45.67,
    "transcription_length": 5234,
    "timestamp": "2024-11-24T14:30:22.123456"
  }
}
```

### GET /download/<filename>

Descarga un archivo generado.

### GET /health

Estado del servidor.

### GET /stats

Estadísticas del sistema.

**Response:**
```json
{
  "total_podcasts": 12,
  "total_transcriptions": 12,
  "total_files": 48
}
```

---

## 🎯 Para la Hackathon

### Ventajas Competitivas

1. **Interfaz Profesional** ⭐⭐⭐⭐⭐
   - Drag & drop intuitivo
   - Visualización de progreso
   - Diseño moderno y atractivo

2. **Funcionalidad Completa** ⭐⭐⭐⭐⭐
   - 4 tipos de salida (transcripción, resumen, guion, audio)
   - Descarga individual de cada archivo
   - Reproductor de audio integrado

3. **Experiencia de Usuario** ⭐⭐⭐⭐⭐
   - Sin conocimientos técnicos requeridos
   - Feedback visual constante
   - Notificaciones claras

4. **Tecnología de Punta** ⭐⭐⭐⭐⭐
   - Gemini AI (Google)
   - ElevenLabs (síntesis de voz profesional)
   - Flask moderno

### Demo para Jueces

**Script de 3 minutos:**

```
1. [30 seg] Introducción
   "Somos [equipo]. En TECSUP, estudiantes pierden clases por trabajo.
   Creamos un sistema que convierte grabaciones en materiales de estudio."

2. [90 seg] Demo en Vivo
   - Mostrar interfaz
   - Arrastrar archivo de audio
   - Explicar los 5 pasos mientras procesa
   - Mostrar resultados (transcripción, resumen, podcast)
   - Reproducir 10 seg del podcast

3. [30 seg] Impacto
   "Reduce tiempo de preparación de 2 horas a 5 minutos.
   Ayuda a estudiantes que trabajan.
   Materiales disponibles 24/7.
   Reduce deserción estudiantil."

4. [30 seg] Tecnología
   "Usa Gemini AI de Google y ElevenLabs.
   Interfaz drag & drop profesional.
   Escalable a nivel institucional."
```

### Puntos a Destacar

- ✅ **Usabilidad**: Drag & drop, sin tecnicismos
- ✅ **Visual**: Interfaz moderna y animada
- ✅ **Completo**: 4 tipos de salida
- ✅ **Rápido**: 5 minutos vs 2 horas manual
- ✅ **Escalable**: API REST para integración

---

## 🐛 Solución de Problemas

### Error: "No se pudo conectar al servidor"

**Solución:**
```bash
# Verificar que el backend esté corriendo
python tecsup_backend.py

# Verificar el puerto
curl http://localhost:5000/health
```

### Error: "Formato no válido"

**Solución:**
- Usa archivos: MP3, WAV, AAC, OGG, FLAC, M4A
- Verifica que el archivo no esté corrupto
- Tamaño máximo: 100MB

### Error: "Error al procesar"

**Solución:**
```bash
# Verificar API keys en tecsup_backend.py
GEMINI_API_KEY = "tu_key_aqui"
ELEVENLABS_API_KEY = "tu_key_aqui"

# Verificar permisos de carpetas
chmod 755 uploads output
```

### Audio no se reproduce

**Solución:**
- Usa Chrome o Edge (mejor compatibilidad)
- Verifica que el archivo MP3 se generó en `output/`
- Descarga el archivo y reprodúcelo localmente

---

## 📈 Mejoras Futuras

### Corto Plazo
- [ ] Integración con Google Drive
- [ ] Soporte para videos (extraer audio)
- [ ] Múltiples idiomas
- [ ] Generación de quizzes

### Largo Plazo
- [ ] Integración con LMS de TECSUP
- [ ] Generación de flashcards
- [ ] Análisis de sentimiento
- [ ] Resúmenes por temas
- [ ] Chatbot interactivo sobre la clase

---

## 👥 Créditos

- **Hackathon**: Educación Superior sin Deserción Estudiantil
- **Institución**: TECSUP - Instituto de Educación Superior
- **Tecnologías**: Gemini AI (Google), ElevenLabs, Flask

---

## 📄 Licencia

Este proyecto fue desarrollado para la hackathon de educación.

---

## 🎉 ¡Buena Suerte en la Hackathon!

Recuerda:
- ✅ Probar la demo antes de presentar
- ✅ Tener un archivo de audio listo (2-3 min)
- ✅ Destacar el drag & drop y la visualización
- ✅ Mostrar los 4 tipos de salida
- ✅ Mencionar el impacto en deserción estudiantil

**¡Éxito! 🚀🎓**
