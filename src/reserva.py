"""
Nombre del estudiante: Maryury Alejandra Hurtado Espinosa
Grupo: 591
Curso: Programación - 213023A_2204
Declaración de herramientas: Código estructurado con apoyo de asistente de IA 
para plantillas de POO y depuración de excepciones, validado y adaptado por la autora.
"""

from datetime import datetime
from src.cliente import Cliente


try:
    from src.exceptions import ReservaError, OperacionNoPermitidaError, DatosInvalidosError
    from src.logger import registrar_evento, registrar_error
except ImportError:
    class ReservaError(Exception):
        pass

    class OperacionNoPermitidaError(Exception):
        pass

    class DatosInvalidosError(Exception):
        pass

    def registrar_evento(mensaje):
        print(f"[EVENTO]: {mensaje}")

    def registrar_error(mensaje):
        print(f"[ERROR]: {mensaje}")


class Reserva:
    """
    Gestiona la reserva de un servicio por parte de un cliente en Software FJ.
    Implementa estados, validaciones estrictas y manejo avanzado de excepciones.
    """
    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "PROCESADA", "CANCELADA")

    def __init__(self, codigo_reserva: str, cliente: Cliente, servicio, duracion_horas: float):
        self.codigo_reserva = codigo_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion_horas = duracion_horas
        self.__estado = "PENDIENTE"
        self.__fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__costo_total = 0.0

        registrar_evento(f"Reserva {self.codigo_reserva} creada en estado PENDIENTE para {self.cliente.nombre}.")

    # --- ENCAPSULACIÓN Y VALIDACIONES ---
    @property
    def codigo_reserva(self) -> str:
        return self.__codigo_reserva

    @codigo_reserva.setter
    def codigo_reserva(self, valor: str):
        if not valor or not str(valor).strip():
            raise DatosInvalidosError("El código de reserva no puede estar vacío.")
        self.__codigo_reserva = str(valor).strip().upper()

    @property
    def cliente(self) -> Cliente:
        return self.__cliente

    @cliente.setter
    def cliente(self, valor: Cliente):
        if not isinstance(valor, Cliente):
            raise DatosInvalidosError("El objeto asignado no corresponde a un Cliente válido.")
        self.__cliente = valor

    @property
    def servicio(self):
        return self.__servicio

    @servicio.setter
    def servicio(self, valor):
        if valor is None:
            raise DatosInvalidosError("Debe asociar un servicio válido a la reserva.")
        self.__servicio = valor

    @property
    def duracion_horas(self) -> float:
        return self.__duracion_horas

    @duracion_horas.setter
    def duracion_horas(self, valor: float):
        try:
            horas = float(valor)
        except (ValueError, TypeError) as e:
            # Encadenamiento de excepciones exigido por la guía
            raise DatosInvalidosError(f"La duración '{valor}' debe ser un valor numérico.") from e

        if horas <= 0:
            raise DatosInvalidosError("La duración de la reserva debe ser mayor a 0 horas.")
        self.__duracion_horas = horas

    @property
    def estado(self) -> str:
        return self.__estado

    @property
    def costo_total(self) -> float:
        return self.__costo_total

    # --- MÉTODOS DE NEGOCIO CON MANEJO AVANZADO DE EXCEPCIONES ---

    def confirmar_reserva(self):
        """
        Confirma una reserva pendiente utilizando bloque try / except / else.
        """
        try:
            if self.__estado != "PENDIENTE":
                raise OperacionNoPermitidaError(
                    f"No se puede confirmar la reserva {self.codigo_reserva} porque está en estado '{self.__estado}'."
                )
            if hasattr(self.__servicio, "disponible") and not self.__servicio.disponible:
                raise ReservaError(f"El servicio '{self.__servicio}' no está disponible actualmente.")
        except (OperacionNoPermitidaError, ReservaError) as e:
            registrar_error(f"Error al confirmar reserva {self.codigo_reserva}: {e}")
            raise
        else:
            # Solo se ejecuta si no hubo excepciones en el bloque try
            self.__estado = "CONFIRMADA"
            registrar_evento(f"Reserva {self.codigo_reserva} CONFIRMADA exitosamente.")

    def procesar_reserva(self, descuento: float = 0.0, aplicar_iva: bool = True):
        """
        Calcula el costo final y procesa la reserva.
        Implementa try / except / finally y encadenamiento de excepciones.
        """
        try:
            if self.__estado != "CONFIRMADA":
                raise OperacionNoPermitidaError(
                    f"La reserva {self.codigo_reserva} debe estar CONFIRMADA antes de procesarse (Estado actual: {self.__estado})."
                )

            # Invoca el método polimórfico calcular_costo() de la clase Servicio del Módulo 3
            if hasattr(self.__servicio, "calcular_costo"):
                self.__costo_total = self.__servicio.calcular_costo(
                    horas=self.__duracion_horas,
                    descuento=descuento,
                    aplicar_iva=aplicar_iva
                )
            else:
                raise ReservaError("El servicio asociado no implementa el cálculo de costos.")

            self.__estado = "PROCESADA"
            registrar_evento(
                f"Reserva {self.codigo_reserva} PROCESADA. Costo total: ${self.__costo_total:,.2f}"
            )

        except OperacionNoPermitidaError as e:
            registrar_error(f"Fallo de estado al procesar {self.codigo_reserva}: {e}")
            raise
        except Exception as e:
            # Encadenamiento de cualquier error matemático o de cálculo interno
            registrar_error(f"Error crítico procesando costos en {self.codigo_reserva}: {e}")
            raise ReservaError(f"Fallo inesperado al procesar la reserva {self.codigo_reserva}.") from e
        finally:
            # Se ejecuta siempre, haya error o no, dejando traza de auditoría
            registrar_evento(f"Auditoría de procesamiento finalizada para reserva {self.codigo_reserva} (Estado: {self.__estado}).")

    def cancelar_reserva(self, motivo: str = "Cancelación solicitada por el cliente"):
        """
        Cancela una reserva siempre que no haya sido procesada previamente.
        """
        try:
            if self.__estado == "PROCESADA":
                raise OperacionNoPermitidaError(
                    f"No es posible cancelar la reserva {self.codigo_reserva} porque ya fue PROCESADA."
                )
            if self.__estado == "CANCELADA":
                raise OperacionNoPermitidaError(
                    f"La reserva {self.codigo_reserva} ya se encuentra CANCELADA."
                )
        except OperacionNoPermitidaError as e:
            registrar_error(f"Intento inválido de cancelación en {self.codigo_reserva}: {e}")
            raise
        else:
            self.__estado = "CANCELADA"
            registrar_evento(f"Reserva {self.codigo_reserva} CANCELADA. Motivo: {motivo}")

    def __str__(self) -> str:
        return (
            f"Reserva[{self.codigo_reserva}] | Cliente: {self.cliente.nombre} | "
            f"Duración: {self.duracion_horas}h | Estado: {self.estado} | Total: ${self.costo_total:,.2f}"
        )


# --- BLOQUE DE PRUEBAS UNITARIAS DEL MÓDULO RESERVA ---
if __name__ == "__main__":
    print("=== INICIANDO PRUEBAS DEL MÓDULO RESERVA ===\n")

    # Clase simulada temporal de Servicio mientras se integra el Módulo 3
    class ServicioMock:
        def __init__(self, nombre, tarifa, disponible=True):
            self.nombre = nombre
            self.tarifa = tarifa
            self.disponible = disponible

        def calcular_costo(self, horas, descuento=0.0, aplicar_iva=True):
            subtotal = (self.tarifa * horas) * (1 - descuento)
            return subtotal * 1.19 if aplicar_iva else subtotal

        def __str__(self):
            return self.nombre

    cliente_prueba = Cliente("1020304050", "Alejandra Hurtado", "alejandra@correo.com", "3001234567")
    sala_juntas = ServicioMock("Sala de Juntas VIP", 50000)

    # 1. Flujo exitoso: Crear -> Confirmar -> Procesar
    try:
        r1 = Reserva("RES-001", cliente_prueba, sala_juntas, 3)
        r1.confirmar_reserva()
        r1.procesar_reserva(descuento=0.10, aplicar_iva=True)
        print("OK ->", r1)
    except Exception as e:
        print("Error inesperado:", e)

    print("-" * 50)

    # 2. Error controlado: Intentar cancelar una reserva ya PROCESADA
    try:
        r1.cancelar_reserva()
    except OperacionNoPermitidaError as e:
        print(f"EXCEPCIÓN CONTROLADA -> {e}")

    print("-" * 50)

    # 3. Encadenamiento de excepciones: Duración no numérica
    try:
        r2 = Reserva("RES-002", cliente_prueba, sala_juntas, "cuatro_horas")
    except DatosInvalidosError as e:
        print(f"ENCADENAMIENTO CAPTURADO -> {e} | Causa original: {type(e.__cause__).__name__}")
