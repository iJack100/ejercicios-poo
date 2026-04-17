import json
class MixinMedico:
    def curar(self):
        self.salud=self.salud+50
                
class Agente:
    def __init__(self, nombre, edad):
        self.nombre=nombre
        self.edad=edad
        self.salud=100
        self.misiones_exitosas=0
        
class AgentedeElite(MixinMedico, Agente):
    pass

def control_de_riesgo(funcion_evaluar):

    def ver_salud(agente):
        if agente.salud>30:
            funcion_evaluar(agente)
        else:
            print("¡Alerta! Agente demasiado herido para la misión.")
    return ver_salud
@control_de_riesgo
def ir_a_mision(agente):
    agente.salud-=40
    agente.misiones_exitosas+=1
def guardar_reporte(agente):
    reporte={
        "Nombre": agente.nombre,
        "Edad": agente.edad,
        "Salud": agente.salud,
        "Misiones exitosas": agente.misiones_exitosas
    }
    with open("reporte_agente.json", "w") as archivo:
        json.dump(reporte,archivo)

milagrin=AgentedeElite("Milagrin",18)
ir_a_mision(milagrin)
ir_a_mision(milagrin)
ir_a_mision(milagrin)
milagrin.curar()
guardar_reporte(milagrin)

                

