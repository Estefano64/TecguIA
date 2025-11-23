#!/usr/bin/env python3
"""Interfaz de línea de comandos para TecguIA."""

import argparse
import sys
import logging
from pathlib import Path
from datetime import datetime

from src.video_processor import VideoProcessor
from src.transcription import AudioTranscriber
from src.summarization import TranscriptionSummarizer
from src.fidelity_evaluator import FidelityEvaluator
from src.generators import PDFGenerator, ConceptMapGenerator, PodcastGenerator
from src.storage import AzureStorageManager
from src.database import init_db, get_db, VideoProcessing, GeneratedArtifact

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def process_video_cli(args):
    """Procesa un video desde CLI."""
    logger.info("=" * 80)
    logger.info("TecguIA - Procesamiento de Video Educativo")
    logger.info("=" * 80)

    try:
        # Inicializar componentes
        logger.info("\n[1/8] Inicializando componentes...")
        video_processor = VideoProcessor()
        transcriber = AudioTranscriber()
        summarizer = TranscriptionSummarizer()
        evaluator = FidelityEvaluator()
        pdf_generator = PDFGenerator()
        map_generator = ConceptMapGenerator()
        podcast_generator = PodcastGenerator()
        storage_manager = AzureStorageManager()

        # Inicializar BD
        init_db()
        db = next(get_db())

        # Paso 1-2: Descarga y extracción de audio
        logger.info("\n[2/8] Descargando video y extrayendo audio...")
        if args.video_url:
            video_path, audio_path = video_processor.process_video(
                source=args.video_url,
                is_url=True
            )
        elif args.video_path:
            video_path, audio_path = video_processor.process_video(
                source=args.video_path,
                is_url=False
            )
        else:
            raise ValueError("Debe proporcionar --video-url o --video-path")

        logger.info(f"✓ Video: {video_path}")
        logger.info(f"✓ Audio: {audio_path}")

        # Crear registro en BD
        processing = VideoProcessing(
            video_url=args.video_url,
            video_path=video_path,
            audio_path=audio_path,
            status="audio_extracted"
        )
        db.add(processing)
        db.commit()
        db.refresh(processing)

        # Paso 3-4: Transcripción
        logger.info("\n[3/8] Transcribiendo audio...")
        transcription_path = f"output/transcription_{processing.id}.txt"
        transcription = transcriber.transcribe_audio(audio_path, transcription_path)

        processing.transcription_path = transcription_path
        processing.status = "transcribed"
        db.commit()

        logger.info(f"✓ Transcripción guardada: {transcription_path}")
        logger.info(f"  Longitud: {len(transcription)} caracteres")

        # Paso 5: Resumen
        logger.info("\n[4/8] Generando resumen...")
        summary_path = f"output/summary_{processing.id}.txt"
        summary = summarizer.summarize(transcription, summary_path)

        processing.summary_path = summary_path
        processing.status = "summarized"
        db.commit()

        logger.info(f"✓ Resumen guardado: {summary_path}")
        logger.info(f"  Longitud: {len(summary)} caracteres")

        # Paso 5.1: Evaluación de fidelidad
        logger.info("\n[5/8] Evaluando fidelidad de la transcripción...")
        try:
            if args.full_evaluation:
                fidelity_result = evaluator.evaluate(audio_path, transcription)
            else:
                fidelity_result = evaluator.quick_evaluate(transcription)

            fidelity_score = fidelity_result['overall_score']
            processing.fidelity_score = fidelity_score
            processing.status = "evaluated"
            db.commit()

            logger.info(f"✓ Puntuación de fidelidad: {fidelity_score:.1f}%")

        except Exception as e:
            logger.warning(f"No se pudo evaluar fidelidad: {e}")
            fidelity_score = None

        # Paso 6-7: Generar artefactos
        logger.info("\n[6/8] Generando artefactos solicitados...")

        artifacts = args.artifacts.split(',') if args.artifacts else []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        title = args.title or f"Material Educativo {processing.id}"

        generated_artifacts = []

        # 7a: PDF
        if "pdf" in artifacts:
            logger.info("\n[7a/8] Generando guía de estudio en PDF...")
            pdf_path = pdf_generator.generate_study_guide(
                summary=summary,
                transcription=transcription,
                output_path=f"output/study_guide_{timestamp}.pdf",
                title=title
            )
            logger.info(f"✓ PDF generado: {pdf_path}")

            # Subir a Azure si está habilitado
            if storage_manager.enabled:
                pdf_url = storage_manager.upload_file(pdf_path, folder="pdfs")
                logger.info(f"✓ PDF subido a Azure: {pdf_url}")
            else:
                pdf_url = None

            # Registrar en BD
            artifact = GeneratedArtifact(
                processing_id=processing.id,
                artifact_type="pdf",
                local_path=pdf_path,
                blob_url=pdf_url
            )
            db.add(artifact)
            generated_artifacts.append(("PDF", pdf_path, pdf_url))

        # 7b: Mapa Conceptual
        if "map" in artifacts:
            logger.info("\n[7b/8] Generando mapa conceptual...")
            map_path = map_generator.generate_concept_map(
                summary=summary,
                output_path=f"output/concept_map_{timestamp}.png",
                title=title
            )
            logger.info(f"✓ Mapa generado: {map_path}")

            # Subir a Azure si está habilitado
            if storage_manager.enabled:
                map_url = storage_manager.upload_file(map_path, folder="maps")
                logger.info(f"✓ Mapa subido a Azure: {map_url}")
            else:
                map_url = None

            # Registrar en BD
            artifact = GeneratedArtifact(
                processing_id=processing.id,
                artifact_type="map",
                local_path=map_path,
                blob_url=map_url
            )
            db.add(artifact)
            generated_artifacts.append(("Mapa Conceptual", map_path, map_url))

        # 7c: Podcast
        if "podcast" in artifacts:
            logger.info("\n[7c/8] Generando podcast...")
            podcast_path = podcast_generator.generate_podcast(
                summary=summary,
                output_path=f"output/podcast_{timestamp}.mp3"
            )
            logger.info(f"✓ Podcast generado: {podcast_path}")

            # Subir a Azure si está habilitado
            if storage_manager.enabled:
                podcast_url = storage_manager.upload_file(podcast_path, folder="podcasts")
                logger.info(f"✓ Podcast subido a Azure: {podcast_url}")
            else:
                podcast_url = None

            # Registrar en BD
            artifact = GeneratedArtifact(
                processing_id=processing.id,
                artifact_type="podcast",
                local_path=podcast_path,
                blob_url=podcast_url
            )
            db.add(artifact)
            generated_artifacts.append(("Podcast", podcast_path, podcast_url))

        # Finalizar
        processing.status = "completed"
        db.commit()

        # Resumen final
        logger.info("\n" + "=" * 80)
        logger.info("PROCESAMIENTO COMPLETADO EXITOSAMENTE")
        logger.info("=" * 80)
        logger.info(f"\nID de procesamiento: {processing.id}")
        logger.info(f"Video: {video_path}")
        logger.info(f"Audio: {audio_path}")
        logger.info(f"Transcripción: {transcription_path}")
        logger.info(f"Resumen: {summary_path}")

        if fidelity_score:
            logger.info(f"Fidelidad: {fidelity_score:.1f}%")

        if generated_artifacts:
            logger.info("\nArtefactos generados:")
            for name, local_path, url in generated_artifacts:
                logger.info(f"\n  {name}:")
                logger.info(f"    Local: {local_path}")
                if url:
                    logger.info(f"    Azure: {url}")

        logger.info("\n" + "=" * 80)

        return 0

    except Exception as e:
        logger.error(f"\n❌ ERROR: {e}", exc_info=True)
        return 1


def main():
    """Función principal del CLI."""
    parser = argparse.ArgumentParser(
        description="TecguIA - Sistema de Procesamiento de Videos Educativos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Procesar video de YouTube y generar todos los artefactos
  python cli.py --video-url "https://youtube.com/watch?v=..." --artifacts pdf,map,podcast

  # Procesar video local y generar solo PDF
  python cli.py --video-path "/path/to/video.mp4" --artifacts pdf --title "Mi Clase"

  # Procesar con evaluación completa de fidelidad
  python cli.py --video-url "..." --artifacts pdf,map --full-evaluation
        """
    )

    parser.add_argument(
        '--video-url',
        help='URL del video a procesar (YouTube, Vimeo, etc.)'
    )

    parser.add_argument(
        '--video-path',
        help='Ruta a un archivo de video local'
    )

    parser.add_argument(
        '--artifacts',
        default='pdf,map,podcast',
        help='Artefactos a generar (pdf,map,podcast). Default: todos'
    )

    parser.add_argument(
        '--title',
        help='Título para los materiales generados'
    )

    parser.add_argument(
        '--full-evaluation',
        action='store_true',
        help='Realizar evaluación completa de fidelidad (más lento pero más preciso)'
    )

    args = parser.parse_args()

    # Validar argumentos
    if not args.video_url and not args.video_path:
        parser.error("Debe proporcionar --video-url o --video-path")

    # Ejecutar procesamiento
    return process_video_cli(args)


if __name__ == "__main__":
    sys.exit(main())
