#bsp_package/main.py
# bsp_package/main.py
import sys

def saludar_usuario(nombre=None):
    if nombre is None:
        if len(sys.argv) != 2:
            print("Uso: hi_user <nombre>")
            sys.exit(1)
        nombre = sys.argv[1]
    
    print(f"¡Hola, {nombre}! Bienvenido a mi_paquete.")

# Llamada principal solo si se ejecuta como script
if __name__ == "__main__":
    saludar_usuario()
