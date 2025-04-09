"""
Punto de entrada para el reproductor de música.

Este módulo inicializa la aplicación PyQt5 y muestra la ventana principal.
"""

import sys
from PyQt5.QtWidgets import QApplication

from ui.main_window import MainWindow


def main():
    """
    Función principal que inicia la aplicación.
    """
    # Crear la aplicación Qt
    app = QApplication(sys.argv)
    
    # Establecer el nombre de la aplicación (para configuraciones)
    app.setApplicationName("Reproductor de Música")
    
    # Crear y mostrar la ventana principal
    window = MainWindow()
    window.show()
    
    # Ejecutar el bucle de eventos
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
