"""
Módulo que implementa una lista de reproducción como lista doblemente enlazada circular.

Este módulo contiene la implementación de la clase ListaReproduccion, que gestiona
una colección de canciones utilizando una estructura de lista doblemente enlazada circular.
"""

from models.node import NodoCancion


class ListaReproduccion:
    """
    Implementación de una lista de reproducción usando una lista doblemente enlazada circular.
    
    Esta clase permite gestionar una colección de canciones con operaciones eficientes
    de navegación en ambas direcciones (anterior/siguiente) y mantiene una referencia
    a la canción que se está reproduciendo actualmente.
    
    Attributes:
        actual (NodoCancion): Referencia al nodo que contiene la canción actual.
        primero (NodoCancion): Referencia al primer nodo de la lista (primera canción agregada).
        tamanio (int): Número de canciones en la lista de reproducción.
    """
    
    def __init__(self):
        """
        Inicializa una lista de reproducción vacía.
        """
        self.actual = None  # No hay canciones en la lista inicialmente
        self.primero = None # Referencia al primer nodo (orden cronológico)
        self.tamanio = 0    # Contador de canciones
    
    def esta_vacia(self):
        """
        Verifica si la lista de reproducción está vacía.
        
        Returns:
            bool: True si la lista está vacía, False en caso contrario.
        """
        return self.tamanio == 0
    
    def agregar_cancion(self, titulo, artista, duracion, ruta):
        """
        Agrega una nueva canción a la lista de reproducción.
        
        La nueva canción se inserta siempre al final de la lista, manteniendo
        un orden cronológico. Si la lista está vacía, la canción se convierte
        en la primera y única de la lista.
        
        Args:
            titulo (str): Título de la canción.
            artista (str): Nombre del artista o grupo.
            duracion (int): Duración de la canción en segundos.
            ruta (str): Ruta completa al archivo de audio.
            
        Returns:
            NodoCancion: El nodo recién creado.
        """
        # Crear un nuevo nodo con la información de la canción
        nuevo_nodo = NodoCancion(titulo, artista, duracion, ruta)
        
        # Caso 1: Lista vacía
        if self.esta_vacia():
            # El nodo apunta a sí mismo en ambas direcciones
            self.actual = nuevo_nodo
            self.primero = nuevo_nodo  # El primer nodo agregado es también el primero de la lista
        # Caso 2: Lista con al menos una canción
        else:
            # El último nodo es el anterior al primero en una lista circular
            ultimo_nodo = self.primero.anterior
            
            # Insertar el nuevo nodo después del último
            # 1. Establecer los enlaces del nuevo nodo
            nuevo_nodo.siguiente = self.primero
            nuevo_nodo.anterior = ultimo_nodo
            # 2. Ajustar los enlaces de los nodos adyacentes
            ultimo_nodo.siguiente = nuevo_nodo
            self.primero.anterior = nuevo_nodo
        
        # Incrementar el contador de canciones
        self.tamanio += 1
        
        return nuevo_nodo
    
    def eliminar_cancion_actual(self):
        """
        Elimina la canción actual de la lista de reproducción.
        
        Si la lista queda vacía, establece actual a None.
        Si hay más canciones, actual se mueve a la siguiente canción.
        
        Returns:
            NodoCancion: El nodo que fue eliminado, o None si la lista está vacía.
        """
        # Verificar si la lista está vacía
        if self.esta_vacia():
            return None
        
        # Guardar referencia al nodo que se va a eliminar
        nodo_eliminado = self.actual
        
        # Caso 1: Si es el único nodo en la lista
        if self.tamanio == 1:
            self.actual = None
            self.primero = None
        # Caso 2: Hay más de un nodo en la lista
        else:
            # Si se está eliminando el primer nodo, actualizar primero
            if self.actual == self.primero:
                self.primero = self.primero.siguiente
            
            # Ajustar los enlaces de los nodos adyacentes para "saltarse" el nodo actual
            self.actual.anterior.siguiente = self.actual.siguiente
            self.actual.siguiente.anterior = self.actual.anterior
            # Mover el puntero actual al siguiente nodo
            self.actual = self.actual.siguiente
        
        # Decrementar el contador de canciones
        self.tamanio -= 1
        
        return nodo_eliminado
    
    def siguiente_cancion(self):
        """
        Avanza a la siguiente canción en la lista.
        
        Returns:
            NodoCancion: El nodo de la siguiente canción, o None si la lista está vacía.
        """
        if self.esta_vacia():
            return None
        
        # Mover el puntero actual al siguiente nodo
        self.actual = self.actual.siguiente
        return self.actual
    
    def cancion_anterior(self):
        """
        Retrocede a la canción anterior en la lista.
        
        Returns:
            NodoCancion: El nodo de la canción anterior, o None si la lista está vacía.
        """
        if self.esta_vacia():
            return None
        
        # Mover el puntero actual al nodo anterior
        self.actual = self.actual.anterior
        return self.actual
    
    def obtener_cancion_actual(self):
        """
        Obtiene la canción actual en la lista de reproducción.
        
        Returns:
            NodoCancion: El nodo de la canción actual, o None si la lista está vacía.
        """
        return self.actual
    
    def obtener_todas_las_canciones(self):
        """
        Obtiene todas las canciones de la lista de reproducción en orden cronológico.
        
        Returns:
            list: Lista de objetos NodoCancion en el orden en que fueron agregados.
        """
        if self.esta_vacia():
            return []
        
        # Lista para almacenar todos los nodos
        canciones = []
        
        # Empezar por el primer nodo (para mantener el orden cronológico)
        nodo = self.primero
        
        # Recorrer la lista circular hasta volver al nodo de inicio
        # Añadir el primer nodo
        canciones.append(nodo)
        
        # Moverse al siguiente nodo
        nodo = nodo.siguiente
        
        # Continuar recorriendo mientras no volvamos al nodo inicial
        while nodo != self.primero:
            canciones.append(nodo)
            nodo = nodo.siguiente
        
        return canciones
    
    def __len__(self):
        """
        Devuelve el número de canciones en la lista de reproducción.
        
        Returns:
            int: Cantidad de canciones en la lista.
        """
        return self.tamanio 