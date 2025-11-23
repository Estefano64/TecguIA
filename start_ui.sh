#!/bin/bash

# Script para iniciar la interfaz web de TecguIA

echo "=================================="
echo "🎓 TecguIA - Interfaz Web"
echo "=================================="
echo ""

# Verificar que existe .env
if [ ! -f .env ]; then
    echo "⚠️  Archivo .env no encontrado. Copiando desde .env.example..."
    cp .env.example .env
    echo "✅ Archivo .env creado"
fi

# Crear directorios si no existen
mkdir -p output temp

# Inicializar base de datos
echo "🗄️  Inicializando base de datos..."
python -c "from src.database import init_db; init_db()" 2>/dev/null

echo ""
echo "🚀 Iniciando interfaz web..."
echo ""
echo "📱 La aplicación se abrirá en tu navegador"
echo "🌐 URL: http://localhost:8501"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

# Iniciar Streamlit
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
