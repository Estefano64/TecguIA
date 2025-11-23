"""Modelos de base de datos para TecguIA."""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tecguia.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class VideoProcessing(Base):
    """Registro de procesamiento de videos."""

    __tablename__ = "video_processing"

    id = Column(Integer, primary_key=True, index=True)
    video_url = Column(String, nullable=True)
    video_path = Column(String, nullable=True)
    audio_path = Column(String, nullable=True)
    transcription_path = Column(String, nullable=True)
    summary_path = Column(String, nullable=True)
    fidelity_score = Column(Float, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = Column(JSON, nullable=True)


class GeneratedArtifact(Base):
    """Artefactos generados (PDF, mapas, podcasts)."""

    __tablename__ = "generated_artifacts"

    id = Column(Integer, primary_key=True, index=True)
    processing_id = Column(Integer, nullable=False)
    artifact_type = Column(String, nullable=False)  # pdf, map, podcast
    local_path = Column(String, nullable=True)
    blob_url = Column(String, nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON, nullable=True)


def init_db():
    """Inicializa la base de datos."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Obtiene una sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
