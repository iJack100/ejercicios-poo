class CuentaBancaria:
    def __init__(self, titular, monto):
        self.titular=titular
        self.monto=monto
    
    def depositar(self, monto_a_depositar):
        self.monto+=monto_a_depositar
        print("Deposito Existoso a la cuenta de", self.titular, "Saldo actual: ", self.monto)
    def retirar(self,monto_a_retirar):
        if self.monto < monto_a_retirar:
            print("Saldo insuficinete, saldo actual: ",self.monto)
        else:
            self.monto-=monto_a_retirar
            print("Retiro realizado con exito, saldo actual: ", self.monto)
cuenta_jhoan=CuentaBancaria("Jhoan Cevallos",500)
cuenta_jhoan.depositar(200)
cuenta_jhoan.retirar(1000)
cuenta_jhoan.retirar(600)     

             
        