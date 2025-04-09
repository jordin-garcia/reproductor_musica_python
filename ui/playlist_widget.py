"""
Módulo que implementa el widget de lista de reproducción.

Este módulo contiene la implementación del widget que muestra
la lista de canciones y permite interactuar con ella.
"""

from PyQt5.QtWidgets import (QWidget, QTableView, QAbstractItemView,
                            QHeaderView, QVBoxLayout, QPushButton,
                            QHBoxLayout, QStyle, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QColor

from models.playlist import ListaReproduccion
from mutagen.mp3 import MP3
import os


class PlaylistModel(QAbstractTableModel):
    """
    Modelo de datos para la vista de tabla de la lista de reproducción.
    
    Esta clase implementa el modelo de datos necesario para mostrar
    la información de las canciones en una tabla.
    
    Attributes:
        canciones (list): Lista de nodos de canciones a mostrar.
        headers (list): Títulos de las columnas de la tabla.
        cancion_actual (NodoCancion): Referencia a la canción que se está reproduciendo.
    """
    
    def __init__(self, parent=None):
        """
        Inicializa el modelo de datos.
        
        Args:
            parent: Objeto padre (opcional).
        """
        super().__init__(parent)
        self.canciones = []
        self.headers = ["Título", "Artista", "Duración"]
        self.cancion_actual = None  # Referencia a la canción en reproducción
    
    def update_canciones(self, canciones):
        """
        Actualiza la lista de canciones en el modelo.
        
        Args:
            canciones (list): Lista de objetos NodoCancion.
        """
        self.beginResetModel()
        self.canciones = canciones
        self.endResetModel()
    
    def set_cancion_actual(self, cancion):
        """
        Establece la canción que se está reproduciendo actualmente.
        
        Args:
            cancion (NodoCancion): Nodo de la canción actual.
        """
        self.cancion_actual = cancion
        # Notificar cambio en todos los datos para que se actualice la vista
        self.dataChanged.emit(self.index(0, 0), 
                              self.index(self.rowCount() - 1, self.columnCount() - 1))
    
    def rowCount(self, parent=QModelIndex()):
        """
        Devuelve el número de filas en el modelo.
        
        Args:
            parent: Índice del modelo padre (no usado).
            
        Returns:
            int: Número de canciones en la lista.
        """
        return len(self.canciones)
    
    def columnCount(self, parent=QModelIndex()):
        """
        Devuelve el número de columnas en el modelo.
        
        Args:
            parent: Índice del modelo padre (no usado).
            
        Returns:
            int: Número de columnas (3: Título, Artista, Duración).
        """
        return len(self.headers)
    
    def data(self, index, role=Qt.DisplayRole):
        """
        Devuelve los datos para mostrar en la tabla.
        
        Args:
            index: Índice del elemento a mostrar.
            role: Rol de visualización.
            
        Returns:
            Datos a mostrar según el rol solicitado.
        """
        if not index.isValid() or not (0 <= index.row() < len(self.canciones)):
            return None
        
        cancion = self.canciones[index.row()]
        
        # Verificar si la canción es la que se está reproduciendo actualmente
        es_cancion_actual = (self.cancion_actual is not None and 
                            cancion == self.cancion_actual)
        
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return cancion.titulo
            elif index.column() == 1:
                return cancion.artista
            elif index.column() == 2:
                # Formatear duración como MM:SS
                minutos = cancion.duracion // 60
                segundos = cancion.duracion % 60
                return f"{minutos}:{segundos:02d}"
        
        elif role == Qt.TextAlignmentRole:
            if index.column() == 2:  # Alinear duración a la derecha
                return Qt.AlignRight | Qt.AlignVCenter
            return Qt.AlignLeft | Qt.AlignVCenter
        
        elif role == Qt.FontRole:
            font = QFont()
            font.setPointSize(10)
            
            # Si es la canción actual, poner en negrita
            if es_cancion_actual:
                font.setBold(True)
            
            return font
        
        elif role == Qt.BackgroundRole and es_cancion_actual:
            # Cambiar el color de fondo para la canción actual
            return QColor(42, 130, 218, 100)  # Azul semi-transparente
        
        elif role == Qt.ForegroundRole and es_cancion_actual:
            # Cambiar el color del texto para la canción actual
            return QColor(255, 255, 255)  # Texto blanco
        
        return None
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """
        Devuelve los datos para las cabeceras de la tabla.
        
        Args:
            section: Índice de la sección.
            orientation: Orientación (horizontal o vertical).
            role: Rol de visualización.
            
        Returns:
            Datos de la cabecera según el rol solicitado.
        """
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if 0 <= section < len(self.headers):
                return self.headers[section]
        
        return None


class PlaylistWidget(QWidget):
    """
    Widget que muestra y gestiona la lista de reproducción.
    
    Este widget contiene una vista de tabla que muestra las canciones
    en la lista de reproducción y botones para agregar, eliminar y
    seleccionar canciones.
    
    Attributes:
        lista_reproduccion (ListaReproduccion): Lista de reproducción a mostrar.
        table_view (QTableView): Vista de tabla para mostrar las canciones.
        playlist_model (PlaylistModel): Modelo de datos para la tabla.
        
    Signals:
        song_selected: Emitido cuando se selecciona una canción.
        song_added: Emitido cuando se agrega una canción.
        song_removed: Emitido cuando se elimina una canción.
    """
    
    # Definición de señales
    song_selected = pyqtSignal(object)  # Canción seleccionada
    song_added = pyqtSignal(object)     # Canción agregada
    song_removed = pyqtSignal(object)   # Canción eliminada
    
    def __init__(self, parent=None):
        """
        Inicializa el widget de lista de reproducción.
        
        Args:
            parent: Widget padre (opcional).
        """
        super().__init__(parent)
        
        # Inicializar la lista de reproducción
        self.lista_reproduccion = ListaReproduccion()
        
        # Configurar la interfaz de usuario
        self._setup_ui()
        
        # Conectar señales
        self._connect_signals()
    
    def _setup_ui(self):
        """
        Configura los elementos de la interfaz de usuario.
        """
        # Crear layout principal
        main_layout = QVBoxLayout(self)
        
        # Crear la vista de tabla
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setShowGrid(False)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Crear el modelo de datos
        self.playlist_model = PlaylistModel()
        self.table_view.setModel(self.playlist_model)
        
        # Crear los botones de control
        buttons_layout = QHBoxLayout()
        
        # Botón para agregar canciones
        self.add_button = QPushButton("Agregar")
        self.add_button.setIcon(self.style().standardIcon(QStyle.SP_FileDialogNewFolder))
        
        # Botón para eliminar canciones
        self.remove_button = QPushButton("Eliminar")
        self.remove_button.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        
        # Agregar botones al layout
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.remove_button)
        
        # Agregar widgets al layout principal
        main_layout.addWidget(self.table_view)
        main_layout.addLayout(buttons_layout)
        
        # Establecer el layout
        self.setLayout(main_layout)
    
    def _connect_signals(self):
        """
        Conecta las señales de los widgets con sus manejadores.
        """
        # Conectar botones
        self.add_button.clicked.connect(self._on_add_clicked)
        self.remove_button.clicked.connect(self._on_remove_clicked)
        
        # Conectar selección de tabla
        self.table_view.doubleClicked.connect(self._on_table_double_clicked)
    
    def _on_add_clicked(self):
        """
        Manejador para el evento de clic en el botón Agregar.
        Abre un diálogo para seleccionar archivos de audio.
        """
        # Abrir diálogo para seleccionar archivos
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Seleccionar archivos de audio",
            "",
            "Archivos de audio (*.mp3 *.wav *.ogg);;Todos los archivos (*)"
        )
        
        # Procesar los archivos seleccionados
        for file_path in files:
            self._add_song_from_file(file_path)
        
        # Actualizar la vista
        self._update_view()
    
    def _add_song_from_file(self, file_path):
        """
        Agrega una canción a la lista de reproducción desde un archivo.
        
        Args:
            file_path (str): Ruta al archivo de audio.
        """
        try:
            # Obtener el nombre del archivo sin extensión como título
            base_name = os.path.basename(file_path)
            title = os.path.splitext(base_name)[0]
            
            # Intentar extraer metadatos si es un archivo MP3
            artist = "Desconocido"
            duration = 0
            
            if file_path.lower().endswith('.mp3'):
                try:
                    audio = MP3(file_path)
                    duration = int(audio.info.length)
                    
                    # Intentar obtener metadatos
                    if 'TPE1' in audio and audio['TPE1'].text[0]:
                        artist = audio['TPE1'].text[0]
                    if 'TIT2' in audio and audio['TIT2'].text[0]:
                        title = audio['TIT2'].text[0]
                except Exception as e:
                    print(f"Error al leer metadatos MP3: {e}")
            
            # Agregar la canción a la lista de reproducción, siempre al final para mantener orden cronológico
            nodo = self.lista_reproduccion.agregar_cancion(title, artist, duration, file_path)
            
            # Emitir señal de canción agregada
            self.song_added.emit(nodo)
            
            return nodo
        
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error al agregar canción",
                f"No se pudo agregar la canción: {str(e)}"
            )
            return None
    
    def _on_remove_clicked(self):
        """
        Manejador para el evento de clic en el botón Eliminar.
        Elimina la canción seleccionada de la lista de reproducción.
        """
        # Obtener el índice seleccionado
        indexes = self.table_view.selectedIndexes()
        if not indexes:
            return
        
        # Obtener la fila seleccionada (todos los índices de la misma fila)
        row = indexes[0].row()
        
        # Verificar si hay canciones en la lista
        if self.lista_reproduccion.esta_vacia():
            return
        
        # Buscar el nodo correspondiente a la fila seleccionada
        canciones = self.lista_reproduccion.obtener_todas_las_canciones()
        if row < len(canciones):
            # Obtener el nodo a eliminar
            nodo_a_eliminar = canciones[row]
            
            # Guardar el nodo actual para restaurarlo después
            nodo_actual_temp = self.lista_reproduccion.obtener_cancion_actual()
            
            # Si el nodo a eliminar es el actual, simplemente eliminarlo
            if nodo_a_eliminar == self.lista_reproduccion.obtener_cancion_actual():
                nodo_eliminado = self.lista_reproduccion.eliminar_cancion_actual()
                
                # Emitir señal de canción eliminada
                if nodo_eliminado:
                    self.song_removed.emit(nodo_eliminado)
            else:
                # Hacer que el nodo a eliminar sea el actual y eliminarlo
                while self.lista_reproduccion.obtener_cancion_actual() != nodo_a_eliminar:
                    self.lista_reproduccion.siguiente_cancion()
                
                # Eliminar la canción y guardar el nodo eliminado
                nodo_eliminado = self.lista_reproduccion.eliminar_cancion_actual()
                
                # Restaurar el nodo actual si todavía existe y no era el eliminado
                if not self.lista_reproduccion.esta_vacia() and nodo_actual_temp != nodo_eliminado:
                    # Navegar hasta encontrar el nodo actual original
                    while self.lista_reproduccion.obtener_cancion_actual() != nodo_actual_temp:
                        self.lista_reproduccion.siguiente_cancion()
                
                # Emitir señal de canción eliminada
                if nodo_eliminado:
                    self.song_removed.emit(nodo_eliminado)
        
        # Actualizar la vista
        self._update_view()
    
    def _on_table_double_clicked(self, index):
        """
        Manejador para el evento de doble clic en la tabla.
        Selecciona la canción y emite una señal.
        
        Args:
            index: Índice del modelo que fue clicado.
        """
        # Obtener la fila seleccionada
        row = index.row()
        
        # Verificar si hay canciones en la lista
        if self.lista_reproduccion.esta_vacia():
            return
        
        # Buscar el nodo correspondiente a la fila seleccionada
        canciones = self.lista_reproduccion.obtener_todas_las_canciones()
        if row < len(canciones):
            # Obtener el nodo seleccionado
            nodo_seleccionado = canciones[row]
            
            # Hacer que este nodo sea el actual
            if nodo_seleccionado != self.lista_reproduccion.obtener_cancion_actual():
                # Si la lista está en orden cronológico, podemos navegar en cualquier dirección
                # para llegar al nodo deseado de la manera más eficiente
                nodo_actual = self.lista_reproduccion.obtener_cancion_actual()
                
                # Si no hay un nodo actual (poco probable), solo establecemos el primero
                if nodo_actual is None:
                    return
                
                # Buscar y hacer actual la canción seleccionada navegando de forma eficiente
                while self.lista_reproduccion.obtener_cancion_actual() != nodo_seleccionado:
                    self.lista_reproduccion.siguiente_cancion()
                
                # Actualizar la canción actual en el modelo
                self.playlist_model.set_cancion_actual(nodo_seleccionado)
            
            # Emitir señal de canción seleccionada
            self.song_selected.emit(self.lista_reproduccion.obtener_cancion_actual())
    
    def _update_view(self):
        """
        Actualiza la vista de la tabla con los datos actuales.
        """
        # Obtener todas las canciones
        canciones = self.lista_reproduccion.obtener_todas_las_canciones()
        
        # Actualizar el modelo
        self.playlist_model.update_canciones(canciones)
        
        # Mantener la referencia a la canción actual
        cancion_actual = self.lista_reproduccion.obtener_cancion_actual()
        if cancion_actual:
            self.playlist_model.set_cancion_actual(cancion_actual)
    
    def get_current_song(self):
        """
        Obtiene la canción actual de la lista de reproducción.
        
        Returns:
            NodoCancion: El nodo de la canción actual, o None si la lista está vacía.
        """
        return self.lista_reproduccion.obtener_cancion_actual()
    
    def next_song(self):
        """
        Avanza a la siguiente canción en la lista.
        
        Returns:
            NodoCancion: El nodo de la siguiente canción, o None si la lista está vacía.
        """
        nodo = self.lista_reproduccion.siguiente_cancion()
        if nodo:
            # Actualizar el modelo para resaltar la nueva canción actual
            self.playlist_model.set_cancion_actual(nodo)
        self._update_view()
        return nodo
    
    def cancion_anterior(self):
        """
        Retrocede a la canción anterior en la lista.
        
        Returns:
            NodoCancion: El nodo de la canción anterior, o None si la lista está vacía.
        """
        nodo = self.lista_reproduccion.cancion_anterior()
        if nodo:
            # Actualizar el modelo para resaltar la nueva canción actual
            self.playlist_model.set_cancion_actual(nodo)
        self._update_view()
        return nodo
    
    def set_current_song(self, nodo_cancion):
        """
        Establece la canción actual y actualiza la vista.
        
        Args:
            nodo_cancion (NodoCancion): El nodo de la canción a establecer como actual.
        """
        if nodo_cancion:
            self.playlist_model.set_cancion_actual(nodo_cancion)
            self._update_view() 