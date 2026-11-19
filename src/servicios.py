from abc import ABC, abstractmethod

# Clase base para todos los servicios
class Servicio(ABC):
    def __init__(self, id_servicio: str, nombre: str, costo_base: float):
        self._id_servicio = id_servicio
        self._nombre = nombre
        self._costo_base = costo_base
        self.validar_parametros()

    @property
    def id_servicio(self) -> str:
        return self._id_servicio

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def costo_base(self) -> float:
        return self._costo_base

    @abstractmethod
    def validar_parametros(self) -> None:
        if not self._id_servicio or not isinstance(self._id_servicio, str):
            raise ValueError("El ID del servicio no puede estar vacío.")
        if not self._nombre or not isinstance(self._nombre, str):
            raise ValueError("El nombre del servicio no es válido.")
        if self._costo_base <= 0:
            raise ValueError("El costo base debe ser mayor a 0.")

    @abstractmethod
    def calcular_costo(self, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        pass

    @abstractmethod
    def obtener_descripcion(self) -> str:
        pass


# Servicio 1: Reserva de salas
class ReservaSalas(Servicio):
    def __init__(self, id_servicio: str, nombre: str, costo_base: float, horas: int, capacidad: int, incluye_catering: bool = False):
        self._horas = horas
        self._capacidad = capacidad
        self._incluye_catering = incluye_catering
        super().__init__(id_servicio, nombre, costo_base)

    @property
    def horas(self) -> int:
        return self._horas

    @property
    def capacidad(self) -> int:
        return self._capacidad

    @property
    def incluye_catering(self) -> bool:
        return self._incluye_catering

    def validar_parametros(self) -> None:
        super().validar_parametros()
        if self._horas <= 0:
            raise ValueError("Las horas deben ser mayores a 0.")
        if self._capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor a 0.")

    def calcular_costo(self, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        subtotal = self._costo_base * self._horas
        
        # recargo por servicio de catering
        if self._incluye_catering:
            subtotal += 50000.0

        desc_monto = subtotal * (descuento / 100.0 if descuento > 1 else descuento)
        total = (subtotal - desc_monto) * (1 + impuesto)
        return round(total, 2)

    def obtener_descripcion(self) -> str:
        catering = "Sí" if self._incluye_catering else "No"
        return f"[Reserva Sala] {self._id_servicio} - {self._nombre} | {self._horas}h | Capacidad: {self._capacidad} p. | Catering: {catering}"


# Servicio 2: Alquiler de equipos
class AlquilerEquipos(Servicio):
    def __init__(self, id_servicio: str, nombre: str, costo_base: float, cantidad_equipos: int, dias: int, incluye_seguro: bool = True):
        self._cantidad_equipos = cantidad_equipos
        self._dias = dias
        self._incluye_seguro = incluye_seguro
        super().__init__(id_servicio, nombre, costo_base)

    @property
    def cantidad_equipos(self) -> int:
        return self._cantidad_equipos

    @property
    def dias(self) -> int:
        return self._dias

    @property
    def incluye_seguro(self) -> bool:
        return self._incluye_seguro

    def validar_parametros(self) -> None:
        super().validar_parametros()
        if self._cantidad_equipos <= 0:
            raise ValueError("La cantidad de equipos debe ser mayor a 0.")
        if self._dias <= 0:
            raise ValueError("Los días de alquiler deben ser mayores a 0.")

    def calcular_costo(self, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        subtotal = self._costo_base * self._cantidad_equipos * self._dias
        
        # 10% de descuento si alquila 5 días o más
        desc_aplicado = descuento
        if self._dias >= 5 and descuento == 0.0:
            desc_aplicado = 10.0

        # seguro por equipo
        if self._incluye_seguro:
            subtotal += (15000.0 * self._cantidad_equipos)

        desc_monto = subtotal * (desc_aplicado / 100.0 if desc_aplicado > 1 else desc_aplicado)
        total = (subtotal - desc_monto) * (1 + impuesto)
        return round(total, 2)

    def obtener_descripcion(self) -> str:
        seguro = "Sí" if self._incluye_seguro else "No"
        return f"[Alquiler Equipos] {self._id_servicio} - {self._nombre} | Cant: {self._cantidad_equipos} | Días: {self._dias} | Seguro: {seguro}"


# Servicio 3: Asesorías especializadas
class AsesoriasEspecializadas(Servicio):
    NIVELES = {"Junior": 1.0, "Senior": 1.5, "Master": 2.0}

    def __init__(self, id_servicio: str, nombre: str, costo_base: float, horas: int, nivel_especialista: str = "Senior"):
        self._horas = horas
        self._nivel_especialista = nivel_especialista.capitalize()
        super().__init__(id_servicio, nombre, costo_base)

    @property
    def horas(self) -> int:
        return self._horas

    @property
    def nivel_especialista(self) -> str:
        return self._nivel_especialista

    def validar_parametros(self) -> None:
        super().validar_parametros()
        if self._horas <= 0:
            raise ValueError("Las horas deben ser mayores a 0.")
        if self._nivel_especialista not in self.NIVELES:
            raise ValueError(f"El nivel debe ser uno de los siguientes: {list(self.NIVELES.keys())}")

    def calcular_costo(self, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        tarifa = self._costo_base * self.NIVELES[self._nivel_especialista]
        subtotal = tarifa * self._horas

        desc_monto = subtotal * (descuento / 100.0 if descuento > 1 else descuento)
        total = (subtotal - desc_monto) * (1 + impuesto)
        return round(total, 2)

    def obtener_descripcion(self) -> str:
        return f"[Asesoría] {self._id_servicio} - {self._nombre} | Nivel: {self._nivel_especialista} | Horas: {self._horas}"


# Pruebas sencillas en consola
if __name__ == "__main__":
    s1 = ReservaSalas("SRV-001", "Sala de Juntas", 45000.0, horas=4, capacidad=10, incluye_catering=True)
    s2 = AlquilerEquipos("SRV-002", "Laptops Dev", 35000.0, cantidad_equipos=3, dias=6, incluye_seguro=True)
    s3 = AsesoriasEspecializadas("SRV-003", "Consultoría Cloud", 80000.0, horas=5, nivel_especialista="Master")

    for servicio in [s1, s2, s3]:
        print(servicio.obtener_descripcion())
        print(f"Total a pagar con IVA: ${servicio.calcular_costo():,.2f}\n")
