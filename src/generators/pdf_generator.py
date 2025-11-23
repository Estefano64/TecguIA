"""Generador de guías de estudio en PDF."""

import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from pathlib import Path
import logging
from typing import Optional
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFGenerator:
    """Generador de guías de estudio en PDF."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el generador de PDFs.

        Args:
            api_key: API key de Gemini para generar contenido estructurado
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        else:
            self.model = None
            logger.warning("No se configuró API key de Gemini. Funcionalidad limitada.")

    def generate_study_guide(
        self,
        summary: str,
        transcription: Optional[str] = None,
        output_path: Optional[str] = None,
        title: str = "Guía de Estudio"
    ) -> str:
        """
        Genera una guía de estudio en PDF.

        Args:
            summary: Resumen de la clase
            transcription: Transcripción completa (opcional)
            output_path: Ruta del archivo PDF de salida
            title: Título de la guía

        Returns:
            Ruta al archivo PDF generado
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"output/study_guide_{timestamp}.pdf"

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Generando guía de estudio en PDF: {output_path}")

        # Obtener contenido estructurado
        if self.model and transcription:
            structured_content = self._generate_structured_content(summary, transcription)
        else:
            structured_content = self._parse_summary(summary)

        # Crear PDF
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )

        # Estilos
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#283593'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        styles.add(ParagraphStyle(
            name='CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
        ))

        # Construir contenido del PDF
        story = []

        # Título
        story.append(Paragraph(title, styles['CustomTitle']))
        story.append(Spacer(1, 0.2 * inch))

        # Fecha
        fecha = datetime.now().strftime("%d de %B de %Y")
        story.append(Paragraph(f"<i>Generado el {fecha}</i>", styles['Normal']))
        story.append(Spacer(1, 0.3 * inch))

        # Contenido estructurado
        for section in structured_content:
            # Título de sección
            story.append(Paragraph(section['title'], styles['CustomHeading']))

            # Contenido de sección
            for item in section['content']:
                if isinstance(item, str):
                    # Texto normal
                    story.append(Paragraph(item, styles['CustomBody']))
                elif isinstance(item, list):
                    # Lista de puntos
                    for point in item:
                        bullet = f"• {point}"
                        story.append(Paragraph(bullet, styles['CustomBody']))
                    story.append(Spacer(1, 0.1 * inch))

            story.append(Spacer(1, 0.2 * inch))

        # Construir PDF
        doc.build(story)

        logger.info(f"PDF generado exitosamente: {output_path}")
        return str(output_path)

    def _generate_structured_content(self, summary: str, transcription: str) -> list:
        """
        Genera contenido estructurado para el PDF usando IA.

        Args:
            summary: Resumen de la clase
            transcription: Transcripción completa

        Returns:
            Lista de secciones estructuradas
        """
        logger.info("Generando contenido estructurado con IA...")

        prompt = f"""Crea una guía de estudio estructurada basada en la siguiente clase.

RESUMEN:
{summary[:3000]}

TRANSCRIPCIÓN:
{transcription[:5000] if len(transcription) > 5000 else transcription}

Genera una guía de estudio completa en el siguiente formato JSON:
[
    {{
        "title": "Resumen Ejecutivo",
        "content": ["Descripción breve del tema principal"]
    }},
    {{
        "title": "Objetivos de Aprendizaje",
        "content": ["Objetivo 1", "Objetivo 2", ...]
    }},
    {{
        "title": "Conceptos Clave",
        "content": ["Concepto 1: Definición", "Concepto 2: Definición", ...]
    }},
    {{
        "title": "Desarrollo del Tema",
        "content": ["Párrafo explicativo del contenido principal..."]
    }},
    {{
        "title": "Puntos Importantes",
        "content": ["Punto 1", "Punto 2", ...]
    }},
    {{
        "title": "Ejercicios y Preguntas de Repaso",
        "content": ["Pregunta 1", "Pregunta 2", ...]
    }},
    {{
        "title": "Glosario",
        "content": ["Término 1: Definición", "Término 2: Definición", ...]
    }}
]

Responde SOLO con el JSON, sin texto adicional."""

        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()

            # Limpiar markdown si existe
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            result_text = result_text.strip()

            import json
            structured = json.loads(result_text)
            return structured

        except Exception as e:
            logger.warning(f"Error al generar contenido estructurado: {e}")
            logger.warning("Usando formato básico")
            return self._parse_summary(summary)

    def _parse_summary(self, summary: str) -> list:
        """
        Parsea un resumen de texto simple a estructura básica.

        Args:
            summary: Texto del resumen

        Returns:
            Lista de secciones estructuradas
        """
        # Estructura básica
        sections = [
            {
                "title": "Resumen de la Clase",
                "content": [summary]
            }
        ]

        return sections


if __name__ == "__main__":
    # Ejemplo de uso
    generator = PDFGenerator()

    # Ejemplo
    # pdf_path = generator.generate_study_guide(
    #     summary="Resumen de la clase sobre ...",
    #     transcription="Transcripción completa...",
    #     title="Guía de Estudio - Introducción a Python"
    # )
    # print(f"PDF generado: {pdf_path}")

    print("PDFGenerator listo para usar")
