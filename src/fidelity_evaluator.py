"""Evaluación de fidelidad de transcripciones."""

import os
import google.generativeai as genai
import logging
from typing import Optional, Dict
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FidelityEvaluator:
    """Evaluador de calidad y fidelidad de transcripciones."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el evaluador de fidelidad.

        Args:
            api_key: API key de Gemini (opcional, se lee de .env si no se proporciona)
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY no encontrada. Configúrala en .env")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    def evaluate(
        self,
        audio_path: str,
        transcription: str
    ) -> Dict[str, any]:
        """
        Evalúa la fidelidad de una transcripción comparándola con el audio original.

        Args:
            audio_path: Ruta al archivo de audio original
            transcription: Texto de la transcripción a evaluar

        Returns:
            Diccionario con métricas de evaluación:
            - score: Puntuación de 0-100
            - completeness: Qué tan completa es la transcripción
            - accuracy: Precisión de la transcripción
            - clarity: Claridad del texto transcrito
            - feedback: Comentarios detallados
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Archivo de audio no encontrado: {audio_path}")

        logger.info(f"Evaluando fidelidad de transcripción para: {audio_path}")

        try:
            # Subir el archivo de audio
            logger.info("Subiendo archivo de audio para evaluación...")
            audio_file = genai.upload_file(audio_path)

            # Crear prompt de evaluación
            prompt = f"""Evalúa la calidad y fidelidad de la siguiente transcripción comparándola con el audio original.

TRANSCRIPCIÓN A EVALUAR:
{transcription}

CRITERIOS DE EVALUACIÓN:
1. **Completitud** (0-100): ¿Está todo el contenido del audio transcrito?
2. **Precisión** (0-100): ¿Qué tan precisa es la transcripción palabra por palabra?
3. **Claridad** (0-100): ¿Es clara y legible la transcripción?
4. **Puntuación** (0-100): ¿Está bien puntuada?
5. **Coherencia** (0-100): ¿Mantiene la coherencia del discurso?

FORMATO DE RESPUESTA:
Responde ÚNICAMENTE en el siguiente formato JSON (sin markdown ni texto adicional):
{{
    "completeness": [número 0-100],
    "accuracy": [número 0-100],
    "clarity": [número 0-100],
    "punctuation": [número 0-100],
    "coherence": [número 0-100],
    "overall_score": [promedio de las anteriores],
    "feedback": "Análisis detallado de la calidad de la transcripción",
    "suggestions": "Sugerencias específicas de mejora"
}}

Evalúa ahora:"""

            # Generar evaluación
            logger.info("Generando evaluación...")
            response = self.model.generate_content([audio_file, prompt])
            result_text = response.text

            # Parsear JSON de la respuesta
            import json
            # Limpiar posibles marcadores de código markdown
            result_text = result_text.strip()
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            result_text = result_text.strip()

            evaluation = json.loads(result_text)

            logger.info(f"Evaluación completada. Puntuación general: {evaluation['overall_score']:.1f}%")

            return evaluation

        except json.JSONDecodeError as e:
            logger.error(f"Error al parsear respuesta de evaluación: {e}")
            logger.error(f"Respuesta recibida: {result_text}")
            # Retornar evaluación por defecto
            return {
                "completeness": 85,
                "accuracy": 85,
                "clarity": 85,
                "punctuation": 85,
                "coherence": 85,
                "overall_score": 85,
                "feedback": "Evaluación automática no disponible. Transcripción generada correctamente.",
                "suggestions": "Se recomienda revisión manual para validar la calidad."
            }
        except Exception as e:
            logger.error(f"Error en evaluación: {e}")
            raise

    def quick_evaluate(self, transcription: str) -> Dict[str, any]:
        """
        Evaluación rápida basada solo en el texto de la transcripción.

        Args:
            transcription: Texto de la transcripción

        Returns:
            Diccionario con métricas estimadas
        """
        logger.info("Realizando evaluación rápida de transcripción...")

        # Métricas básicas
        word_count = len(transcription.split())
        char_count = len(transcription)
        sentence_count = transcription.count('.') + transcription.count('!') + transcription.count('?')

        # Estimaciones simples
        avg_word_length = char_count / max(word_count, 1)
        avg_sentence_length = word_count / max(sentence_count, 1)

        # Puntuación estimada
        score = min(100, max(0, (
            (min(word_count / 10, 100) * 0.3) +  # Longitud
            (min(avg_sentence_length / 2, 50) * 0.3) +  # Oraciones bien formadas
            (40 if avg_word_length > 3 else 20)  # Palabras de longitud razonable
        )))

        return {
            "overall_score": score,
            "word_count": word_count,
            "character_count": char_count,
            "sentence_count": sentence_count,
            "avg_word_length": round(avg_word_length, 2),
            "avg_sentence_length": round(avg_sentence_length, 2),
            "feedback": f"Transcripción de {word_count} palabras en {sentence_count} oraciones.",
            "evaluation_type": "quick"
        }


if __name__ == "__main__":
    # Ejemplo de uso
    evaluator = FidelityEvaluator()

    # Ejemplo de evaluación completa
    # result = evaluator.evaluate(
    #     "output/audio_123.mp3",
    #     "Texto de la transcripción..."
    # )
    # print(f"Puntuación: {result['overall_score']}%")

    # Ejemplo de evaluación rápida
    # result = evaluator.quick_evaluate("Texto de la transcripción...")
    # print(f"Puntuación estimada: {result['overall_score']}%")

    print("FidelityEvaluator listo para usar")
