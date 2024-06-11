from setuptools import setup, find_packages

setup(
    name='bsp_pypi',                     # Nombre del paquete
    version='0.1',                # Versión del paquete
    packages=find_packages(),       # Encuentra automáticamente los subpaquetes
    install_requires=[              # Lista de dependencias
        # package requirements go here
    ],
    entry_points={                  # Puntos de entrada para los scripts de consola
        'console_scripts': [
            'hi_user=bsp_pypi:saludar_usuario'  # Comando CLI 'hi_user' llama a la función 'saludar_usuario' en 'bsp_pypi'
        ]
    },
    
    # metadata for upload to PyPI
)