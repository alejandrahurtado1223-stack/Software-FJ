"""
Nombre del estudiante: [Juan Sebastian Cortes Saenz]
Grupo: 591
Curso: Programación - 213023A_2204
Módulo 1: Sistema de registro de eventos y errores (Logs) para Software FJ.
"""

import logging
import os

# Ruta del archivo .log en la raíz del proyecto para que guarde toda la ejecución sin interrupciones
RUTA_LOG = os.path.join(os.path.dirname(os.path.dirname(__file__)), "software_fj.log")

# Configuración del logger principal
logger = logging.getLogger("SoftwareFJ")
logger.setLevel(logging.INFO)

# Evitar duplicar manejadores si el módulo se importa varias veces
if not logger.handlers:
    formato = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Manejador para guardar en archivo .log (modo 'a' para no borrar registros previos)
    file_handler = logging.FileHandler(RUTA_LOG, mode="a", encoding="utf-8")
    file_handler.setFormatter(formato)
    logger.addHandler(file_handler)

    # Manejador para mostrar también en la consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formato)
    logger.addHandler(console_handler)


def registrar_evento(mensaje: str) -> None:
    """Registra una operación exitosa o evento informativo en el archivo .log y consola."""
    logger.info(mensaje)


def registrar_error(mensaje: str) -> None:
    """Registra un error controlado o excepción en el archivo .log y consola."""
    logger.error(mensaje)
