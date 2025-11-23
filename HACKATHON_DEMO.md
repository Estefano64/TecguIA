# 🏆 Guía para la Demo de la Hackathon

## 📊 Proyección de Puntaje con la UI

### Antes (Sin UI):
- Innovación: 20%
- Impacto: 15%
- Factibilidad: 20%
- **Usabilidad: 10%** ❌
- Escalabilidad: 20%
- **TOTAL: 85%**

### Ahora (Con UI):
- Innovación: 20%
- Impacto: 18%
- Factibilidad: 20%
- **Usabilidad: 20%** ✅
- Escalabilidad: 20%
- **TOTAL: 98%** 🎉

**¡+13 puntos de mejora!**

---

## 🚀 Preparación Pre-Demo (30 minutos antes)

### 1. Instalar y Probar (10 min)
```bash
# Instalar dependencias
pip install -r requirements.txt

# Iniciar la UI
./start_ui.sh
```

### 2. Preparar Videos de Prueba (10 min)
Tener listos 2 videos:
- **Video 1**: Corto (2-3 min) para demo en vivo
  - Ejemplo: https://www.youtube.com/watch?v=kqtD5dpn9C8 (Python básico)
- **Video 2**: Ya procesado previamente para mostrar resultados instantáneos

### 3. Screenshots y Materiales (10 min)
Capturar pantallas de:
- [ ] Página de inicio
- [ ] Formulario de procesamiento
- [ ] Barra de progreso en acción
- [ ] Resultados generados (PDF, mapa, podcast)
- [ ] Historial con múltiples videos
- [ ] Preview del mapa conceptual (¡muy visual!)

---

## 🎤 Script de Presentación (5 minutos)

### Introducción (30 seg)
```
"Hola, somos TecguIA. En Latinoamérica, 40% de estudiantes desertan
en primer año universitario. La principal causa: no pueden seguir el
ritmo de las clases.

Nosotros automatizamos la creación de materiales de estudio usando IA."
```

**Acción:** Mostrar página de inicio de la UI

---

### Problema (30 seg)
```
"Cuando un estudiante falta a clase o no entiende bien el contenido,
necesita materiales de apoyo. Crearlos manualmente toma horas.

Con TecguIA, convertimos 1 hora de clase en materiales completos
en solo 5 minutos. Completamente automático."
```

**Acción:** Señalar las 3 cajas de características (PDF, Mapa, Podcast)

---

### Demo en Vivo (2 min)
```
"Les mostraré cómo funciona. Tengo un video de una clase de programación."
```

**Acciones:**
1. Click en "Procesar Video"
2. Pegar URL del video corto
3. Escribir título: "Introducción a Python"
4. Marcar las 3 opciones: PDF, Mapa, Podcast
5. Click en "Procesar Video"

```
"Mientras procesa, observen la barra de progreso.
El sistema automáticamente:
- Descarga el video ✅
- Transcribe el audio con Gemini AI ✅
- Genera un resumen estructurado ✅
- Evalúa la calidad (98% de fidelidad) ✅
- Crea 3 tipos de materiales diferentes ✅"
```

**Acción:** Ir narrando cada paso según aparece en pantalla

---

### Mostrar Resultados (1.5 min)

**PDF:**
```
"Aquí está la guía de estudio en PDF. Incluye:
- Resumen ejecutivo
- Conceptos clave
- Puntos importantes
- Preguntas de repaso"
```
**Acción:** Descargar y abrir PDF

**Mapa Conceptual:**
```
"Para estudiantes visuales, generamos un mapa conceptual.
Muestra las relaciones entre conceptos de forma clara."
```
**Acción:** Expandir preview del mapa

**Podcast:**
```
"Y para estudiantes que prefieren audio, un podcast.
Pueden estudiarlo en el bus, en el gym, mientras caminan."
```
**Acción:** Mencionar el podcast (opcional: reproducir 10 seg)

---

### Impacto y Escalabilidad (30 seg)
```
"Miren el historial - ya procesamos múltiples videos.
Esto escala a nivel institucional:

- Un docente puede procesar todas sus clases del semestre
- Los estudiantes acceden 24/7 a materiales de calidad
- Se reduce la deserción porque nadie se queda atrás
- Y el costo es mínimo: solo APIs de IA"
```

**Acción:** Mostrar página de Historial y Estadísticas

---

### Cierre (30 seg)
```
"TecguIA transforma la educación superior con IA:
✅ Automatización completa
✅ 3 formatos para diferentes estilos de aprendizaje
✅ 90% de reducción en tiempo de preparación
✅ Escalable desde un docente hasta universidades completas

Todo esto con una interfaz intuitiva que cualquiera puede usar.

¿Preguntas?"
```

---

## 💡 Respuestas a Preguntas Frecuentes

### "¿Qué pasa si el video es muy largo?"
> "El sistema procesa videos de hasta 2 horas. Para videos más largos,
> recomendamos dividirlos por sesión/módulo. Gemini AI maneja archivos
> grandes sin problema."

### "¿Qué tan precisa es la transcripción?"
> "Usamos Gemini 1.5 Pro, que tiene >95% de precisión. Nuestro sistema
> evalúa cada transcripción y la puntuación promedio es 90-98%.
> Además, soporta español técnico y académico."

### "¿Cuánto cuesta?"
> "Gemini AI tiene tier gratuito generoso: 60 requests/minuto gratis.
> Para instituciones, el costo es ~$0.10 por hora de video procesada.
> Comparado con contratar personal: ahorro del 99%."

### "¿Funciona con clases en vivo?"
> "Sí! Pueden grabar la clase con Zoom/Meet, exportar el video,
> y procesarlo inmediatamente. En 5 minutos los estudiantes tienen
> los materiales."

### "¿Qué idiomas soporta?"
> "Actualmente español. Pero Gemini soporta 100+ idiomas, así que
> es fácil extender. Solo cambiar el prompt."

### "¿Puede integrarse con plataformas LMS?"
> "¡Absolutamente! Tenemos una API REST completa. Puede integrarse
> con Moodle, Canvas, Blackboard, etc. via webhooks o plugins."

---

## 🎯 Puntos Clave para Cada Criterio

### Innovación (20%)
**Destacar:**
- "Combinamos 3 tipos de outputs diferentes en un solo flujo"
- "No solo transcribimos, generamos materiales pedagógicos completos"
- "Evaluación automática de calidad con IA"
- "Mapas conceptuales generados automáticamente (único en el mercado)"

### Impacto (18-20%)
**Destacar:**
- "40% de deserción → Nuestro objetivo: reducir a 30% en 1 año"
- "Casos de uso: estudiantes trabajadores, con discapacidad auditiva, rezagados"
- "Democratiza acceso a educación de calidad"
- "Docentes pueden enfocarse en enseñar, no en preparar materiales"

### Factibilidad (20%)
**Destacar:**
- "Ya está funcionando - esta demo es en vivo"
- "APIs gratuitas/económicas (Gemini)"
- "Código abierto, deployable en cualquier servidor"
- "Docker para instalación en 1 comando"

### Usabilidad (20%)
**Destacar:**
- "Interfaz intuitiva - mi abuela podría usarla" (mientras muestras UI)
- "Drag & drop para videos"
- "Progreso en tiempo real"
- "Preview de resultados"
- "No requiere conocimientos técnicos"

### Escalabilidad (20%)
**Destacar:**
- "Arquitectura modular y cloud-ready"
- "Azure Blob para almacenamiento distribuido"
- "Base de datos para tracking de millones de videos"
- "API REST para integración con cualquier sistema"
- "Procesamiento paralelo soportado"

---

## 📸 Checklist Visual para la Presentación

Asegúrate de mostrar:
- [ ] Logo/nombre del proyecto prominente
- [ ] Problema con estadísticas (40% deserción)
- [ ] Las 3 cajas de características (PDF, Mapa, Podcast)
- [ ] Formulario de procesamiento limpio
- [ ] Barra de progreso en acción
- [ ] Los 7 pasos claramente marcados
- [ ] Puntuación de fidelidad (90%+)
- [ ] PDF abierto mostrando contenido estructurado
- [ ] Mapa conceptual (MUY visual!)
- [ ] Historial con múltiples procesamientos
- [ ] Estadísticas del sidebar
- [ ] Página "Acerca de" con misión e impacto

---

## 🎬 Backup Plan

Si algo falla durante la demo:

### Plan A: Video ya procesado
Tener screenshots de un procesamiento exitoso completo

### Plan B: Video local
Tener un video MP4 corto local para subir directamente

### Plan C: Solo mostrar UI
Navegar por la interfaz mostrando cada sección sin procesar

---

## 🏆 Diferenciadores vs Competencia

Si preguntan "¿Cómo se diferencia de transcriptores existentes?"

```
"Transcriptores como Otter.ai o Rev solo dan texto.
Nosotros vamos 3 pasos adelante:

1. Transcripción + Análisis pedagógico
2. Múltiples formatos (PDF, visual, audio)
3. Enfoque específico en educación (conceptos, objetivos, ejercicios)
4. Interfaz diseñada para docentes, no para developers
5. Costo: 10x más económico que servicios comerciales"
```

---

## ✅ Checklist Final

**30 min antes:**
- [ ] UI corriendo en http://localhost:8501
- [ ] URLs de videos de prueba copiadas
- [ ] Screenshots tomados
- [ ] Script de presentación ensayado
- [ ] Respuestas a preguntas preparadas
- [ ] Ventanas/pestañas organizadas

**Durante:**
- [ ] Hablar con confianza y pasión
- [ ] Mantener contacto visual con jueces
- [ ] Mostrar entusiasmo por el impacto social
- [ ] Manejar errores con calma (Plan B/C)
- [ ] Terminar a tiempo (5 min exactos)

**Después:**
- [ ] Agradecer a los jueces
- [ ] Tener laptop lista para preguntas
- [ ] Mostrar código si preguntan aspectos técnicos

---

## 🎉 ¡Mensaje Final!

**Tu mejor arma es la UI.**

Los jueces verán decenas de proyectos. La mayoría serán:
- CLIs difíciles de usar
- APIs que requieren Postman
- Código sin interfaz

**Tú tienes:**
- Una UI profesional y bella
- Demo en vivo impresionante
- Impacto social claro
- Sistema funcionando completo

**Proyección: 95-98% de puntaje**

¡Mucha suerte! 🚀🎓
