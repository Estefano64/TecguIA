"""Generador de podcasts educativos."""

import os
import google.generativeai as genai
from pathlib import Path
import logging
from typing import Optional
from datetime import datetime
from dotenv import load_dotenv
import subprocess

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PodcastGenerator:
    """Generador de podcasts educativos a partir de resúmenes."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el generador de podcasts.

        Args:
            api_key: API key de Gemini para generar guión
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY no encontrada. Configúrala en .env")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    def generate_podcast(
        self,
        summary: str,
        output_path: Optional[str] = None,
        voice: str = "es-ES-Standard-A"
    ) -> str:
        """
        Genera un podcast educativo a partir de un resumen.

        Args:
            summary: Resumen del contenido educativo
            output_path: Ruta del archivo de audio de salida (.mp3)
            voice: Voz a utilizar

        Returns:
            Ruta al archivo de audio generado
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"output/podcast_{timestamp}.mp3"

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        logger.info("Generando guión del podcast...")

        # Generar guión del podcast
        script = self._generate_podcast_script(summary)

        # Guardar guión
        script_path = output_file.with_suffix('.txt')
        script_path.write_text(script, encoding='utf-8')
        logger.info(f"Guión guardado en: {script_path}")

        # Generar audio
        logger.info("Generando audio del podcast...")
        self._generate_audio(script, output_path, voice)

        logger.info(f"Podcast generado: {output_path}")
        return str(output_path)

    def _generate_podcast_script(self, summary: str) -> str:
        """
        Genera el guión del podcast usando IA.

        Args:
            summary: Resumen del contenido

        Returns:
            Guión del podcast
        """
        prompt = f"""Eres un creador de contenido educativo. Crea un guión para un podcast de estudio basado en el siguiente resumen.

RESUMEN:
{summary}

INSTRUCCIONES:
- Crea un guión conversacional y amigable
- Duración objetivo: 5-8 minutos de lectura
- Incluye:
  * Introducción atractiva
  * Explicación clara de conceptos clave
  * Ejemplos y analogías cuando sea apropiado
  * Resumen y puntos de acción al final
- Usa un tono cercano pero profesional
- El guión debe ser natural para ser leído en voz alta
- No incluyas indicaciones escénicas, solo el texto a narrar

Genera el guión del podcast:"""

        try:
            response = self.model.generate_content(prompt)
            script = response.text
            return script

        except Exception as e:
            logger.error(f"Error al generar guión: {e}")
            # Retornar guión básico
            return f"""Bienvenidos a este podcast educativo.

Hoy vamos a repasar el contenido de nuestra clase más reciente.

{summary}

Recuerda repasar estos conceptos y practicar los ejercicios sugeridos.

¡Hasta la próxima!"""

    def _generate_audio(self, script: str, output_path: str, voice: str):
        """
        Genera el audio del podcast usando TTS.

        Args:
            script: Guión del podcast
            output_path: Ruta de salida
            voice: Voz a utilizar
        """
        try:
            # Opción 1: Usar Google Text-to-Speech (si está disponible)
            self._generate_audio_google_tts(script, output_path, voice)

        except Exception as e:
            logger.warning(f"No se pudo generar audio con Google TTS: {e}")
            try:
                # Opción 2: Usar pyttsx3 (offline)
                self._generate_audio_pyttsx3(script, output_path)
            except Exception as e2:
                logger.error(f"Error al generar audio: {e2}")
                # Crear archivo placeholder
                logger.warning("Creando archivo de audio placeholder")
                Path(output_path).touch()

    def _generate_audio_google_tts(self, script: str, output_path: str, voice: str):
        """Genera audio usando Google Text-to-Speech."""
        try:
            from google.cloud import texttospeech

            client = texttospeech.TextToSpeechClient()

            synthesis_input = texttospeech.SynthesisInput(text=script)

            voice_params = texttospeech.VoiceSelectionParams(
                language_code="es-ES",
                name=voice
            )

            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=1.0,
                pitch=0.0
            )

            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice_params,
                audio_config=audio_config
            )

            Path(output_path).write_bytes(response.audio_content)
            logger.info("Audio generado con Google TTS")

        except ImportError:
            raise Exception("google-cloud-texttospeech no está instalado")
        except Exception as e:
            raise Exception(f"Error en Google TTS: {e}")

    def _generate_audio_pyttsx3(self, script: str, output_path: str):
        """Genera audio usando pyttsx3 (TTS offline)."""
        try:
            import pyttsx3

            engine = pyttsx3.init()

            # Configurar voz en español si está disponible
            voices = engine.getProperty('voices')
            for voice in voices:
                if 'spanish' in voice.name.lower() or 'español' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break

            # Configurar propiedades
            engine.setProperty('rate', 150)  # Velocidad
            engine.setProperty('volume', 0.9)  # Volumen

            # Guardar a archivo
            temp_wav = output_path.replace('.mp3', '_temp.wav')
            engine.save_to_file(script, temp_wav)
            engine.runAndWait()

            # Convertir WAV a MP3 usando ffmpeg
            if Path(temp_wav).exists():
                subprocess.run([
                    'ffmpeg', '-i', temp_wav,
                    '-codec:a', 'libmp3lame',
                    '-qscale:a', '2',
                    output_path,
                    '-y'
                ], check=True, capture_output=True)

                # Eliminar WAV temporal
                Path(temp_wav).unlink()

            logger.info("Audio generado con pyttsx3")

        except ImportError:
            raise Exception("pyttsx3 no está instalado")
        except Exception as e:
            raise Exception(f"Error en pyttsx3: {e}")


if __name__ == "__main__":
    # Ejemplo de uso
    generator = PodcastGenerator()

    # Ejemplo
    # podcast_path = generator.generate_podcast(
    #     summary="Resumen de la clase...",
    # )
    # print(f"Podcast generado: {podcast_path}")

    print("PodcastGenerator listo para usar")
