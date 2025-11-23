# 🎨 Guía de la Interfaz Web - TecguIA

## 🚀 Inicio Rápido

### Opción 1: Script automático (Recomendado)
```bash
./start_ui.sh
```

### Opción 2: Manual
```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

---

## 📱 Navegación de la Interfaz

### 🏠 Página de Inicio
- **Problema y Solución**: Contexto de la hackathon
- **Características Principales**: Vista general de capacidades
- **Call to Action**: Botón para comenzar a procesar

### 🎬 Procesar Video

**Paso 1: Seleccionar Fuente**
- 🌐 **URL**: Pega el link de YouTube, Vimeo, etc.
- 💾 **Archivo Local**: Arrastra y suelta tu video

**Paso 2: Configurar**
- ✏️ **Título**: Nombre para los materiales (opcional)
- ☑️ **Artefactos**: Selecciona qué generar:
  - 📄 Guía de Estudio (PDF)
  - 🗺️ Mapa Conceptual
  - 🎙️ Podcast

**Paso 3: Procesar**
- Click en "🚀 Procesar Video"
- Barra de progreso en tiempo real
- 7 pasos claramente indicados

**Paso 4: Descargar**
- Botones de descarga individuales
- Preview del mapa conceptual
- ID de procesamiento para referencia

### 📊 Historial
- Lista de todos los videos procesados
- Estado de cada procesamiento
- Descargar artefactos antiguos
- Información de calidad (fidelidad)

### ℹ️ Acerca de
- Misión del proyecto
- Tecnologías utilizadas
- Estadísticas del sistema
- Información del equipo

---

## 🎨 Características de la UI

### Diseño Visual
- ✨ **Gradientes modernos** en componentes clave
- 🎨 **Código de colores** consistente
- 📱 **Responsive**: Funciona en móviles y tablets
- 🌈 **Tema personalizado** en colores púrpura/azul

### Interactividad
- ⚡ **Feedback inmediato** en cada acción
- 📊 **Barra de progreso** detallada
- 🔔 **Mensajes de estado** claros
- 💾 **Persistencia** de datos entre sesiones

### Usabilidad
- 🧭 **Navegación intuitiva** con sidebar
- 📖 **Instrucciones claras** en cada paso
- 🎯 **Call-to-actions** prominentes
- ❌ **Manejo de errores** informativo

---

## 💡 Tips para la Demo de la Hackathon

### Preparación
1. **Tener videos de prueba listos** (2-3 minutos cada uno)
2. **Pre-generar un ejemplo** para mostrar resultados instantáneamente
3. **Tener los artefactos abiertos** en pestañas para comparar

### Durante la Presentación

**Inicio (30 seg)**
- Muestra la página de inicio
- Destaca el problema (40% deserción)
- Menciona la solución automática

**Demo en Vivo (2-3 min)**
- Selecciona URL de video pregrabado
- Marca todos los artefactos
- Inicia procesamiento
- Mientras procesa, explica cada paso

**Mostrar Resultados (1-2 min)**
- Abre el PDF generado
- Muestra el mapa conceptual (muy visual!)
- Menciona el podcast (reproducir 10 segundos)
- Destaca la calidad de transcripción

**Impacto (30 seg)**
- Sidebar: muestra estadísticas
- Historial: múltiples videos procesados
- Menciona escalabilidad

### Mensajes Clave
- ✅ "Procesamiento completamente automático"
- ✅ "De 1 hora de clase a materiales en 5 minutos"
- ✅ "3 formatos diferentes para distintos estilos de aprendizaje"
- ✅ "Reduce deserción ayudando a estudiantes rezagados"
- ✅ "Escalable a nivel institucional"

---

## 🎯 Ventajas de la UI para la Rúbrica

### Usabilidad (20% → Excelente)
- ✅ **Intuitiva**: No requiere instrucciones
- ✅ **Atractiva**: Diseño profesional con gradientes
- ✅ **Orientación clara**: Tooltips y mensajes guía
- ✅ **Feedback visual**: Progreso en tiempo real

### Innovación (+puntos)
- 🎨 No solo es funcional, es **visualmente impresionante**
- 📱 Interfaz moderna tipo **app nativa**
- 🔄 Procesamiento **en tiempo real visible**

### Impacto (+puntos)
- 📊 **Estadísticas en vivo** demuestran uso
- 📈 **Historial** muestra escalabilidad
- 🎯 Mensaje del problema **front and center**

---

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install streamlit
```

### La UI no se abre en el navegador
1. Verifica que el puerto 8501 esté libre
2. Abre manualmente: http://localhost:8501

### Error al procesar video
- Revisa que `.env` tenga las API keys configuradas
- Verifica que los directorios `output/` y `temp/` existan
- Revisa logs en la terminal

### Video local no sube
- Verifica el formato (mp4, avi, mov, mkv, webm)
- Tamaño máximo: ~200MB (configurable)

---

## 📸 Screenshots para la Presentación

Captura estas pantallas para tu presentación:

1. **Página de inicio** - Muestra el problema y solución
2. **Formulario de procesamiento** - Interfaz limpia
3. **Progreso en ejecución** - Barra de progreso
4. **Resultados completados** - Artefactos generados
5. **Preview del mapa** - Visual impresionante
6. **Historial** - Múltiples procesamientos

---

## 🎉 Personalización Rápida

### Cambiar colores (archivo `.streamlit/config.toml`):
```toml
[theme]
primaryColor = "#TU_COLOR"
backgroundColor = "#ffffff"
textColor = "#1a237e"
```

### Agregar logo del equipo:
En `app.py`, línea ~119, cambia:
```python
st.image("URL_DE_TU_LOGO", width=80)
```

### Cambiar puerto:
```bash
streamlit run app.py --server.port 8080
```

---

## 🏆 Ventajas Competitivas

Comparado con solo CLI o API:

| Aspecto | CLI | API REST | **UI Web** |
|---------|-----|----------|-----------|
| Facilidad de uso | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Visual | ❌ | ❌ | ✅✅✅ |
| Demo en hackathon | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Accesibilidad | Técnicos | Developers | **Todos** |
| Wow factor | Bajo | Medio | **Alto** |

---

¡Buena suerte en la hackathon! 🚀

La UI es tu **arma secreta** para impresionar a los jueces.
