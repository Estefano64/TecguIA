"""Generador de mapas conceptuales."""

import os
import google.generativeai as genai
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import networkx as nx
from pathlib import Path
import logging
from typing import Optional, Dict, List
from datetime import datetime
from dotenv import load_dotenv
import json

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConceptMapGenerator:
    """Generador de mapas conceptuales visuales."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el generador de mapas conceptuales.

        Args:
            api_key: API key de Gemini para extraer conceptos
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY no encontrada. Configúrala en .env")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    def generate_concept_map(
        self,
        summary: str,
        output_path: Optional[str] = None,
        title: str = "Mapa Conceptual"
    ) -> str:
        """
        Genera un mapa conceptual visual a partir de un resumen.

        Args:
            summary: Resumen del contenido educativo
            output_path: Ruta del archivo de imagen de salida (.png)
            title: Título del mapa

        Returns:
            Ruta al archivo de imagen generado
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"output/concept_map_{timestamp}.png"

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        logger.info("Extrayendo conceptos y relaciones...")

        # Extraer conceptos y relaciones usando IA
        concepts_data = self._extract_concepts(summary)

        # Crear grafo
        logger.info("Creando mapa conceptual...")
        self._create_visual_map(concepts_data, output_path, title)

        logger.info(f"Mapa conceptual generado: {output_path}")
        return str(output_path)

    def _extract_concepts(self, summary: str) -> Dict:
        """
        Extrae conceptos y relaciones del resumen usando IA.

        Args:
            summary: Resumen del contenido

        Returns:
            Diccionario con conceptos y relaciones
        """
        prompt = f"""Analiza el siguiente contenido educativo y extrae los conceptos clave y sus relaciones.

CONTENIDO:
{summary}

Genera un mapa conceptual en formato JSON con la siguiente estructura:
{{
    "main_concept": "Concepto principal del tema",
    "concepts": [
        {{
            "id": "concepto1",
            "label": "Nombre del Concepto 1",
            "level": 1,
            "description": "Breve descripción"
        }},
        {{
            "id": "concepto2",
            "label": "Nombre del Concepto 2",
            "level": 2,
            "description": "Breve descripción"
        }}
    ],
    "relations": [
        {{
            "from": "concepto1",
            "to": "concepto2",
            "label": "tipo de relación"
        }}
    ]
}}

INSTRUCCIONES:
- Identifica entre 8-15 conceptos clave
- El "level" indica la jerarquía (1 = principal, 2 = secundario, 3 = detalle)
- Las relaciones deben describir cómo se conectan los conceptos
- Usa labels descriptivos y claros

Responde SOLO con el JSON, sin texto adicional:"""

        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()

            # Limpiar markdown
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            result_text = result_text.strip()

            concepts_data = json.loads(result_text)
            return concepts_data

        except Exception as e:
            logger.error(f"Error al extraer conceptos: {e}")
            # Retornar estructura básica
            return {
                "main_concept": "Tema Principal",
                "concepts": [
                    {"id": "c1", "label": "Concepto 1", "level": 1, "description": ""},
                    {"id": "c2", "label": "Concepto 2", "level": 2, "description": ""},
                    {"id": "c3", "label": "Concepto 3", "level": 2, "description": ""},
                ],
                "relations": [
                    {"from": "c1", "to": "c2", "label": "relacionado"},
                    {"from": "c1", "to": "c3", "label": "relacionado"},
                ]
            }

    def _create_visual_map(self, concepts_data: Dict, output_path: str, title: str):
        """
        Crea la visualización del mapa conceptual.

        Args:
            concepts_data: Datos de conceptos y relaciones
            output_path: Ruta de salida
            title: Título del mapa
        """
        # Crear grafo dirigido
        G = nx.DiGraph()

        # Agregar nodos
        for concept in concepts_data.get('concepts', []):
            G.add_node(
                concept['id'],
                label=concept['label'],
                level=concept.get('level', 2)
            )

        # Agregar aristas
        for relation in concepts_data.get('relations', []):
            G.add_edge(
                relation['from'],
                relation['to'],
                label=relation.get('label', '')
            )

        # Crear figura
        plt.figure(figsize=(16, 12))
        plt.title(title, fontsize=20, fontweight='bold', pad=20)

        # Layout jerárquico
        try:
            pos = nx.spring_layout(G, k=2, iterations=50)
        except:
            pos = nx.shell_layout(G)

        # Colores por nivel
        colors = {
            1: '#1a237e',  # Azul oscuro (principal)
            2: '#283593',  # Azul medio (secundario)
            3: '#3949ab',  # Azul claro (detalle)
        }

        # Dibujar nodos
        for node in G.nodes():
            level = G.nodes[node].get('level', 2)
            color = colors.get(level, '#3949ab')

            x, y = pos[node]

            # Caja del nodo
            bbox = FancyBboxPatch(
                (x - 0.15, y - 0.08),
                0.3, 0.16,
                boxstyle="round,pad=0.01",
                facecolor=color,
                edgecolor='white',
                linewidth=2,
                transform=plt.gca().transData
            )
            plt.gca().add_patch(bbox)

            # Texto del nodo
            label = G.nodes[node].get('label', node)
            plt.text(
                x, y,
                label,
                fontsize=10 if level == 1 else 9,
                color='white',
                ha='center',
                va='center',
                fontweight='bold' if level == 1 else 'normal',
                wrap=True
            )

        # Dibujar aristas
        for edge in G.edges():
            start_pos = pos[edge[0]]
            end_pos = pos[edge[1]]

            arrow = FancyArrowPatch(
                start_pos, end_pos,
                arrowstyle='->,head_width=0.4,head_length=0.8',
                color='gray',
                linewidth=1.5,
                alpha=0.6,
                connectionstyle="arc3,rad=0.1"
            )
            plt.gca().add_patch(arrow)

            # Etiqueta de la relación
            edge_label = G.edges[edge].get('label', '')
            if edge_label:
                mid_x = (start_pos[0] + end_pos[0]) / 2
                mid_y = (start_pos[1] + end_pos[1]) / 2
                plt.text(
                    mid_x, mid_y,
                    edge_label,
                    fontsize=7,
                    color='#424242',
                    ha='center',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='none')
                )

        # Configurar ejes
        plt.axis('off')
        plt.tight_layout()

        # Guardar
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()


if __name__ == "__main__":
    # Ejemplo de uso
    generator = ConceptMapGenerator()

    # Ejemplo
    # map_path = generator.generate_concept_map(
    #     summary="Resumen de la clase...",
    #     title="Mapa Conceptual - Introducción a Python"
    # )
    # print(f"Mapa generado: {map_path}")

    print("ConceptMapGenerator listo para usar")
