"""
Nombre del estudiante: [Juan Sebastian Cortes Saenz]
Grupo: 591
Curso: Programación - 213023A_2204
Módulo 5 (Parte 1 - Integrante 1): Estructura principal y primeras 5 operaciones simuladas
de Software FJ (registro de clientes válidos/inválidos y creación de servicios).
"""

from src.logger import registrar_evento, registrar_error
from src.exceptions import (
    SoftwareFJError,
    DatosInvalidosError,
    ReservaError,
    OperacionNoPermitidaError,
)
from src.cliente import Cliente
from src.servicios import ReservaSalas, AlquilerEquipos, AsesoriasEspecializadas
from src.reserva import Reserva


def main():
    print("============================================================")
    print("       INICIANDO SIMULACIÓN DE OPERACIONES - SOFTWARE FJ    ")
    print("============================================================\n")
    registrar_evento("=== INICIO DE EJECUCIÓN DEL SISTEMA SOFTWARE FJ ===")

    clientes_registrados = []
    servicios_disponibles = []

    # -------------------------------------------------------------------------
    # PARTE 1 (INTEGRANTE 1): PRIMERAS 5 OPERACIONES SIMULADAS
    # -------------------------------------------------------------------------

    # OPERACIÓN 1: Registro válido de cliente 1
    print("--- Operación 1: Registro válido de cliente ---")
    try:
        cliente_1 = Cliente(
            identificacion="1020304050",
            nombre="Alejandra Hurtado",
            correo="alejandra@correo.com",
            telefono="3001234567",
        )
        clientes_registrados.append(cliente_1)
        print(f"Éxito: {cliente_1}\n")
    except DatosInvalidosError as e:
        print(f"Error controlado en Operación 1: {e}\n")

    # OPERACIÓN 2: Registro válido de cliente 2
    print("--- Operación 2: Registro válido de segundo cliente ---")
    try:
        cliente_2 = Cliente(
            identificacion="1098765432",
            nombre="Nicolas Suarez",
            correo="nicolas.suarez@correo.com",
            telefono="3109876543",
        )
        clientes_registrados.append(cliente_2)
        print(f"Éxito: {cliente_2}\n")
    except DatosInvalidosError as e:
        print(f"Error controlado en Operación 2: {e}\n")

    # OPERACIÓN 3: Registro inválido de cliente (correo sin formato válido y teléfono corto)
    print("--- Operación 3: Registro inválido de cliente (prueba de validación) ---")
    try:
        cliente_invalido = Cliente(
            identificacion="55667788",
            nombre="Carlos Perez",
            correo="carlos_sin_arroba.com",
            telefono="123",
        )
        clientes_registrados.append(cliente_invalido)
    except DatosInvalidosError as e:
        print(f"Excepción capturada correctamente: {e}\n")

    # OPERACIÓN 4: Creación de servicio tipo Reserva de Salas y Alquiler de Equipos
    print("--- Operación 4: Creación de servicios (Sala y Equipos) ---")
    try:
        sala_vip = ReservaSalas(
            id_servicio="SRV-001",
            nombre="Sala de Juntas Ejecutiva",
            costo_base=50000.0,
            horas=4,
            capacidad=12,
            incluye_catering=True,
        )
        equipos_dev = AlquilerEquipos(
            id_servicio="SRV-002",
            nombre="Estaciones de Trabajo Portátiles",
            costo_base=35000.0,
            cantidad_equipos=3,
            dias=5,
            incluye_seguro=True,
        )
        servicios_disponibles.extend([sala_vip, equipos_dev])
        registrar_evento(f"Servicio creado: {sala_vip.obtener_descripcion()}")
        registrar_evento(f"Servicio creado: {equipos_dev.obtener_descripcion()}")
        print(f"Creado: {sala_vip.obtener_descripcion()}")
        print(f"Creado: {equipos_dev.obtener_descripcion()}\n")
    except ValueError as e:
        registrar_error(f"Error al crear servicios en Operación 4: {e}")
        print(f"Error en Operación 4: {e}\n")

    # OPERACIÓN 5: Creación de servicio tipo Asesoría Especializada
    print("--- Operación 5: Creación de servicio (Asesoría Especializada) ---")
    try:
        asesoria_cloud = AsesoriasEspecializadas(
            id_servicio="SRV-003",
            nombre="Consultoría Arquitectura Cloud",
            costo_base=80000.0,
            horas=3,
            nivel_especialista="Senior",
        )
        servicios_disponibles.append(asesoria_cloud)
        registrar_evento(f"Servicio creado: {asesoria_cloud.obtener_descripcion()}")
        print(f"Creado: {asesoria_cloud.obtener_descripcion()}\n")
    except ValueError as e:
        registrar_error(f"Error al crear asesoría en Operación 5: {e}")
        print(f"Error en Operación 5: {e}\n")

    # -------------------------------------------------------------------------
    # PARTE 2 (INTEGRANTE 3): OPERACIONES 6 A 10
    # Continuar aquí con reservas exitosas, reservas fallidas por no disponibilidad
    # y cálculos de costos con descuentos e impuestos usando `clientes_registrados`
    # y `servicios_disponibles`.
    # -------------------------------------------------------------------------

    registrar_evento("=== FIN DE LAS PRIMERAS 5 OPERACIONES SIMULADAS ===")
    print("============================================================")
    print("   PRIMERAS 5 OPERACIONES FINALIZADAS - REVISAR .LOG        ")
    print("============================================================")


if __name__ == "__main__":
    main()
