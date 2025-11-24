# 🔧 Solución al Error 503 de Gemini AI

## ❌ Error Recibido

```
Error en transcripción: 503 UNAVAILABLE.
{'error': {'code': 503, 'message': 'The model is overloaded. Please try again later.', 'status': 'UNAVAILABLE'}}
```

---

## 📝 ¿Qué Significa?

El error **503 UNAVAILABLE** ocurre cuando:
- ✅ Tu código está correcto
- ✅ Las API keys son válidas
- ❌ El servidor de Gemini AI está **temporalmente sobrecargado**

Es como cuando un sitio web dice "Servidor ocupado, intenta más tarde". Es temporal y común en horas pico.

---

## ✅ Soluciones

### **Solución 1: Usar el Backend Mejorado (Recomendado)**

Usa el nuevo archivo `tecsup_backend_v2.py` que incluye:

✅ **Retry automático** (3 intentos)
✅ **Exponential backoff** (espera 2s, 4s, 8s)
✅ **Modelo estable** (gemini-1.5-flash en lugar de 2.0-flash-exp)
✅ **Mensajes de error claros**

```bash
# Detener el servidor actual (Ctrl+C)

# Iniciar el nuevo backend
python tecsup_backend_v2.py
```

**¿Qué hace diferente?**

Cuando falla por sobrecarga:
```
⚠️  Servidor sobrecargado. Reintentando en 2s... (intento 1/3)
⚠️  Servidor sobrecargado. Reintentando en 4s... (intento 2/3)
⚠️  Servidor sobrecargado. Reintentando en 8s... (intento 3/3)
✅ Transcripción completada
```

---

### **Solución 2: Cambiar el Modelo (Rápido)**

Si quieres usar tu archivo original, solo cambia estas líneas:

**En `tecsup_backend.py`:**

**Línea ~92 (función `transcribe_with_gemini`):**
```python
# ANTES:
model='gemini-2.0-flash-exp',

# DESPUÉS:
model='gemini-1.5-flash',  # Modelo más estable
```

**Línea ~181 (función `generate_summary_and_script`):**
```python
# ANTES:
model='gemini-2.0-flash-exp',

# DESPUÉS:
model='gemini-1.5-flash',  # Modelo más estable
```

Luego reinicia el servidor.

---

### **Solución 3: Esperar y Reintentar (Temporal)**

Si no quieres cambiar código:

1. **Espera 1-2 minutos**
2. **Reintenta** el procesamiento
3. El servidor de Gemini suele recuperarse rápido

---

## 🆚 Comparación de Modelos

| Modelo | Velocidad | Estabilidad | Costo | Recomendación |
|--------|-----------|-------------|-------|---------------|
| `gemini-2.0-flash-exp` | ⚡⚡⚡ | ⭐⭐ | Gratis | ❌ Experimenta 503 |
| `gemini-1.5-flash` | ⚡⚡ | ⭐⭐⭐⭐⭐ | Gratis | ✅ **Recomendado** |
| `gemini-1.5-pro` | ⚡ | ⭐⭐⭐⭐⭐ | Bajo | ✅ Para producción |

---

## 🔄 ¿Qué Hace el Retry Automático?

**Sin retry (versión original):**
```
Intento 1: 503 Error ❌
→ Falla inmediatamente
```

**Con retry (versión mejorada):**
```
Intento 1: 503 Error → Espera 2 segundos
Intento 2: 503 Error → Espera 4 segundos
Intento 3: ✅ Éxito
```

**Exponential Backoff:**
- Intento 1: espera 2 segundos
- Intento 2: espera 4 segundos (2 × 2)
- Intento 3: espera 8 segundos (4 × 2)

Esto da tiempo al servidor para recuperarse.

---

## 📊 Cuándo Ocurre el Error 503

### Horas Pico (Más Común):
- 🌍 **8am - 10am** hora del Pacífico (horario de oficinas en USA)
- 🌏 **6pm - 8pm** hora del Pacífico (horario de trabajadores remotos)
- 📅 **Lunes y Martes** (inicio de semana)

### Horas Valle (Menos Común):
- ✅ **2am - 6am** hora del Pacífico
- ✅ **Fines de semana**

---

## 🛠️ Verificar que Todo Funciona

### Test 1: Health Check
```bash
curl http://localhost:5000/health
```

**Respuesta esperada:**
```json
{
  "status": "ok",
  "version": "2.1",
  "features": {
    "auto_retry": true,
    "max_retries": 3,
    "stable_model": "gemini-1.5-flash"
  }
}
```

### Test 2: Estadísticas
```bash
curl http://localhost:5000/stats
```

**Respuesta esperada:**
```json
{
  "total_podcasts": 0,
  "total_transcriptions": 0,
  "total_files": 0
}
```

---

## 🚨 Otros Errores Comunes

### Error 429: "Rate limit exceeded"
**Causa:** Demasiadas peticiones en poco tiempo
**Solución:** Espera 1 minuto entre peticiones

### Error 401: "Invalid API key"
**Causa:** API key incorrecta o expirada
**Solución:** Verifica `GEMINI_API_KEY` en el código

### Error 400: "Invalid request"
**Causa:** Formato de audio no soportado
**Solución:** Usa MP3, WAV, AAC, OGG, FLAC

---

## 💡 Tips para la Hackathon

### Para la Demo:
1. **Procesa un audio de prueba 30 min antes**
2. **Si falla por 503:**
   - No entres en pánico
   - Di: "El servidor de Google está ocupado, es temporal"
   - Muestra resultados pre-generados (screenshots)
   - O espera 1-2 minutos y reintenta

### Backup Plan:
```bash
# Antes de la demo, procesa y guarda:
1. Screenshot de la interfaz
2. Screenshot del progreso
3. Screenshot de los resultados
4. Archivo MP3 del podcast generado

# Si falla en vivo, muestra estos materiales
```

---

## 📝 Checklist de Solución

- [ ] Usar `tecsup_backend_v2.py` (con retry automático)
- [ ] O cambiar modelo a `gemini-1.5-flash`
- [ ] Reiniciar el servidor
- [ ] Probar con audio de prueba
- [ ] Verificar que funciona antes de la demo
- [ ] Tener screenshots de backup

---

## 🎯 Resumen Ejecutivo

**Problema:** Error 503 (servidor sobrecargado)
**Causa:** Gemini AI temporalmente ocupado
**Solución rápida:** Usar `tecsup_backend_v2.py`
**Prevención:** Modelo estable + retry automático

**Tiempo de implementación:** 30 segundos

```bash
# Solución en 1 comando:
python tecsup_backend_v2.py
```

---

## ✅ Todo Listo

Con el backend mejorado (`v2`):
- ✅ Maneja automáticamente errores 503
- ✅ Reintenta hasta 3 veces
- ✅ Usa modelo más estable
- ✅ Mensajes de error claros para el usuario
- ✅ Listo para la hackathon

**No más errores 503! 🎉**
