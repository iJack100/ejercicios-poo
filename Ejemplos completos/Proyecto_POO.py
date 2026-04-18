import json
from functools import reduce


def manejar_errores(func):
    """
    DECORADOR:
    Envuelve métodos del sistema para capturar errores
    sin romper el programa.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(f"Error de valor: {e}")
        except FileNotFoundError as e:
            print(f"Error de archivo: {e}")
        except Exception as e:
            print(f"Error inesperado: {type(e).__name__} - {e}")
    return wrapper


class SistemaEstudiantes:
    """
    PROYECTO FINAL:
    Sistema de gestión de estudiantes.

    CONCEPTOS INTEGRADOS:
    - constructor
    - listas
    - diccionarios
    - funciones
    - excepciones
    - archivos JSON
    - decoradores
    - funciones de orden superior
    """

    def __init__(self, archivo="estudiantes.json"):
        """
        CONSTRUCTOR:
        Se ejecuta automáticamente al crear el objeto.
        Inicializa variables importantes del sistema.
        """
        self.archivo = archivo
        self.estudiantes = []
        self.cargar_datos()

    # =========================================================
    # VALIDACIONES
    # =========================================================
    def validar_cedula(self, cedula):
        """
        Valida que la cédula tenga solo dígitos y longitud válida.
        """
        if not cedula.isdigit():
            raise ValueError("La cédula debe contener solo números")
        if len(cedula) < 8:
            raise ValueError("La cédula debe tener al menos 8 dígitos")

    def validar_nota(self, nota):
        """
        Valida que la nota esté en rango 0 a 10.
        """
        if nota < 0 or nota > 10:
            raise ValueError("La nota debe estar entre 0 y 10")

    # =========================================================
    # ARCHIVOS JSON
    # =========================================================
    @manejar_errores
    def guardar_datos(self):
        """
        Guarda la lista de estudiantes en archivo JSON.
        """
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(self.estudiantes, f, indent=4, ensure_ascii=False)
        print("Datos guardados correctamente.")

    @manejar_errores
    def cargar_datos(self):
        """
        Carga los estudiantes desde JSON.
        Si el archivo no existe, inicia con lista vacía.
        """
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                self.estudiantes = json.load(f)
            print("Datos cargados correctamente.")
        except FileNotFoundError:
            self.estudiantes = []
            print("No existe archivo previo. Se inicia con lista vacía.")

    # =========================================================
    # FUNCIONES PRINCIPALES
    # =========================================================
    @manejar_errores
    def registrar_estudiante(self):
        """
        Registra un estudiante usando entrada por teclado.

        CONCEPTOS:
        - input
        - casting
        - listas
        - diccionarios
        - conjuntos
        """
        print("\n=== REGISTRAR ESTUDIANTE ===")

        cedula = input("Cédula: ").strip()
        self.validar_cedula(cedula)

        if self.buscar_estudiante_por_cedula(cedula, mostrar=False):
            raise ValueError("Ya existe un estudiante con esa cédula")

        nombre = input("Nombre: ").strip().title()
        edad = int(input("Edad: "))
        carrera = input("Carrera: ").strip().title()

        materias_texto = input("Materias separadas por coma: ").strip()
        materias_lista = [m.strip().title() for m in materias_texto.split(",") if m.strip()]

        # CONJUNTOS: eliminar duplicados
        materias_sin_duplicados = list(set(materias_lista))

        notas = []
        for materia in materias_sin_duplicados:
            nota = float(input(f"Ingrese nota de {materia}: "))
            self.validar_nota(nota)
            notas.append({"materia": materia, "nota": nota})

        estudiante = {
            "cedula": cedula,
            "nombre": nombre,
            "edad": edad,
            "carrera": carrera,
            "notas": notas
        }

        self.estudiantes.append(estudiante)
        print("Estudiante registrado correctamente.")
        self.guardar_datos()

    @manejar_errores
    def listar_estudiantes(self):
        """
        Lista todos los estudiantes.

        CONCEPTOS:
        - bucles
        - enumerate
        - diccionarios
        """
        print("\n=== LISTA DE ESTUDIANTES ===")

        if not self.estudiantes:
            print("No hay estudiantes registrados.")
            return

        for i, estudiante in enumerate(self.estudiantes, start=1):
            print(f"\nEstudiante #{i}")
            print(f"Cédula: {estudiante['cedula']}")
            print(f"Nombre: {estudiante['nombre']}")
            print(f"Edad: {estudiante['edad']}")
            print(f"Carrera: {estudiante['carrera']}")

            print("Notas:")
            for detalle in estudiante["notas"]:
                print(f" - {detalle['materia']}: {detalle['nota']}")

    def buscar_estudiante_por_cedula(self, cedula, mostrar=True):
        """
        Busca estudiante por cédula.

        CONCEPTOS:
        - bucle for
        - condicionales
        - retorno
        """
        for estudiante in self.estudiantes:
            if estudiante["cedula"] == cedula:
                if mostrar:
                    print("\n=== ESTUDIANTE ENCONTRADO ===")
                    print(estudiante)
                return estudiante
        if mostrar:
            print("Estudiante no encontrado.")
        return None

    @manejar_errores
    def buscar_estudiante(self):
        """
        Solicita cédula y busca estudiante.
        """
        print("\n=== BUSCAR ESTUDIANTE ===")
        cedula = input("Ingrese la cédula: ").strip()
        self.validar_cedula(cedula)
        self.buscar_estudiante_por_cedula(cedula)

    @manejar_errores
    def actualizar_nota(self):
        """
        Actualiza la nota de una materia de un estudiante.
        """
        print("\n=== ACTUALIZAR NOTA ===")
        cedula = input("Ingrese cédula del estudiante: ").strip()
        self.validar_cedula(cedula)

        estudiante = self.buscar_estudiante_por_cedula(cedula, mostrar=False)
        if not estudiante:
            raise ValueError("Estudiante no encontrado")

        materia_buscar = input("Materia a actualizar: ").strip().title()

        for detalle in estudiante["notas"]:
            if detalle["materia"] == materia_buscar:
                nueva_nota = float(input("Nueva nota: "))
                self.validar_nota(nueva_nota)
                detalle["nota"] = nueva_nota
                print("Nota actualizada correctamente.")
                self.guardar_datos()
                return

        print("La materia no existe para ese estudiante.")

    # =========================================================
    # FUNCIONES DE CÁLCULO
    # =========================================================
    def calcular_promedio_estudiante(self, estudiante):
        """
        Calcula promedio de un estudiante.

        CONCEPTOS:
        - funciones
        - listas
        - map
        - reduce
        """
        if not estudiante["notas"]:
            return 0

        notas = list(map(lambda x: x["nota"], estudiante["notas"]))
        suma = reduce(lambda a, b: a + b, notas)
        promedio = suma / len(notas)
        return round(promedio, 2)

    def obtener_estado_academico(self, promedio):
        """
        Determina el estado académico.
        """
        if promedio >= 7:
            return "Aprobado"
        elif promedio >= 5:
            return "Supletorio"
        else:
            return "Reprobado"

    @manejar_errores
    def mostrar_promedio_estudiante(self):
        """
        Busca estudiante y muestra promedio y estado.
        """
        print("\n=== PROMEDIO DE ESTUDIANTE ===")
        cedula = input("Ingrese cédula: ").strip()
        self.validar_cedula(cedula)

        estudiante = self.buscar_estudiante_por_cedula(cedula, mostrar=False)
        if not estudiante:
            raise ValueError("Estudiante no encontrado")

        promedio = self.calcular_promedio_estudiante(estudiante)
        estado = self.obtener_estado_academico(promedio)

        print(f"Nombre: {estudiante['nombre']}")
        print(f"Promedio: {promedio}")
        print(f"Estado: {estado}")

    # =========================================================
    # FUNCIONES DE ORDEN SUPERIOR
    # =========================================================
    @manejar_errores
    def mostrar_aprobados(self):
        """
        Muestra solo estudiantes aprobados.

        CONCEPTOS:
        - filter
        - lambda
        """
        print("\n=== ESTUDIANTES APROBADOS ===")

        aprobados = list(filter(
            lambda e: self.calcular_promedio_estudiante(e) >= 7,
            self.estudiantes
        ))

        if not aprobados:
            print("No hay estudiantes aprobados.")
            return

        for estudiante in aprobados:
            promedio = self.calcular_promedio_estudiante(estudiante)
            print(f"{estudiante['nombre']} - Promedio: {promedio}")

    @manejar_errores
    def mostrar_resumen_promedios(self):
        """
        Muestra una lista de tuplas con nombre y promedio.

        CONCEPTOS:
        - map
        - tuplas
        - unpacking
        """
        print("\n=== RESUMEN DE PROMEDIOS ===")

        resumen = list(map(
            lambda e: (e["nombre"], self.calcular_promedio_estudiante(e)),
            self.estudiantes
        ))

        for nombre, promedio in resumen:
            print(f"{nombre}: {promedio}")

    # =========================================================
    # ELIMINAR ESTUDIANTE
    # =========================================================
    @manejar_errores
    def eliminar_estudiante(self):
        """
        Elimina estudiante por cédula.
        """
        print("\n=== ELIMINAR ESTUDIANTE ===")
        cedula = input("Ingrese cédula: ").strip()
        self.validar_cedula(cedula)

        for i, estudiante in enumerate(self.estudiantes):
            if estudiante["cedula"] == cedula:
                eliminado = self.estudiantes.pop(i)
                print(f"Estudiante eliminado: {eliminado['nombre']}")
                self.guardar_datos()
                return

        print("No se encontró el estudiante.")

    # =========================================================
    # ESTADÍSTICAS
    # =========================================================
    @manejar_errores
    def mostrar_estadisticas(self):
        """
        Muestra estadísticas del sistema.

        CONCEPTOS:
        - listas
        - map
        - filter
        - reduce
        - conjuntos
        """
        print("\n=== ESTADÍSTICAS ===")

        if not self.estudiantes:
            print("No hay datos registrados.")
            return

        promedios = list(map(self.calcular_promedio_estudiante, self.estudiantes))
        promedio_general = round(sum(promedios) / len(promedios), 2)

        aprobados = list(filter(lambda p: p >= 7, promedios))
        reprobados = list(filter(lambda p: p < 5, promedios))

        carreras = set(map(lambda e: e["carrera"], self.estudiantes))

        print(f"Total estudiantes: {len(self.estudiantes)}")
        print(f"Promedio general: {promedio_general}")
        print(f"Aprobados: {len(aprobados)}")
        print(f"Reprobados: {len(reprobados)}")
        print(f"Carreras registradas: {carreras}")

    # =========================================================
    # MENÚ
    # =========================================================
    def menu(self):
        """
        Menú principal del sistema.

        CONCEPTOS:
        - while
        - condicionales
        - control de flujo
        """
        while True:
            print("\n" + "=" * 50)
            print(" SISTEMA DE GESTIÓN DE ESTUDIANTES ")
            print("=" * 50)
            print("1. Registrar estudiante")
            print("2. Listar estudiantes")
            print("3. Buscar estudiante")
            print("4. Actualizar nota")
            print("5. Mostrar promedio de estudiante")
            print("6. Mostrar aprobados")
            print("7. Mostrar resumen de promedios")
            print("8. Eliminar estudiante")
            print("9. Mostrar estadísticas")
            print("10. Guardar datos")
            print("0. Salir")

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.registrar_estudiante()
            elif opcion == "2":
                self.listar_estudiantes()
            elif opcion == "3":
                self.buscar_estudiante()
            elif opcion == "4":
                self.actualizar_nota()
            elif opcion == "5":
                self.mostrar_promedio_estudiante()
            elif opcion == "6":
                self.mostrar_aprobados()
            elif opcion == "7":
                self.mostrar_resumen_promedios()
            elif opcion == "8":
                self.eliminar_estudiante()
            elif opcion == "9":
                self.mostrar_estadisticas()
            elif opcion == "10":
                self.guardar_datos()
            elif opcion == "0":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción inválida. Intente nuevamente.")


# =========================================================
# INSTANCIA Y EJECUCIÓN
# =========================================================
sistema = SistemaEstudiantes()
sistema.menu()