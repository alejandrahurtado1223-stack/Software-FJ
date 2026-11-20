"""
Nombre del estudiante: Juan Sebastian Cortes Saenz
Grupo: 591
Curso: Programación - 213023A_2204
Módulo 1: Clase base abstracta para las entidades del sistema Software FJ.
"""

from abc import ABC, abstractmethod
from datetime import datetime


class EntidadBase(ABC):
    """
    Clase base abstracta que define la estructura común (identificador y fecha de creación)
    para las entidades del sistema Software FJ.
    """

    def __init__(self, id_entidad: str):
        if not id_entidad or not str(id_entidad).strip():
            raise ValueError("El identificador de la entidad no puede estar vacío.")
        self._id_entidad = str(id_entidad).strip()
        self._fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def id_entidad(self) -> str:
        return self._id_entidad

    @property
    def fecha_creacion(self) -> str:
        return self._fecha_creacion

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método obligatorio para representar la información principal de la entidad."""
        pass

    def __str__(self) -> str:
        return f"[{self._id_entidad}] Creado el {self._fecha_creacion}"
