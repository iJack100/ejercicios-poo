# 05_validacion.py
# Ejercicio: Validar tipos y valores de argumentos
# Objetivo: Usar decoradores como capa de validación

import functools
import inspect


def validar_tipos(**tipos_esperados):
    """Valida que los argumentos sean del tipo correcto."""
    def decorador(func):
        @functools.wraps(func) 
        def wrapper(*args, **kwargs):
            # Mapea args posicionales a nombres de parámetros
            parametros = list(inspect.signature(func).parameters.keys())
            todos = dict(zip(parametros, args))
            todos.update(kwargs)

            for nombre, tipo in tipos_esperados.items():
                if nombre in todos and not isinstance(todos[nombre], tipo):
                    raise TypeError(
                        f"'{nombre}' debe ser {tipo.__name__}, "
                        f"recibido {type(todos[nombre]).__name__}"
                    )
            return func(*args, **kwargs)
        return wrapper
    return decorador


def no_nulo(*nombres):
    """Verifica que los argumentos especificados no sean None."""
    def decorador(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            parametros = list(inspect.signature(func).parameters.keys())
            todos = dict(zip(parametros, args))
            todos.update(kwargs)

            for nombre in nombres:
                if todos.get(nombre) is None:
                    raise ValueError(f"El argumento '{nombre}' no puede ser None")
            return func(*args, **kwargs)
        return wrapper
    return decorador


def rango_numerico(nombre, minimo=None, maximo=None):
    """Valida que un argumento numérico esté dentro de un rango."""
    def decorador(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            parametros = list(inspect.signature(func).parameters.keys())
            todos = dict(zip(parametros, args))
            todos.update(kwargs)

            valor = todos.get(nombre)
            if valor is not None:
                if minimo is not None and valor < minimo:
                    raise ValueError(f"'{nombre}' = {valor} es menor que el mínimo {minimo}")
                if maximo is not None and valor > maximo:
                    raise ValueError(f"'{nombre}' = {valor} supera el máximo {maximo}")
            return func(*args, **kwargs)
        return wrapper
    return decorador


# ── Ejemplos ───────────────────────────────────────────────
@validar_tipos(nombre=str, edad=int)
def crear_usuario(nombre, edad):
    return {"nombre": nombre, "edad": edad}


@no_nulo("email")
@validar_tipos(email=str)
def enviar_correo(email, asunto="Sin asunto"):
    return f"Enviado a {email}: '{asunto}'"


@rango_numerico("nota", minimo=0, maximo=10)
def registrar_nota(alumno, nota):
    return f"{alumno}: {nota}/10"


# ── Pruebas ────────────────────────────────────────────────
if __name__ == "__main__":
    print(crear_usuario("Ana", 30))

    try:
        crear_usuario("Luis", "treinta")   # TypeError
    except TypeError as e:
        print(f"TypeError: {e}")

    print(enviar_correo("ana@mail.com", "Hola"))

    try:
        enviar_correo(None)               # ValueError
    except ValueError as e:
        print(f"ValueError: {e}")

    print(registrar_nota("Pedro", 8.5))

    try:
        registrar_nota("Pedro", 11)       # fuera de rango
    except ValueError as e:
        print(f"ValueError: {e}")


# ── Reto ───────────────────────────────────────────────────
# Crea `@longitud(nombre, minimo, maximo)` que valide la
# longitud de un argumento string o lista.
#
# @longitud("contrasena", minimo=8, maximo=20)
# def registrar(usuario, contrasena): ...
