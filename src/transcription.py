"""Transcripción de audio usando Gemini AI."""

import os
import google.generativeai as genai
from pathlib import Path
import logging
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AudioTranscriber:
    """Transcriptor de audio usando Gemini AI."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el transcriptor.

        Args:
            api_key: API key de Gemini (opcional, se lee de .env si no se proporciona)
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY no encontrada. Configúrala en .env")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    def transcribe_audio(self, audio_path: str, output_path: Optional[str] = None) -> str:
        """
        Transcribe un archivo de audio a texto.

        Args:
            audio_path: Ruta al archivo de audio
            output_path: Ruta donde guardar la transcripción (opcional)

        Returns:
            Texto transcrito
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Archivo de audio no encontrado: {audio_path}")

        logger.info(f"Transcribiendo audio: {audio_path}")

        try:
            # Subir el archivo de audio
            logger.info("Subiendo archivo de audio a Gemini...")
            audio_file = genai.upload_file(audio_path)

            # Crear prompt para transcripción
            prompt = """Por favor, transcribe el audio completo de esta clase o video educativo.

Instrucciones:
- Transcribe todo el contenido de forma precisa y completa
- Mantén la puntuación adecuada
- Indica cuando hay cambios de tema o secciones importantes
- Si hay múltiples hablantes, intenta identificarlos (Profesor, Estudiante, etc.)
- Incluye términos técnicos y académicos exactamente como se pronuncian
- No omitas ningún contenido importante

Formato de salida:
Transcripción completa en texto plano, organizada en párrafos según el flujo natural del contenido."""

            # Generar transcripción
            logger.info("Generando transcripción...")
            response = self.model.generate_content([audio_file, prompt])
            transcription = response.text

            logger.info(f"Transcripción completada ({len(transcription)} caracteres)")

            # Guardar si se proporciona ruta
            if output_path:
                output_file = Path(output_path)
                output_file.parent.mkdir(parents=True, exist_ok=True)
                output_file.write_text(transcription, encoding='utf-8')
                logger.info(f"Transcripción guardada en: {output_path}")

            return transcription

        except Exception as e:
            logger.error(f"Error en transcripción: {e}")
            raise

    def transcribe_audio_chunked(
        self,
        audio_path: str,
        chunk_duration: int = 600,
        output_path: Optional[str] = None
    ) -> str:
        """
        Transcribe audio largo dividiéndolo en chunks (para archivos muy grandes).

        Args:
            audio_path: Ruta al archivo de audio
            chunk_duration: Duración de cada chunk en segundos (default: 10 min)
            output_path: Ruta donde guardar la transcripción

        Returns:
            Texto transcrito completo
        """
        # Por ahora, Gemini puede manejar archivos grandes
        # Esta función está preparada para futuras implementaciones
        logger.info("Usando transcripción directa (Gemini maneja archivos grandes)")
        return self.transcribe_audio(audio_path, output_path)


if __name__ == "__main__":
    # Ejemplo de uso
    transcriber = AudioTranscriber()

    # Ejemplo
    # transcription = transcriber.transcribe_audio(
    #     "output/audio_123.mp3",
    #     "output/transcription_123.txt"
    # )
    # print(f"Transcripción: {transcription[:200]}...")

    print("AudioTranscriber listo para usar")
