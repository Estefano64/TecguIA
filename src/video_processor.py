"""Procesamiento de video: descarga y extracción de audio."""

import os
import yt_dlp
from moviepy.editor import VideoFileClip
from pathlib import Path
from typing import Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoProcessor:
    """Procesador de videos para descarga y extracción de audio."""

    def __init__(self, output_dir: str = "./output", temp_dir: str = "./temp"):
        self.output_dir = Path(output_dir)
        self.temp_dir = Path(temp_dir)

        # Crear directorios si no existen
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def download_video(self, url: str, output_name: Optional[str] = None) -> str:
        """
        Descarga un video desde una URL (YouTube, Vimeo, etc.).

        Args:
            url: URL del video
            output_name: Nombre opcional para el archivo

        Returns:
            Ruta al archivo de video descargado
        """
        if output_name is None:
            output_name = f"video_{int(os.time())}"

        output_path = self.temp_dir / f"{output_name}.mp4"

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': str(output_path.with_suffix('')),
            'quiet': False,
            'no_warnings': False,
        }

        try:
            logger.info(f"Descargando video desde: {url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # yt-dlp puede agregar extensiones, buscar el archivo
            possible_paths = [
                output_path,
                output_path.with_suffix('.mp4'),
                output_path.with_suffix('.mkv'),
                output_path.with_suffix('.webm'),
            ]

            for path in possible_paths:
                if path.exists():
                    logger.info(f"Video descargado: {path}")
                    return str(path)

            raise FileNotFoundError(f"No se encontró el video descargado en {output_path}")

        except Exception as e:
            logger.error(f"Error al descargar video: {e}")
            raise

    def process_local_video(self, video_path: str) -> str:
        """
        Copia un video local al directorio temporal.

        Args:
            video_path: Ruta al video local

        Returns:
            Ruta al video en el directorio temporal
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"No se encontró el video en: {video_path}")

        # Copiar al directorio temporal
        import shutil
        dest_path = self.temp_dir / Path(video_path).name
        shutil.copy2(video_path, dest_path)
        logger.info(f"Video copiado a: {dest_path}")

        return str(dest_path)

    def extract_audio(self, video_path: str, output_name: Optional[str] = None) -> str:
        """
        Extrae el audio de un video.

        Args:
            video_path: Ruta al archivo de video
            output_name: Nombre opcional para el archivo de audio

        Returns:
            Ruta al archivo de audio extraído (.mp3)
        """
        if output_name is None:
            output_name = f"audio_{int(os.time())}"

        audio_path = self.output_dir / f"{output_name}.mp3"

        try:
            logger.info(f"Extrayendo audio de: {video_path}")
            video = VideoFileClip(video_path)
            video.audio.write_audiofile(
                str(audio_path),
                codec='mp3',
                bitrate='192k',
                logger=None  # Silenciar logs de moviepy
            )
            video.close()

            logger.info(f"Audio extraído: {audio_path}")
            return str(audio_path)

        except Exception as e:
            logger.error(f"Error al extraer audio: {e}")
            raise

    def process_video(
        self,
        source: str,
        is_url: bool = True,
        output_name: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        Procesa un video completo: descarga (si es URL) y extrae audio.

        Args:
            source: URL o ruta del video
            is_url: Si True, descarga desde URL; si False, procesa archivo local
            output_name: Nombre base para los archivos de salida

        Returns:
            Tupla (video_path, audio_path)
        """
        if output_name is None:
            import time
            output_name = f"content_{int(time.time())}"

        # Paso 1: Obtener el video
        if is_url:
            video_path = self.download_video(source, output_name)
        else:
            video_path = self.process_local_video(source)

        # Paso 2: Extraer audio
        audio_path = self.extract_audio(video_path, output_name)

        logger.info(f"Procesamiento completado:")
        logger.info(f"  Video: {video_path}")
        logger.info(f"  Audio: {audio_path}")

        return video_path, audio_path


if __name__ == "__main__":
    # Ejemplo de uso
    processor = VideoProcessor()

    # Ejemplo con URL de YouTube
    # video, audio = processor.process_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    # Ejemplo con archivo local
    # video, audio = processor.process_video("/path/to/video.mp4", is_url=False)

    print("VideoProcessor listo para usar")
