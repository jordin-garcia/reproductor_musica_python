"""
Paquete que contiene los modelos de datos para el reproductor de música.

Este paquete define las clases necesarias para representar y manipular
la estructura de datos de la lista de reproducción.
"""

from models.node import NodoCancion
from models.playlist import ListaReproduccion

__all__ = ['NodoCancion', 'ListaReproduccion']
