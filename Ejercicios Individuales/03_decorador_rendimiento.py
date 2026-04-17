import time
def medir_tiempo(funcion_original):
    def calcular_tiempo(*args):
        inicio=time.time()
        funcion_original(*args)
        fin=time.time()
        print(f"⏱️ Tiempo total: {fin - inicio:.2f} segundos.")
    return calcular_tiempo
@medir_tiempo
def descargar_archivo(nombre_archivo):
    print("Descargando:" ,nombre_archivo, "....")
    time.sleep(3)
    print("Descarga completada")


@medir_tiempo
def procesar_pago(usuario, cantidad):
    print(f"💳 Procesando pago de {usuario} por ${cantidad}...")
    time.sleep(1)
    print("✅ Pago aprobado.")
    
descargar_archivo("Tesis.pdf") 
print("-" * 30) # 
procesar_pago("Jhoan", 500)