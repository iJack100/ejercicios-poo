from abc import ABC, abstractmethod
from datetime import datetime
import functools

# ==========================================================
# 1. DECORADORES
# ==========================================================
def decorador_interfaz(titulo):
    """Decorador para dar formato a los encabezados de las interfaces."""
    def wrapper(func):
        def inner(*args, **kwargs):
            print("=" * 40)
            print(f"{titulo.center(40)}")
            print("=" * 40)
            res = func(*args, **kwargs)
            return res
        return inner
    return wrapper

# ==========================================================
# 2. MIXINS
# ==========================================================
class CalculosMixin:
    """Mixin para proveer funcionalidades de cálculo y validación."""
    def validar_fecha(self, fecha_str):
        try:
            return datetime.strptime(fecha_str, "%d/%m/%Y")
        except ValueError:
            return None

    def calcular_descuento(self, tipo, tiempo, valor_hora, remunerado):
        if remunerado == 'S':
            return 0.0
        # Si es por día (D), se asumen 8 horas laborables por día
        factor = 8 if tipo == 'D' else 1
        return round(float(tiempo) * factor * valor_hora, 2)

# ==========================================================
# 3. INTERFACES (CLASES ABSTRACTAS)
# ==========================================================
class ICrud(ABC):
    @abstractmethod
    def crear(self): pass
    
    @abstractmethod
    def consultar(self): pass

# ==========================================================
# 4. ENTIDADES
# ==========================================================
class Empleado:
    secuencia = 0
    def __init__(self, nombre, sueldo):
        Empleado.secuencia += 1
        self.id = Empleado.secuencia
        self.nombre = nombre
        self.sueldo = float(sueldo)
        self.valor_hora = round(self.sueldo / 240, 2)

class TipoPermiso:
    secuencia = 0
    def __init__(self, descripcion, remunerado):
        TipoPermiso.secuencia += 1
        self.id = TipoPermiso.secuencia
        self.descripcion = descripcion
        self.remunerado = remunerado.upper() # S o N

class Permiso:
    secuencia = 0
    def __init__(self, emp_id, tipo_id, f_desde, f_hasta, tipo_dh, tiempo, descuento):
        Permiso.secuencia += 1
        self.id = Permiso.secuencia
        self.id_empleado = emp_id
        self.id_tipo_permiso = tipo_id
        self.fecha_desde = f_desde
        self.fecha_hasta = f_hasta
        self.tipo = tipo_dh.upper() # D o H
        self.tiempo = float(tiempo)
        self.descuento = descuento

# ==========================================================
# 5. CORE DEL SISTEMA (LÓGICA Y CRUD)
# ==========================================================
class SistemaGestion(ICrud, CalculosMixin):
    def __init__(self):
        self.empleados = []
        self.tipos_permisos = []
        self.permisos = []

    @decorador_interfaz("REGISTRO DE EMPLEADO")
    def crear_empleado(self):
        print(f"ID: {Empleado.secuencia + 1}")
        nombre = input("Nombre: ")
        sueldo = float(input("Sueldo: "))
        temp_emp = Empleado(nombre, sueldo)
        print("-" * 40)
        print(f"Valor hora calculado: $ {temp_emp.valor_hora}")
        print("-" * 40)
        
        if input("¿Desea guardar? (1. Sí / 2. No): ") == "1":
            self.empleados.append(temp_emp)
            print("Empleado guardado con éxito.")

    @decorador_interfaz("TIPO DE PERMISO")
    def crear_tipo_permiso(self):
        print(f"ID: {TipoPermiso.secuencia + 1}")
        desc = input("Descripción: ")
        remu = input("¿Remunerado? (S/N): ").upper()
        
        if input("¿Guardar? (1. Sí / 2. No): ") == "1":
            self.tipos_permisos.append(TipoPermiso(desc, remu))
            print("Tipo de permiso registrado.")

    @decorador_interfaz("REGISTRO DE PERMISO")
    def crear_permiso(self):
        try:
            emp_id = int(input("ID Empleado: "))
            tipo_id = int(input("ID Tipo Permiso: "))
            
            # Buscar objetos relacionados
            emp = next((e for e in self.empleados if e.id == emp_id), None)
            tp = next((t for t in self.tipos_permisos if t.id == tipo_id), None)
            
            if not emp or not tp:
                print("Error: Empleado o Tipo de Permiso no existe.")
                return

            f_desde = input("Fecha desde (DD/MM/YYYY): ")
            f_hasta = input("Fecha hasta (DD/MM/YYYY): ")
            t_dh = input("Tipo (D/H): ").upper()
            tiempo = float(input("Tiempo (cantidad): "))
            
            descuento = self.calcular_descuento(t_dh, tiempo, emp.valor_hora, tp.remunerado)
            
            print("-" * 40)
            print("Resumen:")
            print(f"¿Remunerado?: {tp.remunerado}")
            print(f"Descuento aplicado: $ {descuento}")
            print("-" * 40)
            
            if input("¿Confirmar? (1. Sí / 2. No): ") == "1":
                nuevo_p = Permiso(emp_id, tipo_id, f_desde, f_hasta, t_dh, tiempo, descuento)
                self.permisos.append(nuevo_p)
                print("Permiso registrado correctamente.")
        except ValueError:
            print("Dato inválido introducido.")

    @decorador_interfaz("ESTADÍSTICAS DE PERMISOS")
    def generar_estadisticas(self):
        # Uso de Funciones de Orden Superior (HOF)
        total_emp = len(self.empleados)
        total_per = len(self.permisos)
        
        # Filtros con HOF
        remu = list(filter(lambda x: next(t.remunerado for t in self.tipos_permisos if t.id == x.id_tipo_permiso) == 'S', self.permisos))
        no_remu = list(filter(lambda x: next(t.remunerado for t in self.tipos_permisos if t.id == x.id_tipo_permiso) == 'N', self.permisos))
        
        # Reducción/Suma con HOF
        total_tiempo = functools.reduce(lambda a, b: a + b.tiempo, self.permisos, 0)
        total_descuentos = sum(map(lambda x: x.descuento, self.permisos))

        print(f"Total empleados: {total_emp}")
        print(f"Total permisos: {total_per}")
        print(f"Permisos remunerados: {len(remu)}")
        print(f"Permisos no remunerados: {len(no_remu)}")
        print(f"Total horas/días solicitados: {total_tiempo}")
        print(f"Monto total descontado: $ {total_descuentos:.2f}")

    # Implementación obligatoria de ICrud
    def crear(self): pass
    def consultar(self):
        print("\n--- Listado de Empleados ---")
        for e in self.empleados: print(f"ID: {e.id} | {e.nombre} | Sueldo: {e.sueldo}")
        print("\n--- Listado de Tipos ---")
        for t in self.tipos_permisos: print(f"ID: {t.id} | {t.descripcion} | Remu: {t.remunerado}")

# ==========================================================
# 6. MENÚ PRINCIPAL
# ==========================================================
def menu():
    sistema = SistemaGestion()
    while True:
        print("\n" + "="*40)
        print("SISTEMA DE GESTIÓN DE PERMISOS".center(40))
        print("="*40)
        print("1. Registrar Empleado")
        print("2. Registrar Tipo de Permiso")
        print("3. Registrar Permiso")
        print("4. Consultar Registros")
        print("5. Estadísticas")
        print("6. Salir")
        opc = input("Seleccione una opción: ")

        if opc == "1": sistema.crear_empleado()
        elif opc == "2": sistema.crear_tipo_permiso()
        elif opc == "3": sistema.crear_permiso()
        elif opc == "4": sistema.consultar()
        elif opc == "5": sistema.generar_estadisticas()
        elif opc == "6": break
        else: print("Opción no válida.")

if __name__ == "__main__":
    menu()