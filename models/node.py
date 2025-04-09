"""
Módulo que define la clase NodoCancion para el reproductor de música.

Este módulo implementa la estructura básica para almacenar información de una canción
en forma de nodo para una lista doblemente enlazada circular.
"""


class NodoCancion:
    """
    Clase que representa un nodo en la lista doblemente enlazada circular.
    
    Cada nodo contiene información sobre una canción (título, artista, duración, ruta)
    y referencias al nodo anterior y siguiente en la lista.
    
    Attributes:
        titulo (str): Título de la canción.
        artista (str): Nombre del artista o grupo.
        duracion (int): Duración de la canción en segundos.
        ruta (str): Ruta completa al archivo de audio.
        anterior (NodoCancion): Referencia al nodo anterior en la lista.
        siguiente (NodoCancion): Referencia al nodo siguiente en la lista.
    """
    
    def __init__(self, titulo, artista, duracion, ruta):
        """
        Inicializa un nuevo nodo con la información de la canción.
        
        Args:
            titulo (str): Título de la canción.
            artista (str): Nombre del artista o grupo.
            duracion (int): Duración de la canción en segundos.
            ruta (str): Ruta completa al archivo de audio.
        """
        # Información de la canción
        self.titulo = titulo
        self.artista = artista
        self.duracion = duracion
        self.ruta = ruta
        
        # Referencias para la lista doblemente enlazada
        # Por defecto, los enlaces apuntan a sí mismo (nodo aislado)
        self.anterior = self
        self.siguiente = self
    
    def __str__(self):
        """
        Devuelve una representación en cadena del nodo.
        
        Returns:
            str: Representación en formato "Título - Artista (Duración)".
        """
        # Convertir duración de segundos a formato MM:SS
        minutos = self.duracion // 60
        segundos = self.duracion % 60
        duracion_str = f"{minutos}:{segundos:02d}"
        
        return f"{self.titulo} - {self.artista} ({duracion_str})" 