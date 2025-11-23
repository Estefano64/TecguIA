#!/bin/bash

# Script para ejecutar TecguIA

echo "==================================="
echo "TecguIA - Inicializando Sistema"
echo "==================================="

# Verificar que existe .env
if [ ! -f .env ]; then
    echo "⚠️  Archivo .env no encontrado. Copiando desde .env.example..."
    cp .env.example .env
    echo "⚠️  Por favor, edita .env con tus credenciales antes de continuar."
    exit 1
fi

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

# Crear directorios necesarios
mkdir -p output temp

# Inicializar base de datos
echo "🗄️  Inicializando base de datos..."
python -c "from src.database import init_db; init_db(); print('✓ Base de datos inicializada')"

# Preguntar modo de ejecución
echo ""
echo "Selecciona el modo de ejecución:"
echo "1) API (FastAPI - servidor web)"
echo "2) CLI (línea de comandos)"
read -p "Selección [1/2]: " mode

if [ "$mode" == "1" ]; then
    echo ""
    echo "🚀 Iniciando API en http://localhost:8000"
    echo "📖 Documentación disponible en http://localhost:8000/docs"
    echo ""
    python main.py
elif [ "$mode" == "2" ]; then
    echo ""
    echo "Modo CLI activado. Usa:"
    echo "  python cli.py --help"
    echo ""
    echo "Ejemplo:"
    echo "  python cli.py --video-url 'URL' --artifacts pdf,map,podcast"
    echo ""
else
    echo "❌ Opción inválida"
    exit 1
fi
