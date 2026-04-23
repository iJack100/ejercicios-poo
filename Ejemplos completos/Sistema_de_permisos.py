# ============================================================
#   SISTEMA DE REGISTRO DE PERMISOS DEL PERSONAL
#   Caso de Estudio - POO, CRUD, Mixins, Decoradores, HOF
# ============================================================

from abc import ABC, abstractmethod
from datetime import datetime, date
from functools import reduce
import os

# ──────────────────────────────────────────────
# DECORADORES
# ──────────────────────────────────────────────

def validar_no_vacio(func):
    """Decorador: garantiza que el valor retornado no sea cadena vacía."""
    def wrapper(*args, **kwargs):
        while True:
            valor = func(*args, **kwargs)
            if valor.strip() != "":
                return valor.strip()
            print("  ⚠  El campo no puede estar vacío. Intente de nuevo.")
    return wrapper


def validar_positivo(func):
    """Decorador: garantiza que el valor numérico sea positivo."""
    def wrapper(*args, **kwargs):
        while True:
            try:
                valor = func(*args, **kwargs)
                if valor > 0:
                    return valor
                print("  ⚠  El valor debe ser mayor que cero.")
            except ValueError:
                print("  ⚠  Ingrese un número válido.")
    return wrapper


def log_operacion(func):
    """Decorador: registra en consola cuándo se ejecuta una operación CRUD."""
    def wrapper(*args, **kwargs):
        nombre_op = func.__name__.replace("_", " ").upper()
        print(f"\n  → Ejecutando: {nombre_op}")
        resultado = func(*args, **kwargs)
        return resultado
    return wrapper


# ──────────────────────────────────────────────
# INTERFAZ CRUD ABSTRACTA
# ──────────────────────────────────────────────

class ICrud(ABC):
    @abstractmethod
    def crear(self): pass

    @abstractmethod
    def consultar(self): pass

    @abstractmethod
    def eliminar(self): pass


# ──────────────────────────────────────────────
# MIXIN: Utilidades de presentación
# ──────────────────────────────────────────────

class MixinDisplay:
    """Mixin con helpers de impresión reutilizables."""

    def cabecera(self, titulo: str):
        print("\n" + "=" * 44)
        print(f"  {titulo.center(40)}")
        print("=" * 44)

    def separador(self):
        print("-" * 44)

    def pausa(self):
        input("\n  Presione ENTER para continuar...")


class MixinEstadisticas:
    """Mixin que aporta métodos estadísticos usando HOF."""

    # HOF: filter + len
    def contar_por_condicion(self, lista: list, condicion) -> int:
        return len(list(filter(condicion, lista)))

    # HOF: map + reduce → suma total
    def sumar_campo(self, lista: list, extractor) -> float:
        valores = list(map(extractor, lista))
        return reduce(lambda a, b: a + b, valores, 0.0)

    # HOF: filter → sublista
    def filtrar(self, lista: list, condicion) -> list:
        return list(filter(condicion, lista))


# ──────────────────────────────────────────────
# ENTIDADES (modelos de datos)
# ──────────────────────────────────────────────

class Empleado:
    _contador = 1

    def __init__(self, nombre: str, sueldo: float):
        self.id = Empleado._contador
        Empleado._contador += 1
        self.nombre = nombre
        self.sueldo = sueldo
        self.valor_hora: float = round(sueldo / 240, 4)

    def __str__(self):
        return (f"  [{self.id:03d}] {self.nombre:<25} "
                f"Sueldo: ${self.sueldo:>10.2f}   "
                f"Val/hora: ${self.valor_hora:.4f}")


class TipoPermiso:
    _contador = 1

    def __init__(self, descripcion: str, remunerado: str):
        self.id = TipoPermiso._contador
        TipoPermiso._contador += 1
        self.descripcion = descripcion
        self.remunerado: bool = remunerado.upper() == "S"

    def __str__(self):
        rem = "Sí" if self.remunerado else "No"
        return (f"  [{self.id:03d}] {self.descripcion:<30}  Remunerado: {rem}")


class Permiso:
    _contador = 1

    def __init__(self, id_empleado: int, id_tipo: int,
                 fecha_desde: date, fecha_hasta: date,
                 tipo: str, tiempo: float,
                 descuento: float):
        self.id = Permiso._contador
        Permiso._contador += 1
        self.id_empleado = id_empleado
        self.id_tipo = id_tipo
        self.fecha_desde = fecha_desde
        self.fecha_hasta = fecha_hasta
        self.tipo = tipo.upper()          # D = días, H = horas
        self.tiempo = tiempo
        self.descuento = descuento        # 0 si remunerado

    def __str__(self):
        unidad = "día(s)" if self.tipo == "D" else "hora(s)"
        return (f"  [{self.id:03d}] Emp:{self.id_empleado:03d}  "
                f"Tipo:{self.id_tipo:03d}  "
                f"{self.fecha_desde} → {self.fecha_hasta}  "
                f"{self.tiempo} {unidad}  Desc:${self.descuento:.2f}")


# ──────────────────────────────────────────────
# REPOSITORIOS (almacenamiento en memoria)
# ──────────────────────────────────────────────

class Repositorio:
    """Almacén genérico en memoria."""
    def __init__(self):
        self._datos: list = []

    def agregar(self, entidad):
        self._datos.append(entidad)

    def todos(self) -> list:
        return list(self._datos)

    def buscar_por_id(self, id_: int):
        return next((e for e in self._datos if e.id == id_), None)

    def eliminar_por_id(self, id_: int) -> bool:
        entidad = self.buscar_por_id(id_)
        if entidad:
            self._datos.remove(entidad)
            return True
        return False

    def count(self) -> int:
        return len(self._datos)


# ──────────────────────────────────────────────
# HELPERS DE ENTRADA (con decoradores)
# ──────────────────────────────────────────────

@validar_no_vacio
def pedir_texto(prompt: str) -> str:
    return input(f"  {prompt}: ")


@validar_positivo
def pedir_float(prompt: str) -> float:
    return float(input(f"  {prompt}: "))


def pedir_fecha(prompt: str) -> date:
    while True:
        raw = input(f"  {prompt} (DD/MM/AAAA): ").strip()
        try:
            return datetime.strptime(raw, "%d/%m/%Y").date()
        except ValueError:
            print("  ⚠  Formato de fecha inválido. Use DD/MM/AAAA.")


def pedir_tipo_permiso_dh() -> str:
    while True:
        valor = input("  Tipo (D=Días / H=Horas): ").strip().upper()
        if valor in ("D", "H"):
            return valor
        print("  ⚠  Solo se acepta D o H.")


def pedir_sn(prompt: str) -> str:
    while True:
        valor = input(f"  {prompt} (S/N): ").strip().upper()
        if valor in ("S", "N"):
            return valor
        print("  ⚠  Solo se acepta S o N.")


def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


# ──────────────────────────────────────────────
# CONTROLADORES (heredan ICrud, MixinDisplay)
# ──────────────────────────────────────────────

class ControladorEmpleado(ICrud, MixinDisplay):

    def __init__(self, repo: Repositorio):
        self.repo = repo

    @log_operacion
    def crear(self):
        self.cabecera("REGISTRO DE EMPLEADO")
        print(f"  ID: [GENERADO AUTOMÁTICAMENTE → {Empleado._contador:03d}]")
        self.separador()
        nombre = pedir_texto("Nombre")
        sueldo = pedir_float("Sueldo")
        valor_hora = round(sueldo / 240, 4)
        self.separador()
        print(f"  Valor hora calculado: $ {valor_hora:.4f}")
        self.separador()
        print("  ¿Desea guardar?\n  1. Sí\n  2. No")
        op = input("  Opción: ").strip()
        if op == "1":
            emp = Empleado(nombre, sueldo)
            self.repo.agregar(emp)
            print(f"\n  ✔  Empleado registrado con ID {emp.id:03d}.")
        else:
            print("  ✘  Operación cancelada.")
        self.pausa()

    @log_operacion
    def consultar(self):
        self.cabecera("LISTA DE EMPLEADOS")
        empleados = self.repo.todos()
        if not empleados:
            print("  (No hay empleados registrados)")
        else:
            for e in empleados:
                print(e)
        self.pausa()

    @log_operacion
    def eliminar(self):
        self.cabecera("ELIMINAR EMPLEADO")
        self.consultar()
        try:
            id_ = int(input("  ID a eliminar: "))
            if self.repo.eliminar_por_id(id_):
                print(f"  ✔  Empleado {id_:03d} eliminado.")
            else:
                print("  ⚠  ID no encontrado.")
        except ValueError:
            print("  ⚠  ID inválido.")
        self.pausa()


class ControladorTipoPermiso(ICrud, MixinDisplay):

    def __init__(self, repo: Repositorio):
        self.repo = repo

    @log_operacion
    def crear(self):
        self.cabecera("TIPO DE PERMISO")
        print(f"  ID: [GENERADO AUTOMÁTICAMENTE → {TipoPermiso._contador:03d}]")
        self.separador()
        desc = pedir_texto("Descripción")
        rem  = pedir_sn("¿Remunerado?")
        self.separador()
        print("  ¿Guardar?\n  1. Sí\n  2. No")
        op = input("  Opción: ").strip()
        if op == "1":
            tp = TipoPermiso(desc, rem)
            self.repo.agregar(tp)
            print(f"\n  ✔  Tipo de permiso registrado con ID {tp.id:03d}.")
        else:
            print("  ✘  Operación cancelada.")
        self.pausa()

    @log_operacion
    def consultar(self):
        self.cabecera("TIPOS DE PERMISO")
        tipos = self.repo.todos()
        if not tipos:
            print("  (No hay tipos de permiso registrados)")
        else:
            for t in tipos:
                print(t)
        self.pausa()

    @log_operacion
    def eliminar(self):
        self.cabecera("ELIMINAR TIPO DE PERMISO")
        self.consultar()
        try:
            id_ = int(input("  ID a eliminar: "))
            if self.repo.eliminar_por_id(id_):
                print(f"  ✔  Tipo {id_:03d} eliminado.")
            else:
                print("  ⚠  ID no encontrado.")
        except ValueError:
            print("  ⚠  ID inválido.")
        self.pausa()


class ControladorPermiso(ICrud, MixinDisplay):

    def __init__(self, repo_perm: Repositorio,
                 repo_emp: Repositorio,
                 repo_tipo: Repositorio):
        self.repo      = repo_perm
        self.repo_emp  = repo_emp
        self.repo_tipo = repo_tipo

    # ── helpers internos ──────────────────────

    def _calcular_descuento(self, empleado: Empleado,
                            tipo_permiso: TipoPermiso,
                            tipo_tiempo: str,
                            tiempo: float) -> float:
        """Descuento solo si el permiso NO es remunerado."""
        if tipo_permiso.remunerado:
            return 0.0
        if tipo_tiempo == "H":
            return round(empleado.valor_hora * tiempo, 2)
        else:  # D
            return round(empleado.valor_hora * 8 * tiempo, 2)

    # ── CRUD ──────────────────────────────────

    @log_operacion
    def crear(self):
        self.cabecera("REGISTRO DE PERMISO")
        print(f"  ID: [GENERADO AUTOMÁTICAMENTE → {Permiso._contador:03d}]")
        self.separador()

        # -- Empleado
        try:
            id_emp = int(input("  ID Empleado: "))
        except ValueError:
            print("  ⚠  ID inválido.")
            self.pausa()
            return
        empleado = self.repo_emp.buscar_por_id(id_emp)
        if not empleado:
            print("  ⚠  Empleado no encontrado.")
            self.pausa()
            return

        # -- Tipo permiso
        try:
            id_tipo = int(input("  ID Tipo Permiso: "))
        except ValueError:
            print("  ⚠  ID inválido.")
            self.pausa()
            return
        tipo_p = self.repo_tipo.buscar_por_id(id_tipo)
        if not tipo_p:
            print("  ⚠  Tipo de permiso no encontrado.")
            self.pausa()
            return

        # -- Fechas
        fecha_desde = pedir_fecha("Fecha desde")
        fecha_hasta = pedir_fecha("Fecha hasta")
        if fecha_hasta < fecha_desde:
            print("  ⚠  Fecha hasta no puede ser anterior a fecha desde.")
            self.pausa()
            return

        # -- Tipo y tiempo
        tipo_dt = pedir_tipo_permiso_dh()
        tiempo  = pedir_float("Tiempo (cantidad)")

        # -- Cálculo
        descuento = self._calcular_descuento(empleado, tipo_p, tipo_dt, tiempo)
        rem_texto = "Sí" if tipo_p.remunerado else "No"

        self.separador()
        print(f"  Resumen:")
        print(f"  Empleado      : {empleado.nombre}")
        print(f"  Tipo permiso  : {tipo_p.descripcion}")
        print(f"  ¿Remunerado?  : {rem_texto}")
        print(f"  Descuento     : $ {descuento:.2f}")
        self.separador()
        print("  ¿Confirmar?\n  1. Sí\n  2. No")
        op = input("  Opción: ").strip()
        if op == "1":
            p = Permiso(id_emp, id_tipo, fecha_desde, fecha_hasta,
                        tipo_dt, tiempo, descuento)
            self.repo.agregar(p)
            print(f"\n  ✔  Permiso registrado con ID {p.id:03d}.")
        else:
            print("  ✘  Operación cancelada.")
        self.pausa()

    @log_operacion
    def consultar(self):
        self.cabecera("LISTA DE PERMISOS")
        permisos = self.repo.todos()
        if not permisos:
            print("  (No hay permisos registrados)")
        else:
            for p in permisos:
                emp  = self.repo_emp.buscar_por_id(p.id_empleado)
                tipo = self.repo_tipo.buscar_por_id(p.id_tipo)
                nombre_emp  = emp.nombre if emp else "?"
                nombre_tipo = tipo.descripcion if tipo else "?"
                unidad = "día(s)" if p.tipo == "D" else "hora(s)"
                print(f"  [{p.id:03d}] {nombre_emp:<20} | {nombre_tipo:<20} | "
                      f"{p.fecha_desde}→{p.fecha_hasta} | "
                      f"{p.tiempo} {unidad} | Desc:${p.descuento:.2f}")
        self.pausa()

    @log_operacion
    def eliminar(self):
        self.cabecera("ELIMINAR PERMISO")
        self.consultar()
        try:
            id_ = int(input("  ID a eliminar: "))
            if self.repo.eliminar_por_id(id_):
                print(f"  ✔  Permiso {id_:03d} eliminado.")
            else:
                print("  ⚠  ID no encontrado.")
        except ValueError:
            print("  ⚠  ID inválido.")
        self.pausa()


# ──────────────────────────────────────────────
# MÓDULO DE ESTADÍSTICAS (usa MixinEstadisticas)
# ──────────────────────────────────────────────

class Estadisticas(MixinDisplay, MixinEstadisticas):

    def __init__(self, repo_emp: Repositorio,
                 repo_perm: Repositorio,
                 repo_tipo: Repositorio):
        self.repo_emp  = repo_emp
        self.repo_perm = repo_perm
        self.repo_tipo = repo_tipo

    def _es_remunerado(self, permiso: Permiso) -> bool:
        tipo = self.repo_tipo.buscar_por_id(permiso.id_tipo)
        return tipo.remunerado if tipo else False

    def mostrar(self):
        self.cabecera("ESTADÍSTICAS DE PERMISOS")

        empleados = self.repo_emp.todos()
        permisos  = self.repo_perm.todos()

        # HOF: contar empleados y permisos totales
        total_emp   = len(empleados)
        total_perm  = len(permisos)

        # HOF: filter remunerados / no remunerados
        perm_rem    = self.contar_por_condicion(
                          permisos, lambda p: self._es_remunerado(p))
        perm_no_rem = self.contar_por_condicion(
                          permisos, lambda p: not self._es_remunerado(p))

        # HOF: reduce → suma tiempo
        total_tiempo = self.sumar_campo(permisos, lambda p: p.tiempo)

        # HOF: reduce → suma descuentos
        total_desc   = self.sumar_campo(permisos, lambda p: p.descuento)

        # HOF: map → detalle tiempo por tipo
        dias_  = self.sumar_campo(
                     self.filtrar(permisos, lambda p: p.tipo == "D"),
                     lambda p: p.tiempo)
        horas_ = self.sumar_campo(
                     self.filtrar(permisos, lambda p: p.tipo == "H"),
                     lambda p: p.tiempo)

        self.separador()
        print(f"  Total empleados           : {total_emp}")
        print(f"  Total permisos            : {total_perm}")
        self.separador()
        print(f"  Permisos remunerados      : {perm_rem}")
        print(f"  Permisos no remunerados   : {perm_no_rem}")
        self.separador()
        print(f"  Total días solicitados    : {dias_:.1f}")
        print(f"  Total horas solicitadas   : {horas_:.1f}")
        print(f"  Total tiempo (combinado)  : {total_tiempo:.1f} unidades")
        self.separador()
        print(f"  Monto total descontado    : $ {total_desc:.2f}")
        self.separador()
        self.pausa()


# ──────────────────────────────────────────────
# MENÚ PRINCIPAL
# ──────────────────────────────────────────────

class MenuPrincipal(MixinDisplay):

    def __init__(self):
        # Repositorios compartidos
        self.repo_emp  = Repositorio()
        self.repo_tipo = Repositorio()
        self.repo_perm = Repositorio()

        # Controladores
        self.ctrl_emp  = ControladorEmpleado(self.repo_emp)
        self.ctrl_tipo = ControladorTipoPermiso(self.repo_tipo)
        self.ctrl_perm = ControladorPermiso(
                             self.repo_perm, self.repo_emp, self.repo_tipo)
        self.estadist  = Estadisticas(
                             self.repo_emp, self.repo_perm, self.repo_tipo)

    # ── submenús ──────────────────────────────

    def _menu_empleados(self):
        while True:
            limpiar()
            self.cabecera("GESTIÓN DE EMPLEADOS")
            print("  1. Registrar empleado")
            print("  2. Consultar empleados")
            print("  3. Eliminar empleado")
            print("  0. Volver")
            op = input("\n  Seleccione: ").strip()
            if   op == "1": self.ctrl_emp.crear()
            elif op == "2": self.ctrl_emp.consultar()
            elif op == "3": self.ctrl_emp.eliminar()
            elif op == "0": break
            else: print("  ⚠  Opción inválida.")

    def _menu_tipos(self):
        while True:
            limpiar()
            self.cabecera("GESTIÓN DE TIPOS DE PERMISO")
            print("  1. Registrar tipo de permiso")
            print("  2. Consultar tipos")
            print("  3. Eliminar tipo")
            print("  0. Volver")
            op = input("\n  Seleccione: ").strip()
            if   op == "1": self.ctrl_tipo.crear()
            elif op == "2": self.ctrl_tipo.consultar()
            elif op == "3": self.ctrl_tipo.eliminar()
            elif op == "0": break
            else: print("  ⚠  Opción inválida.")

    def _menu_permisos(self):
        while True:
            limpiar()
            self.cabecera("GESTIÓN DE PERMISOS")
            print("  1. Registrar permiso")
            print("  2. Consultar permisos")
            print("  3. Eliminar permiso")
            print("  0. Volver")
            op = input("\n  Seleccione: ").strip()
            if   op == "1": self.ctrl_perm.crear()
            elif op == "2": self.ctrl_perm.consultar()
            elif op == "3": self.ctrl_perm.eliminar()
            elif op == "0": break
            else: print("  ⚠  Opción inválida.")

    # ── menú raíz ─────────────────────────────

    def ejecutar(self):
        while True:
            limpiar()
            self.cabecera("SISTEMA DE PERMISOS DEL PERSONAL")
            print("  1. Gestión de Empleados")
            print("  2. Gestión de Tipos de Permiso")
            print("  3. Gestión de Permisos")
            print("  4. Estadísticas")
            print("  0. Salir")
            op = input("\n  Seleccione: ").strip()
            if   op == "1": self._menu_empleados()
            elif op == "2": self._menu_tipos()
            elif op == "3": self._menu_permisos()
            elif op == "4": self.estadist.mostrar()
            elif op == "0":
                print("\n  Hasta pronto.\n")
                break
            else:
                print("  ⚠  Opción inválida.")
                self.pausa()


# ──────────────────────────────────────────────
# PUNTO DE ENTRADA
# ──────────────────────────────────────────────

if __name__ == "__main__":
    app = MenuPrincipal()
    app.ejecutar()
