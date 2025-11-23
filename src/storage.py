"""Gestión de almacenamiento en Azure Blob Storage."""

import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from pathlib import Path
import logging
from typing import Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AzureStorageManager:
    """Gestor de almacenamiento en Azure Blob Storage."""

    def __init__(
        self,
        connection_string: Optional[str] = None,
        container_name: Optional[str] = None
    ):
        """
        Inicializa el gestor de almacenamiento.

        Args:
            connection_string: Cadena de conexión de Azure Storage
            container_name: Nombre del contenedor
        """
        self.connection_string = connection_string or os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.container_name = container_name or os.getenv("AZURE_STORAGE_CONTAINER_NAME", "educational-content")

        if not self.connection_string:
            logger.warning("AZURE_STORAGE_CONNECTION_STRING no configurada. Modo local activado.")
            self.enabled = False
            return

        try:
            self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
            self._ensure_container_exists()
            self.enabled = True
            logger.info(f"Azure Storage configurado. Contenedor: {self.container_name}")

        except Exception as e:
            logger.error(f"Error al configurar Azure Storage: {e}")
            self.enabled = False

    def _ensure_container_exists(self):
        """Asegura que el contenedor existe, si no, lo crea."""
        try:
            container_client = self.blob_service_client.get_container_client(self.container_name)
            if not container_client.exists():
                container_client.create_container()
                logger.info(f"Contenedor '{self.container_name}' creado")
        except Exception as e:
            logger.error(f"Error al verificar/crear contenedor: {e}")
            raise

    def upload_file(
        self,
        file_path: str,
        blob_name: Optional[str] = None,
        folder: str = ""
    ) -> Optional[str]:
        """
        Sube un archivo a Azure Blob Storage.

        Args:
            file_path: Ruta del archivo local
            blob_name: Nombre del blob (opcional, usa nombre del archivo si no se especifica)
            folder: Carpeta dentro del contenedor

        Returns:
            URL del blob subido o None si no está habilitado
        """
        if not self.enabled:
            logger.warning("Azure Storage no está habilitado. Archivo no subido.")
            return None

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

        # Determinar nombre del blob
        if blob_name is None:
            blob_name = Path(file_path).name

        # Agregar folder si se especifica
        if folder:
            blob_name = f"{folder.rstrip('/')}/{blob_name}"

        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )

            # Subir archivo
            logger.info(f"Subiendo {file_path} a Azure como {blob_name}...")
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)

            # Obtener URL
            blob_url = blob_client.url
            logger.info(f"Archivo subido exitosamente: {blob_url}")

            return blob_url

        except Exception as e:
            logger.error(f"Error al subir archivo a Azure: {e}")
            raise

    def upload_multiple(
        self,
        file_paths: list,
        folder: str = ""
    ) -> dict:
        """
        Sube múltiples archivos a Azure Blob Storage.

        Args:
            file_paths: Lista de rutas de archivos
            folder: Carpeta dentro del contenedor

        Returns:
            Diccionario {nombre_archivo: url_blob}
        """
        results = {}

        for file_path in file_paths:
            try:
                url = self.upload_file(file_path, folder=folder)
                results[Path(file_path).name] = url
            except Exception as e:
                logger.error(f"Error al subir {file_path}: {e}")
                results[Path(file_path).name] = None

        return results

    def download_file(
        self,
        blob_name: str,
        download_path: str
    ) -> str:
        """
        Descarga un archivo desde Azure Blob Storage.

        Args:
            blob_name: Nombre del blob
            download_path: Ruta donde guardar el archivo

        Returns:
            Ruta del archivo descargado
        """
        if not self.enabled:
            raise Exception("Azure Storage no está habilitado")

        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )

            logger.info(f"Descargando {blob_name} desde Azure...")

            # Asegurar que el directorio existe
            Path(download_path).parent.mkdir(parents=True, exist_ok=True)

            with open(download_path, "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())

            logger.info(f"Archivo descargado: {download_path}")
            return download_path

        except Exception as e:
            logger.error(f"Error al descargar archivo: {e}")
            raise

    def get_blob_url(self, blob_name: str, expiry_hours: int = 24) -> Optional[str]:
        """
        Obtiene una URL con SAS token para acceder al blob.

        Args:
            blob_name: Nombre del blob
            expiry_hours: Horas de validez del SAS token

        Returns:
            URL con SAS token
        """
        if not self.enabled:
            return None

        try:
            from azure.storage.blob import generate_blob_sas, BlobSasPermissions

            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )

            # Generar SAS token
            sas_token = generate_blob_sas(
                account_name=blob_client.account_name,
                container_name=self.container_name,
                blob_name=blob_name,
                account_key=self.blob_service_client.credential.account_key,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(hours=expiry_hours)
            )

            # Construir URL completa
            url_with_sas = f"{blob_client.url}?{sas_token}"
            return url_with_sas

        except Exception as e:
            logger.error(f"Error al generar URL con SAS: {e}")
            return blob_client.url

    def list_blobs(self, folder: str = "") -> list:
        """
        Lista los blobs en un contenedor o carpeta.

        Args:
            folder: Carpeta a listar (opcional)

        Returns:
            Lista de nombres de blobs
        """
        if not self.enabled:
            return []

        try:
            container_client = self.blob_service_client.get_container_client(self.container_name)

            if folder:
                blobs = container_client.list_blobs(name_starts_with=folder)
            else:
                blobs = container_client.list_blobs()

            blob_names = [blob.name for blob in blobs]
            return blob_names

        except Exception as e:
            logger.error(f"Error al listar blobs: {e}")
            return []

    def delete_blob(self, blob_name: str) -> bool:
        """
        Elimina un blob del almacenamiento.

        Args:
            blob_name: Nombre del blob a eliminar

        Returns:
            True si se eliminó correctamente
        """
        if not self.enabled:
            return False

        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )

            blob_client.delete_blob()
            logger.info(f"Blob eliminado: {blob_name}")
            return True

        except Exception as e:
            logger.error(f"Error al eliminar blob: {e}")
            return False


if __name__ == "__main__":
    # Ejemplo de uso
    storage = AzureStorageManager()

    if storage.enabled:
        # Ejemplo de subida
        # url = storage.upload_file("output/study_guide.pdf", folder="guides")
        # print(f"Archivo subido: {url}")

        # Ejemplo de listado
        # blobs = storage.list_blobs()
        # print(f"Blobs: {blobs}")

        print("AzureStorageManager configurado y listo")
    else:
        print("AzureStorageManager en modo local (Azure no configurado)")
