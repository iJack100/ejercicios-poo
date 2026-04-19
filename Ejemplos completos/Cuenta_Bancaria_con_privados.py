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
            self._saldo__inicial-=saldo_a_retirar
            print(f"Retiro realizado su saldo actual es {self.__saldo_inicial} por falta de fondos")

    
    def versaldo(self):
        print(f"Saldo en la cuenta de {self.nombre} es {self.__saldo_inicial}")

             
def guardarcuentas (cuenta):
    cuentasidc={
        "Nombre dle Titualar": cuenta.nombre,
        "Saldo Actial": cuenta.saldo
     }
    with open("cuentas_y_saldos.json","w") as archivo:
            json.dump(cuentasidc, archivo, indent=4)




cuenta_jhoan = Cuenta_Bancaria("Jhoan", 500)
cuenta_jhoan._saldo_inicial=100000
cuenta_jhoan.retiro(800)


guardarcuentas(cuenta_jhoan)