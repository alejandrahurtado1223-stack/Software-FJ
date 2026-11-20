"""
Nombre del estudiante: Juan Sebastian Cortes Saenz
Grupo: 591
Curso: Programación - 213023A_2204
Módulo 1: Sistema de registro de eventos y errores (Logs) para Software FJ.
"""

import logging
import os

RUTA_LOG = os.path.join(os.path.dirname(os.path.dirname(__file__)), "software_fj.log")

logger = logging.getLogger("SoftwareFJ")
logger.setLevel(logging.INFO)

if not logger.handlers:
    formato = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    try:
        file_handler = logging.FileHandler(RUTA_LOG, mode="a", encoding="utf-8")
        file_handler.setFormatter(formato)
        logger.addHandler(file_handler)
    except OSError as e:
        print(f"Advertencia: no se pudo abrir el archivo de logs ({e}).")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formato)
    logger.addHandler(console_handler)


def registrar_evento(mensaje: str) -> None:
    """Registra una operación exitosa o evento informativo en el log."""
    logger.info(mensaje)


def registrar_error(mensaje: str) -> None:
    """Registra un error controlado o excepción en el log."""
    logger.error(mensaje)
