import json
import os 

def guardar_datos(lista_productos):
    with open("inventario_tienda.json", "w") as archivo:
        json.dump(lista_productos, archivo, indent=4)
    print("\n💾 [SISTEMA]: Datos guardados con éxito en 'inventario_tienda.json'.")

def cargar_datos():

    if os.path.exists("inventario_tienda.json"):
        with open("inventario_tienda.json", "r") as archivo:
            datos = json.load(archivo)
            print("\n📂 [SISTEMA]: Datos recuperados del disco duro.")
            return datos
    else:
        print("\n⚠️ [SISTEMA]: No se encontró base de datos. Creando una nueva...")
        return []

# --- INCIA---

inventario = cargar_datos()

if not inventario:
    print("🛒 Registrando productos iniciales...")
    inventario = [
        {"item": "Laptop Pro", "precio": 2500, "stock": 10},
        {"item": "Monitor 4K", "precio": 500, "stock": 15},
        {"item": "Mouse Inalámbrico", "precio": 50, "stock": 30}
    ]
    guardar_datos(inventario)

print("\n=== INVENTARIO DE LA TIENDA ===")
for p in inventario:
    print(f"📦 Producto: {p['item']}")
    print(f"   💰 Precio: ${p['precio']}")
    print(f"   🔢 Stock: {p['stock']} unidades")
    print("-" * 25)