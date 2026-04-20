import json
def validar_monto_positivo(funcion):
    def envoltorio(self, monto):
        if monto <= 0:
            print("Tiene que ser un monto valido")
            raise ValueError("Tiene que ser un monto valido papi")
        
        else:
            return funcion(self, monto)
    return envoltorio

class Cuenta_Bancaria:
    def __init__(self, nombre,saldo_inicial):
        self.nombre=nombre
        self.__saldo_inicial=saldo_inicial
        
    @property
    def saldo(self):
        return self.__saldo_inicial
        
    @validar_monto_positivo
    def depostiar (self, monto_depos):
        self.__saldo_inicial+=monto_depos
        print(f"Depostio a la cuenta de {self.nombre} relizado con exito saldo actual: {self.__saldo_inicial}")
    
    @validar_monto_positivo
    def retiro(self,saldo_a_retirar):
        if self.__saldo_inicial<saldo_a_retirar:
            print(f"Retiro cancelado por falta de fondos")
        else:
            self.__saldo_inicial-=saldo_a_retirar
            print(f"Retiro realizado su saldo actual es {self.__saldo_inicial} ")

    
    def versaldo(self):
        print(f"Saldo en la cuenta de {self.nombre} es {self.__saldo_inicial}")

             
def guardarcuentas (cuenta):
    nombre_archivo = "cuentas_y_saldos.json"
    try:
        with open(nombre_archivo, "r") as archivo:
            historial_cuentas=json.load(archivo)
    except FileNotFoundError:
        historial_cuentas = {}
    
    historial_cuentas[cuenta.nombre] = {
        "Saldo": cuenta.saldo
    }
    
    with open(nombre_archivo, "w") as archivo:
        json.dump(historial_cuentas, archivo, indent=4)
        print(f"Datos de {cuenta.nombre} guradado correctamente ")


def ver_vuentas():
    try:
        nombre_archivo = "cuentas_y_saldos.json"
        with open(nombre_archivo, "r") as archivo:
            historial=json.load(archivo)
            print("\n--- LISTA DE CUENTAS EN EL BANCO ---")
            for nombre, datos in historial.items():
                print(f"Nombre: {nombre} | Saldo: {datos['Saldo']}")
    except FileNotFoundError:
        print ("Aún no hay cuentas registradas en el sistema.")
        
        

cuenta_jhoan = Cuenta_Bancaria("Jhoan", 500)
cuenta_jhoan.retiro(100) 
guardarcuentas(cuenta_jhoan)

cuenta_papa = Cuenta_Bancaria("Papa", 2000)
cuenta_papa.depostiar(500) 
guardarcuentas(cuenta_papa)

# Llamamos a la función para ver toda la base de datos
ver_vuentas()