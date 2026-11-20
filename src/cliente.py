"""
Nombre del estudiante: Maryury Alejandra Hurtado Espinosa
Grupo: 591
Curso: Programación - 213023A_2204
Declaración de herramientas: Código estructurado con apoyo de asistente de IA
para plantillas de POO y manejo de excepciones, validado y adaptado por la autora.
"""

import re
from src.entidad_base import EntidadBase
from src.exceptions import DatosInvalidosError
from src.logger import registrar_evento, registrar_error


class Cliente(EntidadBase):
    """
    Representa a un cliente dentro del sistema Software FJ.
    Hereda de EntidadBase e implementa encapsulación y validaciones estrictas.
    """

    def __init__(self, identificacion: str, nombre: str, correo: str, telefono: str):
        try:
            super().__init__(identificacion)
        except ValueError as e:
            registrar_error(str(e))
            raise DatosInvalidosError(str(e)) from e

        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

        registrar_evento(f"Cliente creado exitosamente: {self.nombre} (ID: {self.id_entidad})")

    @property
    def identificacion(self) -> str:
        return self.id_entidad

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            error_msg = f"Nombre inválido: '{valor}'. Debe tener al menos 3 caracteres."
            registrar_error(error_msg)
            raise DatosInvalidosError(error_msg)
        self.__nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str):
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not isinstance(valor, str) or not re.match(patron, valor.strip()):
            error_msg = f"Formato de correo electrónico inválido: '{valor}'."
            registrar_error(error_msg)
            raise DatosInvalidosError(error_msg)
        self.__correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        if valor is None:
            error_msg = f"Número de teléfono inválido: '{valor}'. Debe tener entre 7 y 15 dígitos."
            registrar_error(error_msg)
            raise DatosInvalidosError(error_msg)
        valor_limpio = str(valor).strip()
        if not valor_limpio.isdigit() or not (7 <= len(valor_limpio) <= 15):
            error_msg = f"Número de teléfono inválido: '{valor}'. Debe tener entre 7 y 15 dígitos."
            registrar_error(error_msg)
            raise DatosInvalidosError(error_msg)
        self.__telefono = valor_limpio

    def obtener_resumen(self) -> str:
        """Implementación obligatoria del método abstracto de EntidadBase."""
        return f"Cliente[{self.identificacion}] - {self.nombre} | Correo: {self.correo} | Tel: {self.telefono}"

    def __str__(self) -> str:
        return self.obtener_resumen()
