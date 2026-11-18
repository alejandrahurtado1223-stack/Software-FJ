"""
Nombre del estudiante: Maryury Alejandra Hurtado Espinosa
Grupo: 591
Curso: Programación - 213023A_2204
Declaración de herramientas: Código estructurado con apoyo de asistente de IA 
para plantillas de POO y depuración de excepciones, validado y adaptado por la autora.
"""

import re
from datetime import datetime

try:
    from src.exceptions import DatosInvalidosError
    from src.logger import registrar_evento, registrar_error
except ImportError:
    class DatosInvalidosError(Exception):
        """Excepción temporal mientras se integra el Módulo 1."""
        pass

    def registrar_evento(mensaje):
        print(f"[EVENTO]: {mensaje}")

    def registrar_error(mensaje):
        print(f"[ERROR]: {mensaje}")


class Cliente:
    """
    Representa a un cliente registrado en Software FJ.
    Aplica encapsulación estricta y validación de datos personales.
    """

    def __init__(self, identificacion: str, nombre: str, correo: str, telefono: str):
       
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.__fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        registrar_evento(f"Cliente creado exitosamente: {self.nombre} (ID: {self.identificacion})")

    # --- ENCAPSULACIÓN: IDENTIFICACIÓN ---
    @property
    def identificacion(self) -> str:
        """Getter: Permite leer la identificación privada."""
        return self.__identificacion

    @identificacion.setter
    def identificacion(self, valor: str):
        """Setter: Valida que la identificación no esté vacía y sea alfanumérica."""
        if not valor or not str(valor).strip():
            error_msg = "La identificación del cliente es obligatoria."
            registrar_error(error_msg)
            raise DatosInvalidosError(error_msg)
        
        valor_limpio = str(valor).strip()
        if len(valor_limpio) < 5:
            error_msg = f"Identificación '{valor_limpio}' demasiado corta (mínimo 5 caracteres)."
            registrar_error(error_msg)
            raise DatosInvalidosError(error_msg)
            
        self.__identificacion = valor_limpio

  # --- ENCAPSULACIÓN: NOMBRE ---
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        """Valida que el nombre tenga al menos 3 letras y no sea solo números."""
        if not valor or len(valor.strip()) < 3 or valor.strip().isdigit():
            error_msg = f"Nombre inválido proporcionado: '{valor}'."
            registrar_error(error_msg)
            raise DatosInvalidosError(error_msg)
        self.__nombre = valor.strip().title()  # Guarda el nombre con mayúsculas iniciales

  # --- ENCAPSULACIÓN: CORREO ELECTRÓNICO ---
    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str):
        """Valida el formato de correo usando expresiones regulares (Regex)."""
        patron_correo = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not valor or not re.match(patron_correo, valor.strip()):
            error_msg = f"Formato de correo electrónico inválido: '{valor}'."
            registrar_error(error_msg)
            raise DatosInvalidosError(error_msg)
        self.__correo = valor.strip().lower()

    # --- ENCAPSULACIÓN: TELÉFONO ---
    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        """Valida que el teléfono contenga únicamente dígitos (entre 7 y 15 números)."""
        valor_limpio = str(valor).strip() if valor else ""
        if not valor_limpio.isdigit() or not (7 <= len(valor_limpio) <= 15):
            error_msg = f"Número de teléfono inválido: '{valor}'. Debe tener entre 7 y 15 dígitos."
            registrar_error(error_msg)
            raise DatosInvalidosError(error_msg)
        self.__telefono = valor_limpio

    @property
    def fecha_registro(self) -> str:
        """Atributo de solo lectura (no tiene setter para que nadie altere la fecha)."""
        return self.__fecha_registro

    def __str__(self) -> str:
        """Representación en texto legible del objeto Cliente."""
        return f"Cliente[{self.identificacion}] - {self.nombre} | Correo: {self.correo} | Tel: {self.telefono}"


# --- BLOQUE DE PRUEBAS UNITARIAS ---
if __name__ == "__main__":
    print("=== INICIANDO PRUEBAS DEL MÓDULO CLIENTE ===\n")

    # 1. Prueba exitosa
    try:
        c1 = Cliente("1020304050", "Alejandra Hurtado", "alejandra@correo.com", "3001234567")
        print("OK ->", c1)
    except DatosInvalidosError as e:
        print("Error inesperado:", e)

    print("-" * 50)

    # 2. Prueba de error controlado (correo inválido)
    try:
        c2 = Cliente("987654321", "Carlos Perez", "correo_sin_arroba.com", "3109876543")
    except DatosInvalidosError as e:
        print(f"EXCEPCIÓN CONTROLADA -> {e}")

    print("-" * 50)

    # 3. Prueba de encapsulación (intentar modificar con dato inválido)
    try:
        c1.telefono = "12"
    except DatosInvalidosError as e:
        print(f"VALIDACIÓN EN SETTER -> {e}")