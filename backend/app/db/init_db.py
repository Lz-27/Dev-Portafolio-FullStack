"""
db/init_db.py
─────────────
Inicialización de la base de datos:
  1. Crea todas las tablas (si no existen)
  2. Inserta el usuario admin por defecto (si no existe)
  3. Inserta los datos iniciales del portafolio (proyectos y certificaciones)
"""
from __future__ import annotations

import json
import logging

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_password
from app.db.database import Base, engine
from app.models import Certification, Message, Project, User  # noqa: F401 — registra tablas

logger = logging.getLogger(__name__)

# ── Datos iniciales del portafolio (desde content.js) ────────────────────────
_INITIAL_PROJECTS = [
    {
        "slug": "sistema-prediccion-ventas",
        "titulo": "Sistema de Predicción de Ventas",
        "descripcion": "Modelo ML para predecir ventas con series temporales y análisis de tendencias.",
        "detalles": "Desarrollo completo de un sistema de predicción de ventas usando Python, TensorFlow y FastAPI. El modelo alcanza 94% de precisión en predicciones a 30 días utilizando LSTM y técnicas de feature engineering avanzadas.",
        "categoria": "data",
        "categoria_label": "Data / IA",
        "tecnologias": json.dumps(["Python", "TensorFlow", "FastAPI", "React", "PostgreSQL"]),
        "github": "https://github.com/tu-usuario/proyecto",
        "demo": "https://demo.com",
        "destacado": True,
    },
    {
        "slug": "dashboard-analisis-realtime",
        "titulo": "Dashboard de Análisis en Tiempo Real",
        "descripcion": "Visualización interactiva de métricas y datos con WebSockets y D3.js.",
        "detalles": "Dashboard interactivo construido con React y D3.js que procesa datos en tiempo real desde múltiples fuentes vía WebSockets. Maneja hasta 10,000 eventos/segundo con latencia sub-100ms.",
        "categoria": "fullstack",
        "categoria_label": "Full-Stack",
        "tecnologias": json.dumps(["React", "Node.js", "D3.js", "WebSockets", "MongoDB"]),
        "github": "https://github.com/tu-usuario/proyecto",
        "demo": "https://demo.com",
        "destacado": True,
    },
    {
        "slug": "plataforma-ecommerce",
        "titulo": "Plataforma E-Commerce",
        "descripcion": "Tienda online completa con gestión de inventario, pagos y panel admin.",
        "detalles": "Sistema e-commerce full-stack con React en el frontend y FastAPI+SQLAlchemy en el backend. Incluye autenticación JWT, gestión de pedidos, integración con pasarelas de pago y panel administrativo CMS.",
        "categoria": "fullstack",
        "categoria_label": "Full-Stack",
        "tecnologias": json.dumps(["React", "FastAPI", "SQLAlchemy", "PostgreSQL", "JWT"]),
        "github": "https://github.com/tu-usuario/proyecto",
        "demo": "https://demo.com",
        "destacado": True,
    },
    {
        "slug": "vision-computacional-defectos",
        "titulo": "Detección de Defectos con Visión Computacional",
        "descripcion": "Sistema automatizado de control de calidad usando OpenCV y CNN.",
        "detalles": "Pipeline de procesamiento de imágenes que detecta defectos en líneas de manufactura con 97% de precisión. Usa CNNs personalizadas y OpenCV para segmentación y clasificación en tiempo real.",
        "categoria": "data",
        "categoria_label": "Data / IA",
        "tecnologias": json.dumps(["Python", "OpenCV", "PyTorch", "FastAPI", "Docker"]),
        "github": "https://github.com/tu-usuario/proyecto",
        "demo": None,
        "destacado": False,
    },
    {
        "slug": "gestor-inventario-pyqt6",
        "titulo": "Gestor de Inventario Desktop",
        "descripcion": "Aplicación de escritorio para control de stock con reportes y alertas.",
        "detalles": "Aplicación de escritorio desarrollada con PyQt6 y SQLite. Incluye generación de reportes en PDF, sistema de alertas por bajo stock, dashboard visual con gráficos y exportación a Excel.",
        "categoria": "desktop",
        "categoria_label": "Desktop",
        "tecnologias": json.dumps(["Python", "PyQt6", "SQLite", "Matplotlib", "ReportLab"]),
        "github": "https://github.com/tu-usuario/proyecto",
        "demo": None,
        "destacado": False,
    },
    {
        "slug": "api-microservicios",
        "titulo": "Arquitectura de Microservicios",
        "descripcion": "API gateway con servicios independientes orquestados con Docker Compose.",
        "detalles": "Arquitectura de microservicios con FastAPI donde cada dominio (usuarios, pedidos, notificaciones) es un servicio independiente. Comunicación via REST y mensajería con Redis. Orquestado con Docker Compose.",
        "categoria": "backend",
        "categoria_label": "Backend",
        "tecnologias": json.dumps(["FastAPI", "Docker", "Redis", "PostgreSQL", "JWT"]),
        "github": "https://github.com/tu-usuario/proyecto",
        "demo": None,
        "destacado": False,
    },
]

_INITIAL_CERTIFICATIONS = [
    {
        "titulo": "Universidad Desarrollo Web",
        "emisor": "DataCamp",
        "fecha": "2022",
        "categoria": "data",
        "categoria_label": "Data & IA",
        "habilidades": json.dumps(["Python", "Machine Learning", "Statistics", "Deep Learning"]),
        "descripcion": "Certificación integral en Data Science cubriendo estadística, machine learning, deep learning y visualización de datos con Python.",
        "credencial": "https://www.datacamp.com",
    },
    {
        "titulo": "AWS Cloud Practitioner",
        "emisor": "Amazon Web Services",
        "fecha": "2023",
        "categoria": "cloud",
        "categoria_label": "Cloud",
        "habilidades": json.dumps(["AWS", "Cloud Computing", "S3", "EC2", "IAM"]),
        "descripcion": "Fundamentos de servicios cloud de AWS: computación, almacenamiento, redes, seguridad y arquitectura de soluciones.",
        "credencial": "https://aws.amazon.com/certification/",
    },
    {
        "titulo": "TensorFlow Developer Certificate",
        "emisor": "Google",
        "fecha": "2023",
        "categoria": "data",
        "categoria_label": "Data & IA",
        "habilidades": json.dumps(["TensorFlow", "Deep Learning", "NLP", "Computer Vision"]),
        "descripcion": "Construcción y entrenamiento de modelos de deep learning para visión computacional, NLP y series temporales.",
        "credencial": "https://www.tensorflow.org/certificate",
    },
    {
        "titulo": "React Developer Certification",
        "emisor": "Meta",
        "fecha": "2022",
        "categoria": "dev",
        "categoria_label": "Desarrollo",
        "habilidades": json.dumps(["React", "JavaScript", "Redux", "REST APIs"]),
        "descripcion": "Dominio del ecosistema React: hooks, context, routing, state management y optimización de rendimiento.",
        "credencial": "https://www.coursera.org/professional-certificates/meta-front-end-developer",
    },
    {
        "titulo": "Python for Everybody Specialization",
        "emisor": "University of Michigan",
        "fecha": "2021",
        "categoria": "dev",
        "categoria_label": "Desarrollo",
        "habilidades": json.dumps(["Python", "SQL", "Web Scraping", "APIs"]),
        "descripcion": "Especialización completa en Python abarcando desde fundamentos hasta bases de datos, web scraping y APIs.",
        "credencial": "https://www.coursera.org/specializations/python",
    },
    {
        "titulo": "Docker & Kubernetes Essentials",
        "emisor": "Linux Foundation",
        "fecha": "2023",
        "categoria": "cloud",
        "categoria_label": "Cloud",
        "habilidades": json.dumps(["Docker", "Kubernetes", "CI/CD", "DevOps"]),
        "descripcion": "Containerización de aplicaciones con Docker y orquestación de servicios con Kubernetes en entornos de producción.",
        "credencial": "https://training.linuxfoundation.org",
    },
]


def _create_tables() -> None:
    """Crea todas las tablas definidas en los modelos."""
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Tablas creadas / verificadas")


def _seed_admin(db: Session) -> None:
    """Inserta el usuario admin si no existe."""
    existing = db.query(User).filter(User.username == settings.FIRST_ADMIN_USERNAME).first()
    if existing:
        logger.info("👤 Admin ya existe — omitiendo seed")
        return

    admin = User(
        username=settings.FIRST_ADMIN_USERNAME,
        email=settings.FIRST_ADMIN_EMAIL,
        hashed_password=hash_password(settings.FIRST_ADMIN_PASSWORD),
        is_admin=True,
        is_active=True,
    )
    db.add(admin)
    db.commit()
    logger.info(f"✅ Admin creado: {settings.FIRST_ADMIN_USERNAME}")


def _seed_projects(db: Session) -> None:
    """Inserta los proyectos iniciales si la tabla está vacía."""
    if db.query(Project).count() > 0:
        logger.info("📁 Proyectos ya existen — omitiendo seed")
        return

    for data in _INITIAL_PROJECTS:
        db.add(Project(**data))
    db.commit()
    logger.info(f"✅ {len(_INITIAL_PROJECTS)} proyectos insertados")


def _seed_certifications(db: Session) -> None:
    """Inserta las certificaciones iniciales si la tabla está vacía."""
    if db.query(Certification).count() > 0:
        logger.info("🏆 Certificaciones ya existen — omitiendo seed")
        return

    for data in _INITIAL_CERTIFICATIONS:
        db.add(Certification(**data))
    db.commit()
    logger.info(f"✅ {len(_INITIAL_CERTIFICATIONS)} certificaciones insertadas")


def init_db(db: Session) -> None:
    """
    Punto de entrada principal de inicialización.
    Se llama en el startup event de FastAPI.
    """
    _create_tables()
    _seed_admin(db)
    _seed_projects(db)
    _seed_certifications(db)
    logger.info("🚀 Base de datos inicializada correctamente")
