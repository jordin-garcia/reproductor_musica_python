"""
Paquete que contiene los componentes de la interfaz gráfica del reproductor de música.

Este paquete proporciona las clases necesarias para la interfaz gráfica
utilizando PyQt5.
"""

from ui.main_window import MainWindow
from ui.player_widget import PlayerWidget
from ui.playlist_widget import PlaylistWidget

__all__ = ['MainWindow', 'PlayerWidget', 'PlaylistWidget']
