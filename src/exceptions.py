"""
Nombre del estudiante: [Juan Sebastian Cortes Saenz]
Grupo: 591
Curso: Programación - 213023A_2204
Módulo 1: Excepciones personalizadas del sistema Software FJ.
"""


class SoftwareFJError(Exception):
    """Excepción base para todos los errores controlados del sistema Software FJ."""
    pass


class DatosInvalidosError(SoftwareFJError):
    """Se lanza cuando los datos ingresados (cliente, duración, código, etc.) no cumplen las validaciones."""
    pass


class ReservaError(SoftwareFJError):
    """Se lanza cuando ocurre un fallo general o de disponibilidad en una reserva."""
    pass


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza cuando se intenta realizar una transición de estado inválida en una reserva."""
    pass
