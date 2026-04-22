#abc en minusculas es el modulo base

from abc import ABC, abstractmethod
class InterfazCRUD(ABC):

    @abstractmethod
    def registrar(self):
        pass

    @abstractmethod
    def consultar(self):
        pass

    @abstractmethod
    def eliminar(self):
        pass

class Empleado:
    contador_id = 1

    def init(self, nombre, sueldo):
        self.id = Empleado.contador_id
        Empleado.contador_id += 1

        self.nombre = nombre
        self.sueldo = sueldo
        self.valor_hora = sueldo/240

class TipoPermiso:
    contador_id = 1

    def init(self, descripcion, remunerado):
        self.id = TipoPermiso.contador_id
        TipoPermiso.contador_id += 1

        self.descripcion = descripcion
        self.remunerado = remunerado

class Permiso:
    contador_id = 1

    def init(self, id_empleado, id_tipo_permiso, fecha_desde, fecha_hasta, tipo, tiempo):
        self.id = Permiso.contador_id
        Permiso.contador_id += 1

        self.id_empleado = id_empleado
        self.id_tipo_permiso = id_tipo_permiso
        self.fecha_desde = fecha_desde
        self.fecha_hasta = fecha_hasta
        self.tipo = tipo
        self.tiempo = tiempo