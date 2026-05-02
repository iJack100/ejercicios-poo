# property_getters_setters.py
# Ejercicio: @property, getter y setter en Python
# Objetivo: Encapsular atributos con lógica de validación elegante


class Temperatura:
    """
    Representa una temperatura con conversión y validación automática.

    Internamente guarda los grados en Celsius, pero expone
    propiedades para leer/escribir en Celsius, Fahrenheit y Kelvin.
    """

    CERO_ABSOLUTO = -273.15  # °C

    def __init__(self, celsius: float = 0.0):
        self.celsius = celsius  # usa el setter → valida desde el inicio

    # ── Celsius ───────────────────────────────────────────
    @property
    def celsius(self) -> float:
        """Temperatura en grados Celsius."""
        return self._celsius

    @celsius.setter
    def celsius(self, valor: float):
        if not isinstance(valor, (int, float)):
            raise TypeError(f"Se esperaba un número, recibido {type(valor).__name__}")
        if valor < self.CERO_ABSOLUTO:
            raise ValueError(
                f"{valor}°C es menor que el cero absoluto ({self.CERO_ABSOLUTO}°C)"
            )
        self._celsius = float(valor)

    # ── Fahrenheit ────────────────────────────────────────
    @property
    def fahrenheit(self) -> float:
        """Temperatura en grados Fahrenheit."""
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, valor: float):
        self.celsius = (valor - 32) * 5 / 9   # reutiliza la validación de celsius

    # ── Kelvin ────────────────────────────────────────────
    @property
    def kelvin(self) -> float:
        """Temperatura en Kelvin."""
        return self._celsius - self.CERO_ABSOLUTO

    @kelvin.setter
    def kelvin(self, valor: float):
        if valor < 0:
            raise ValueError(f"Kelvin no puede ser negativo: {valor}")
        self.celsius = valor + self.CERO_ABSOLUTO

    # ── Representación ────────────────────────────────────
    def __repr__(self):
        return (
            f"Temperatura("
            f"{self.celsius:.2f}°C | "
            f"{self.fahrenheit:.2f}°F | "
            f"{self.kelvin:.2f}K)"
        )


# ── Pruebas ───────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Creación y lectura ===")
    t = Temperatura(100)
    print(t)                              # 100°C | 212°F | 373.15K

    print("\n=== Escribir por Fahrenheit ===")
    t.fahrenheit = 32
    print(t)                              # 0°C | 32°F | 273.15K

    print("\n=== Escribir por Kelvin ===")
    t.kelvin = 0
    print(t)                              # -273.15°C | -459.67°F | 0K

    print("\n=== Validaciones ===")
    try:
        t.celsius = -300                  # bajo el cero absoluto
    except ValueError as e:
        print(f"ValueError: {e}")

    try:
        t.celsius = "caliente"            # tipo incorrecto
    except TypeError as e:
        print(f"TypeError: {e}")

    try:
        t.kelvin = -1                     # Kelvin negativo
    except ValueError as e:
        print(f"ValueError: {e}")


# ── Reto ──────────────────────────────────────────────────
# Añade a la clase:
#
# 1. Una propiedad `descripcion` (solo lectura, sin setter) que devuelva
#    un string descriptivo según el valor:
#    < 0°C  → "bajo cero"
#    0–20   → "frío"
#    21–36  → "templado"
#    > 36   → "caliente"
#
# 2. Un `@celsius.deleter` que resetee la temperatura a 0°C.
#
# Ejemplo esperado:
#   t = Temperatura(25)
#   print(t.descripcion)   # → "templado"
#   del t.celsius
#   print(t.celsius)       # → 0.0
