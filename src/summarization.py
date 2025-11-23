"""Generación de resúmenes de transcripciones usando IA."""

import os
import google.generativeai as genai
from pathlib import Path
import logging
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TranscriptionSummarizer:
    """Generador de resúmenes de transcripciones educativas."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el generador de resúmenes.

        Args:
            api_key: API key de Gemini (opcional, se lee de .env si no se proporciona)
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY no encontrada. Configúrala en .env")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    def summarize(self, transcription: str, output_path: Optional[str] = None) -> str:
        """
        Resume una transcripción de clase o video educativo.

        Args:
            transcription: Texto de la transcripción
            output_path: Ruta donde guardar el resumen (opcional)

        Returns:
            Resumen generado
        """
        logger.info("Generando resumen de la transcripción...")

        prompt = f"""Eres un asistente educativo experto. Tu tarea es crear un resumen completo y estructurado de la siguiente clase o video educativo.

TRANSCRIPCIÓN:
{transcription}

INSTRUCCIONES:
Crea un resumen exhaustivo que incluya:

1. **Tema Principal**: Identifica el tema central de la clase
2. **Objetivos de Aprendizaje**: ¿Qué se espera que el estudiante aprenda?
3. **Conceptos Clave**: Lista los conceptos principales explicados
4. **Desarrollo del Contenido**: Resume el contenido organizado en secciones lógicas
5. **Ejemplos y Casos**: Menciona los ejemplos prácticos utilizados
6. **Conclusiones**: Puntos principales de cierre
7. **Términos Importantes**: Glosario de términos técnicos mencionados

FORMATO:
- Usa markdown para la estructura
- Sé claro y conciso pero completo
- Mantén la precisión académica
- Organiza la información de forma jerárquica
- Incluye todos los puntos importantes sin omitir detalles clave

Genera el resumen ahora:"""

        try:
            response = self.model.generate_content(prompt)
            summary = response.text

            logger.info(f"Resumen generado ({len(summary)} caracteres)")

            # Guardar si se proporciona ruta
            if output_path:
                output_file = Path(output_path)
                output_file.parent.mkdir(parents=True, exist_ok=True)
                output_file.write_text(summary, encoding='utf-8')
                logger.info(f"Resumen guardado en: {output_path}")

            return summary

        except Exception as e:
            logger.error(f"Error al generar resumen: {e}")
            raise

    def summarize_from_file(self, transcription_path: str, output_path: Optional[str] = None) -> str:
        """
        Resume una transcripción desde un archivo.

        Args:
            transcription_path: Ruta al archivo de transcripción
            output_path: Ruta donde guardar el resumen

        Returns:
            Resumen generado
        """
        if not os.path.exists(transcription_path):
            raise FileNotFoundError(f"Archivo de transcripción no encontrado: {transcription_path}")

        logger.info(f"Leyendo transcripción desde: {transcription_path}")
        transcription = Path(transcription_path).read_text(encoding='utf-8')

        if output_path is None:
            # Generar nombre de archivo de salida basado en la entrada
            output_path = str(Path(transcription_path).with_name(
                f"summary_{Path(transcription_path).stem}.txt"
            ))

        return self.summarize(transcription, output_path)


if __name__ == "__main__":
    # Ejemplo de uso
    summarizer = TranscriptionSummarizer()

    # Ejemplo
    # summary = summarizer.summarize_from_file(
    #     "output/transcription_123.txt",
    #     "output/summary_123.txt"
    # )
    # print(summary)

    print("TranscriptionSummarizer listo para usar")
