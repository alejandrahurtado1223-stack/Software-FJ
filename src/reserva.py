"""
Nombre del estudiante: Maryury Alejandra Hurtado Espinosa
Grupo: 591
Curso: Programación - 213023A_2204
Declaración de herramientas: Código estructurado con apoyo de asistente de IA
para plantillas de POO y manejo de excepciones, validado y adaptado por la autora.
"""

from src.entidad_base import EntidadBase
from src.cliente import Cliente
from src.exceptions import ReservaError, OperacionNoPermitidaError, DatosInvalidosError
from src.logger import registrar_evento, registrar_error


class Reserva(EntidadBase):
    """
    Gestiona la reserva de un servicio por parte de un cliente en Software FJ.
    Hereda de EntidadBase e implementa estados, validaciones y manejo de excepciones.
    """
    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "PROCESADA", "CANCELADA")

    def __init__(self, codigo_reserva: str, cliente: Cliente, servicio, duracion_horas: float):
        try:
            super().__init__(str(codigo_reserva).strip().upper())
        except ValueError as e:
            registrar_error(str(e))
            raise DatosInvalidosError(str(e)) from e

        self.cliente = cliente
        self.servicio = servicio
        self.duracion_horas = duracion_horas
        self.__estado = "PENDIENTE"
        self.__costo_total = 0.0

        registrar_evento(f"Reserva {self.codigo_reserva} creada en estado PENDIENTE para {self.cliente.nombre}.")

    @property
    def codigo_reserva(self) -> str:
        return self.id_entidad

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

    def confirmar_reserva(self):
        """Confirma una reserva pendiente utilizando bloque try / except / else."""
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
            self.__estado = "CONFIRMADA"
            registrar_evento(f"Reserva {self.codigo_reserva} CONFIRMADA exitosamente.")

    def procesar_reserva(self, descuento: float = 0.0, aplicar_iva: bool = True):
        """Calcula el costo final y procesa la reserva con try / except / finally."""
        try:
            if self.__estado != "CONFIRMADA":
                raise OperacionNoPermitidaError(
                    f"La reserva {self.codigo_reserva} debe estar CONFIRMADA antes de procesarse (Estado actual: {self.__estado})."
                )

            if hasattr(self.__servicio, "calcular_costo"):
                try:
                    self.__costo_total = self.__servicio.calcular_costo(
                        horas=self.__duracion_horas,
                        descuento=descuento,
                        aplicar_iva=aplicar_iva
                    )
                except TypeError:
                    # Respaldo por si el método calcular_costo del compañero usa otra firma
                    self.__costo_total = self.__servicio.calcular_costo()
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
            registrar_error(f"Error crítico procesando costos en {self.codigo_reserva}: {e}")
            raise ReservaError(f"Fallo inesperado al procesar la reserva {self.codigo_reserva}.") from e
        finally:
            registrar_evento(
                f"Auditoría de procesamiento finalizada para reserva {self.codigo_reserva} (Estado: {self.__estado})."
            )

    def cancelar_reserva(self, motivo: str = "Cancelación solicitada por el cliente"):
        """Cancela una reserva siempre que no haya sido procesada previamente."""
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

    def obtener_resumen(self) -> str:
        """Implementación obligatoria del método abstracto de EntidadBase."""
        return (
            f"Reserva[{self.codigo_reserva}] | Cliente: {self.cliente.nombre} | "
            f"Duración: {self.duracion_horas}h | Estado: {self.estado} | Total: ${self.costo_total:,.2f}"
        )

    def __str__(self) -> str:
        return self.obtener_resumen()