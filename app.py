"""
TecguIA - Interfaz Web
Sistema de Procesamiento de Videos Educativos con IA
"""

import streamlit as st
import os
import time
from pathlib import Path
from datetime import datetime
import tempfile

from src.video_processor import VideoProcessor
from src.transcription import AudioTranscriber
from src.summarization import TranscriptionSummarizer
from src.fidelity_evaluator import FidelityEvaluator
from src.generators import PDFGenerator, ConceptMapGenerator, PodcastGenerator
from src.storage import AzureStorageManager
from src.database import init_db, get_db, VideoProcessing, GeneratedArtifact

# Configuración de la página
st.set_page_config(
    page_title="TecguIA - Procesamiento de Videos Educativos",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1a237e;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #424242;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .success-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-size: 1.1rem;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    .artifact-card {
        background: #f5f5f5;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 2px solid #e0e0e0;
    }
    .progress-text {
        font-size: 1.1rem;
        font-weight: bold;
        color: #1a237e;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar base de datos
init_db()

# Inicializar componentes (con caché)
@st.cache_resource
def get_components():
    """Inicializa y cachea los componentes del sistema."""
    return {
        'video_processor': VideoProcessor(),
        'transcriber': AudioTranscriber(),
        'summarizer': TranscriptionSummarizer(),
        'evaluator': FidelityEvaluator(),
        'pdf_generator': PDFGenerator(),
        'map_generator': ConceptMapGenerator(),
        'podcast_generator': PodcastGenerator(),
        'storage_manager': AzureStorageManager()
    }

def main():
    """Función principal de la aplicación."""

    # Header
    st.markdown('<div class="main-header">🎓 TecguIA</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Sistema Inteligente de Procesamiento de Videos Educativos</div>',
        unsafe_allow_html=True
    )

    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
        st.title("Menú Principal")

        page = st.radio(
            "Navegar a:",
            ["🏠 Inicio", "🎬 Procesar Video", "📊 Historial", "ℹ️ Acerca de"],
            label_visibility="collapsed"
        )

        st.divider()

        st.markdown("### 📈 Estadísticas")
        db = next(get_db())
        total_processed = db.query(VideoProcessing).count()
        completed = db.query(VideoProcessing).filter_by(status="completed").count()

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total", total_processed)
        with col2:
            st.metric("Completados", completed)

        st.divider()
        st.markdown("**Hackathon:** Educación sin Deserción")
        st.markdown("**Powered by:** Gemini AI")

    # Páginas
    if page == "🏠 Inicio":
        show_home_page()
    elif page == "🎬 Procesar Video":
        show_process_page()
    elif page == "📊 Historial":
        show_history_page()
    elif page == "ℹ️ Acerca de":
        show_about_page()

def show_home_page():
    """Página de inicio."""

    # Hero section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://img.icons8.com/clouds/400/education.png", width=300)

    st.markdown("---")

    # Problema y solución
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎯 El Problema")
        st.markdown("""
        - **40%** de deserción en primer año universitario
        - Estudiantes no pueden seguir el ritmo de clases
        - Falta de materiales de estudio personalizados
        - Docentes sobrecargados de trabajo
        """)

    with col2:
        st.markdown("### ✨ Nuestra Solución")
        st.markdown("""
        - Convierte **videos de clases** en materiales de estudio
        - Genera **PDFs, mapas conceptuales y podcasts** automáticamente
        - Procesa **1 hora de clase en 5 minutos**
        - **100% automático** con inteligencia artificial
        """)

    st.markdown("---")

    # Características
    st.markdown("### 🚀 Características Principales")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-box">
            <h3>📄 Guías de Estudio</h3>
            <p>PDFs profesionales con resúmenes, conceptos clave y ejercicios</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-box">
            <h3>🗺️ Mapas Conceptuales</h3>
            <p>Visualizaciones claras de las relaciones entre conceptos</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-box">
            <h3>🎙️ Podcasts</h3>
            <p>Audio resúmenes para estudiar mientras te desplazas</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Call to action
    st.markdown("### 🎬 ¿Listo para comenzar?")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Procesar mi primer video", use_container_width=True):
            st.session_state.page = "🎬 Procesar Video"
            st.rerun()

def show_process_page():
    """Página de procesamiento de videos."""

    st.markdown("## 🎬 Procesar Video Educativo")
    st.markdown("Convierte tu video de clase en materiales de estudio automáticamente")

    st.markdown("---")

    # Formulario
    with st.form("process_form"):
        st.markdown("### 📹 Fuente del Video")

        input_type = st.radio(
            "Selecciona el origen:",
            ["🌐 URL (YouTube, Vimeo, etc.)", "💾 Archivo Local"],
            horizontal=True
        )

        video_url = None
        video_file = None

        if input_type == "🌐 URL (YouTube, Vimeo, etc.)":
            video_url = st.text_input(
                "URL del video:",
                placeholder="https://www.youtube.com/watch?v=...",
                help="Pega la URL del video que deseas procesar"
            )
        else:
            video_file = st.file_uploader(
                "Sube tu video:",
                type=['mp4', 'avi', 'mov', 'mkv', 'webm'],
                help="Sube un archivo de video desde tu computadora"
            )

        st.markdown("---")

        # Configuración
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ⚙️ Configuración")
            title = st.text_input(
                "Título del material:",
                placeholder="Ej: Introducción a Python - Clase 1",
                help="Este título aparecerá en los materiales generados"
            )

        with col2:
            st.markdown("### 📦 Artefactos a Generar")
            generate_pdf = st.checkbox("📄 Guía de Estudio (PDF)", value=True)
            generate_map = st.checkbox("🗺️ Mapa Conceptual", value=True)
            generate_podcast = st.checkbox("🎙️ Podcast de Resumen", value=True)

        st.markdown("---")

        # Botón de procesar
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit = st.form_submit_button("🚀 Procesar Video", use_container_width=True)

    # Procesamiento
    if submit:
        # Validaciones
        if input_type == "🌐 URL (YouTube, Vimeo, etc.)" and not video_url:
            st.error("❌ Por favor ingresa una URL válida")
            return

        if input_type == "💾 Archivo Local" and not video_file:
            st.error("❌ Por favor sube un archivo de video")
            return

        if not (generate_pdf or generate_map or generate_podcast):
            st.error("❌ Selecciona al menos un artefacto para generar")
            return

        # Procesar
        process_video(
            video_url=video_url,
            video_file=video_file,
            title=title or "Material Educativo",
            generate_pdf=generate_pdf,
            generate_map=generate_map,
            generate_podcast=generate_podcast
        )

def process_video(video_url, video_file, title, generate_pdf, generate_map, generate_podcast):
    """Procesa el video y genera los artefactos."""

    components = get_components()

    # Contenedor de progreso
    progress_container = st.container()

    with progress_container:
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown("### 🔄 Procesamiento en Curso")
        st.markdown("</div>", unsafe_allow_html=True)

        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            # Paso 1-2: Descarga y extracción de audio
            status_text.markdown('<p class="progress-text">📥 Paso 1/7: Descargando video y extrayendo audio...</p>', unsafe_allow_html=True)
            progress_bar.progress(10)

            if video_url:
                video_path, audio_path = components['video_processor'].process_video(
                    source=video_url,
                    is_url=True
                )
            else:
                # Guardar archivo temporal
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                    tmp_file.write(video_file.read())
                    tmp_path = tmp_file.name

                video_path, audio_path = components['video_processor'].process_video(
                    source=tmp_path,
                    is_url=False
                )

            progress_bar.progress(20)

            # Crear registro en BD
            db = next(get_db())
            processing = VideoProcessing(
                video_url=video_url,
                video_path=video_path,
                audio_path=audio_path,
                status="processing"
            )
            db.add(processing)
            db.commit()
            db.refresh(processing)

            # Paso 3-4: Transcripción
            status_text.markdown('<p class="progress-text">🎤 Paso 2/7: Transcribiendo audio con IA...</p>', unsafe_allow_html=True)
            progress_bar.progress(30)

            transcription_path = f"output/transcription_{processing.id}.txt"
            transcription = components['transcriber'].transcribe_audio(audio_path, transcription_path)

            processing.transcription_path = transcription_path
            db.commit()

            progress_bar.progress(45)

            # Paso 5: Resumen
            status_text.markdown('<p class="progress-text">📝 Paso 3/7: Generando resumen inteligente...</p>', unsafe_allow_html=True)
            progress_bar.progress(50)

            summary_path = f"output/summary_{processing.id}.txt"
            summary = components['summarizer'].summarize(transcription, summary_path)

            processing.summary_path = summary_path
            db.commit()

            progress_bar.progress(60)

            # Paso 5.1: Evaluación
            status_text.markdown('<p class="progress-text">🔍 Paso 4/7: Evaluando calidad de transcripción...</p>', unsafe_allow_html=True)
            progress_bar.progress(65)

            fidelity_result = components['evaluator'].quick_evaluate(transcription)
            fidelity_score = fidelity_result['overall_score']

            processing.fidelity_score = fidelity_score
            db.commit()

            progress_bar.progress(70)

            # Preparar para generar artefactos
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            artifacts_generated = []

            # Paso 7a: PDF
            if generate_pdf:
                status_text.markdown('<p class="progress-text">📄 Paso 5/7: Generando guía de estudio en PDF...</p>', unsafe_allow_html=True)
                progress_bar.progress(75)

                pdf_path = components['pdf_generator'].generate_study_guide(
                    summary=summary,
                    transcription=transcription,
                    output_path=f"output/study_guide_{timestamp}.pdf",
                    title=title
                )

                # Subir a Azure si está habilitado
                pdf_url = components['storage_manager'].upload_file(pdf_path, folder="pdfs")

                artifact = GeneratedArtifact(
                    processing_id=processing.id,
                    artifact_type="pdf",
                    local_path=pdf_path,
                    blob_url=pdf_url
                )
                db.add(artifact)
                artifacts_generated.append(("PDF", pdf_path, "📄"))

            # Paso 7b: Mapa
            if generate_map:
                status_text.markdown('<p class="progress-text">🗺️ Paso 6/7: Creando mapa conceptual...</p>', unsafe_allow_html=True)
                progress_bar.progress(85)

                map_path = components['map_generator'].generate_concept_map(
                    summary=summary,
                    output_path=f"output/concept_map_{timestamp}.png",
                    title=title
                )

                map_url = components['storage_manager'].upload_file(map_path, folder="maps")

                artifact = GeneratedArtifact(
                    processing_id=processing.id,
                    artifact_type="map",
                    local_path=map_path,
                    blob_url=map_url
                )
                db.add(artifact)
                artifacts_generated.append(("Mapa Conceptual", map_path, "🗺️"))

            # Paso 7c: Podcast
            if generate_podcast:
                status_text.markdown('<p class="progress-text">🎙️ Paso 7/7: Generando podcast educativo...</p>', unsafe_allow_html=True)
                progress_bar.progress(90)

                podcast_path = components['podcast_generator'].generate_podcast(
                    summary=summary,
                    output_path=f"output/podcast_{timestamp}.mp3"
                )

                podcast_url = components['storage_manager'].upload_file(podcast_path, folder="podcasts")

                artifact = GeneratedArtifact(
                    processing_id=processing.id,
                    artifact_type="podcast",
                    local_path=podcast_path,
                    blob_url=podcast_url
                )
                db.add(artifact)
                artifacts_generated.append(("Podcast", podcast_path, "🎙️"))

            # Finalizar
            processing.status = "completed"
            db.commit()

            progress_bar.progress(100)
            status_text.markdown('<p class="progress-text">✅ ¡Procesamiento completado exitosamente!</p>', unsafe_allow_html=True)

            time.sleep(1)

            # Mostrar resultados
            st.markdown("---")
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown("## 🎉 ¡Procesamiento Completado!")
            st.markdown(f"**Calidad de Transcripción:** {fidelity_score:.1f}%")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("### 📦 Artefactos Generados")

            for name, path, icon in artifacts_generated:
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"""
                    <div class="artifact-card">
                        <h4>{icon} {name}</h4>
                        <p><code>{Path(path).name}</code></p>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    with open(path, "rb") as file:
                        st.download_button(
                            label="⬇️ Descargar",
                            data=file,
                            file_name=Path(path).name,
                            mime="application/octet-stream",
                            key=f"download_{name}"
                        )

                # Preview para imágenes
                if name == "Mapa Conceptual":
                    with st.expander("👁️ Ver preview del mapa"):
                        st.image(path, use_container_width=True)

            # Información adicional
            st.markdown("---")
            st.info(f"💾 **ID de Procesamiento:** {processing.id} | Todos los archivos están guardados en la carpeta `output/`")

            # Botón para procesar otro
            if st.button("🔄 Procesar otro video"):
                st.rerun()

        except Exception as e:
            st.error(f"❌ Error durante el procesamiento: {str(e)}")
            import traceback
            with st.expander("🐛 Ver detalles del error"):
                st.code(traceback.format_exc())

def show_history_page():
    """Página de historial de procesamiento."""

    st.markdown("## 📊 Historial de Procesamiento")

    db = next(get_db())
    processings = db.query(VideoProcessing).order_by(VideoProcessing.created_at.desc()).all()

    if not processings:
        st.info("📭 No hay videos procesados aún. ¡Procesa tu primer video!")
        return

    st.markdown(f"**Total de videos procesados:** {len(processings)}")
    st.markdown("---")

    for proc in processings:
        with st.expander(f"🎬 Video ID: {proc.id} - {proc.status} ({proc.created_at.strftime('%Y-%m-%d %H:%M')})"):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Información General**")
                st.write(f"URL: {proc.video_url or 'Archivo local'}")
                st.write(f"Estado: {proc.status}")
                if proc.fidelity_score:
                    st.write(f"Fidelidad: {proc.fidelity_score:.1f}%")

            with col2:
                st.markdown("**Archivos Generados**")
                if proc.transcription_path and os.path.exists(proc.transcription_path):
                    st.write("✅ Transcripción")
                if proc.summary_path and os.path.exists(proc.summary_path):
                    st.write("✅ Resumen")

            # Artefactos
            artifacts = db.query(GeneratedArtifact).filter_by(processing_id=proc.id).all()

            if artifacts:
                st.markdown("**Artefactos Generados**")
                cols = st.columns(len(artifacts))

                for idx, artifact in enumerate(artifacts):
                    with cols[idx]:
                        icon = {"pdf": "📄", "map": "🗺️", "podcast": "🎙️"}.get(artifact.artifact_type, "📦")
                        st.write(f"{icon} {artifact.artifact_type.upper()}")

                        if artifact.local_path and os.path.exists(artifact.local_path):
                            with open(artifact.local_path, "rb") as file:
                                st.download_button(
                                    label="Descargar",
                                    data=file,
                                    file_name=Path(artifact.local_path).name,
                                    key=f"hist_download_{artifact.id}"
                                )

def show_about_page():
    """Página de información sobre el proyecto."""

    st.markdown("## ℹ️ Acerca de TecguIA")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ### 🎯 Misión

        Reducir la deserción estudiantil en educación superior mediante la democratización
        del acceso a materiales de estudio de calidad, generados automáticamente con
        inteligencia artificial.

        ### 💡 ¿Cómo Funciona?

        TecguIA utiliza modelos avanzados de IA (Gemini) para:

        1. **Transcribir** automáticamente el audio de las clases
        2. **Analizar** el contenido y extraer conceptos clave
        3. **Generar** múltiples formatos de materiales de estudio:
           - Guías en PDF con resúmenes estructurados
           - Mapas conceptuales visuales
           - Podcasts para estudio móvil

        ### 🚀 Tecnologías

        - **IA:** Google Gemini AI
        - **Backend:** Python, FastAPI
        - **Frontend:** Streamlit
        - **Procesamiento:** yt-dlp, moviepy, reportlab
        - **Almacenamiento:** Azure Blob Storage
        - **Base de Datos:** SQLite/PostgreSQL

        ### 📊 Impacto

        - ⏱️ Reduce tiempo de preparación de materiales en **90%**
        - 📚 Genera **3 formatos diferentes** automáticamente
        - 🎓 Ayuda a estudiantes que no pueden asistir a clases
        - 👨‍🏫 Libera tiempo de docentes para tareas de mayor valor
        """)

    with col2:
        st.markdown("### 👥 Equipo")
        st.info("""
        Desarrollado para la hackathon:

        **"Educación Superior sin Deserción Estudiantil"**

        Powered by Claude + Gemini AI
        """)

        st.markdown("### 🔗 Enlaces")
        st.markdown("""
        - 📖 [Documentación Completa](README.md)
        - 🚀 [Guía Rápida](QUICKSTART.md)
        - 💻 [Código Fuente](.)
        """)

        st.markdown("### 📈 Estadísticas del Sistema")
        db = next(get_db())
        total = db.query(VideoProcessing).count()
        completed = db.query(VideoProcessing).filter_by(status="completed").count()
        artifacts = db.query(GeneratedArtifact).count()

        st.metric("Videos Procesados", total)
        st.metric("Exitosos", completed)
        st.metric("Artefactos Generados", artifacts)

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>TecguIA © 2024 | Transformando la educación con IA</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
