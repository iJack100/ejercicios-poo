import datetime
class Empleado:
    def __init__(self, nombre, puesto):
        self.nombre=nombre
        self.puesto=puesto
class MixinAuditoria:
    def regsitrar_accion(self, accion):
        hora_actual=datetime.datetime.now().strftime("%H:%M:%S")
        print("AUDITORIA: ", hora_actual, " - ", self.nombre, "Subio: " ,accion )

class RegistrarAuditoria(Empleado, MixinAuditoria):
    def trabajar(self):
        self.regsitrar_accion("Subiendo commit")
        print(self.nombre, "ha empujado el codigo al repositorio")
trabajdor=RegistrarAuditoria("Jhoan", "Desarollador web")
trabajdor.regsitrar_accion("Creando el archivo de la cuenta bancaria")
trabajdor.regsitrar_accion("Arreglando el bug del signo mayor que")
