#bsp_package/main.py
import sys

def saludar_usuario():
    if len(sys.argv) != 2:
        print("Uso: hi_user <nombre>")
        sys.exit(1)

    nombre = sys.argv[1]
    print(f"¡Hola, {nombre}! Bienvenido a mi_paquete.")