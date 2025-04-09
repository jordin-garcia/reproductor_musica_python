"""
Módulo que implementa la ventana principal del reproductor de música.

Este módulo contiene la implementación de la ventana principal que
integra todos los componentes de la interfaz gráfica.
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QSplitter, QAction, QMenu, QApplication, QStyle,
                           QMessageBox, QFileDialog, QLabel, QStatusBar)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPalette, QColor

from ui.player_widget import PlayerWidget
from ui.playlist_widget import PlaylistWidget


class MainWindow(QMainWindow):
    """
    Ventana principal del reproductor de música.
    
    Esta ventana integra el reproductor de audio, la lista de reproducción
    y proporciona menús para interactuar con la aplicación.
    
    Attributes:
        player_widget (PlayerWidget): Widget de controles de reproducción.
        playlist_widget (PlaylistWidget): Widget de lista de reproducción.
    """
    
    def __init__(self, parent=None):
        """
        Inicializa la ventana principal.
        
        Args:
            parent: Widget padre (opcional).
        """
        super().__init__(parent)
        
        # Configurar la ventana
        self.setWindowTitle("Reproductor de Música")
        self.setMinimumSize(800, 600)
        
        # Configurar el icono de la aplicación
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        
        # Configurar la interfaz de usuario
        self._setup_ui()
        
        # Configurar menús
        self._setup_menus()
        
        # Configurar la barra de estado
        self._setup_status_bar()
        
        # Conectar señales
        self._connect_signals()
    
    def _setup_ui(self):
        """
        Configura los elementos de la interfaz de usuario.
        """
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes
        main_layout.setSpacing(0)  # Eliminar espaciado entre widgets
        
        # Crear widgets
        self.player_widget = PlayerWidget()
        self.playlist_widget = PlaylistWidget()
        
        # Agregar widgets directamente al layout vertical (sin splitter)
        main_layout.addWidget(self.player_widget)
        main_layout.addWidget(self.playlist_widget)
        
        # Establecer la proporción del espacio (30% para el reproductor, 70% para la lista)
        main_layout.setStretch(0, 30)  # Índice 0 = player_widget, 30% del espacio
        main_layout.setStretch(1, 70)  # Índice 1 = playlist_widget, 70% del espacio
        
        # Aplicar estilo oscuro
        self._apply_dark_theme()
    
    def _setup_menus(self):
        """
        Configura los menús de la aplicación.
        """
        # Menú Archivo
        file_menu = self.menuBar().addMenu("&Archivo")
        
        # Acción Abrir
        open_action = QAction(QIcon.fromTheme("document-open"), "&Abrir...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.setStatusTip("Abrir archivos de audio")
        open_action.triggered.connect(self._on_open_action)
        file_menu.addAction(open_action)
        
        # Separador
        file_menu.addSeparator()
        
        # Acción Salir
        exit_action = QAction(QIcon.fromTheme("application-exit"), "&Salir", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Salir de la aplicación")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menú Reproducción
        playback_menu = self.menuBar().addMenu("&Reproducción")
        
        # Acción Reproducir/Pausar
        self.play_action = QAction(self.style().standardIcon(QStyle.SP_MediaPlay), "&Reproducir", self)
        self.play_action.setShortcut("Space")
        self.play_action.setStatusTip("Reproducir o pausar la canción actual")
        self.play_action.triggered.connect(self._on_play_action)
        playback_menu.addAction(self.play_action)
        
        # Acción Detener
        stop_action = QAction(self.style().standardIcon(QStyle.SP_MediaStop), "&Detener", self)
        stop_action.setShortcut("Ctrl+S")
        stop_action.setStatusTip("Detener la reproducción")
        stop_action.triggered.connect(self._on_stop_action)
        playback_menu.addAction(stop_action)
        
        # Separador
        playback_menu.addSeparator()
        
        # Acción Anterior
        prev_action = QAction(self.style().standardIcon(QStyle.SP_MediaSkipBackward), "A&nterior", self)
        prev_action.setShortcut("Ctrl+Left")
        prev_action.setStatusTip("Ir a la canción anterior")
        prev_action.triggered.connect(self._on_prev_action)
        playback_menu.addAction(prev_action)
        
        # Acción Siguiente
        next_action = QAction(self.style().standardIcon(QStyle.SP_MediaSkipForward), "&Siguiente", self)
        next_action.setShortcut("Ctrl+Right")
        next_action.setStatusTip("Ir a la siguiente canción")
        next_action.triggered.connect(self._on_next_action)
        playback_menu.addAction(next_action)
        
        # Menú Ayuda
        help_menu = self.menuBar().addMenu("A&yuda")
        
        # Acción Acerca de
        about_action = QAction("&Acerca de", self)
        about_action.setStatusTip("Mostrar información acerca de la aplicación")
        about_action.triggered.connect(self._on_about_action)
        help_menu.addAction(about_action)
    
    def _setup_status_bar(self):
        """
        Configura la barra de estado.
        """
        # Crear la barra de estado
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        # Etiqueta para mostrar información
        self.status_label = QLabel("Listo")
        self.statusBar.addPermanentWidget(self.status_label)
    
    def _connect_signals(self):
        """
        Conecta las señales de los widgets con sus manejadores.
        """
        # Señales del widget de reproducción
        self.player_widget.play_button_clicked.connect(self._on_play_button_clicked)
        self.player_widget.stop_button_clicked.connect(self._on_stop_button_clicked)
        self.player_widget.next_button_clicked.connect(self._on_next_button_clicked)
        self.player_widget.prev_button_clicked.connect(self._on_prev_button_clicked)
        self.player_widget.song_finished.connect(self._on_song_finished)
        
        # Señales del widget de lista de reproducción
        self.playlist_widget.song_selected.connect(self._on_song_selected)
        self.playlist_widget.song_added.connect(self._on_song_added)
        self.playlist_widget.song_removed.connect(self._on_song_removed)
    
    def _on_open_action(self):
        """
        Manejador para la acción Abrir.
        Abre un diálogo para seleccionar archivos de audio.
        """
        # Este manejador simula un clic en el botón Agregar del widget de lista
        self.playlist_widget._on_add_clicked()
    
    def _on_play_action(self):
        """
        Manejador para la acción Reproducir/Pausar.
        """
        # Este manejador simula un clic en el botón Reproducir/Pausar del widget de reproductor
        self.player_widget._on_play_clicked()
    
    def _on_stop_action(self):
        """
        Manejador para la acción Detener.
        """
        # Este manejador simula un clic en el botón Detener del widget de reproductor
        self.player_widget._on_stop_clicked()
    
    def _on_prev_action(self):
        """
        Manejador para la acción Anterior.
        """
        self._on_prev_button_clicked()
    
    def _on_next_action(self):
        """
        Manejador para la acción Siguiente.
        """
        self._on_next_button_clicked()
    
    def _on_about_action(self):
        """
        Manejador para la acción Acerca de.
        Muestra un diálogo con información acerca de la aplicación.
        """
        # Crear un QMessageBox personalizado
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Acerca de Reproductor de Música")
        
        # Establecer el texto con formato HTML
        msg_box.setText("""<h2 style="color: #333333; text-align: center;">Reproductor de Música</h2>
        <p style="color: #333333; text-align: center;"><b>Versión 1.0</b></p>
        <hr>
        <p style="color: #333333;">Un reproductor de música desarrollado con PyQt5 que utiliza una 
        lista doblemente enlazada circular para gestionar la lista de reproducción.</p>
        
        <p style="color: #333333;"><b>Características principales:</b></p>
        <ul style="color: #333333;">
            <li>Reproducción de archivos MP3, WAV y OGG</li>
            <li>Gestión de lista de reproducción (agregar/eliminar canciones)</li>
            <li>Controles de reproducción (reproducir, pausar, detener)</li>
            <li>Navegación entre canciones (anterior/siguiente)</li>
            <li>Extracción automática de metadatos</li>
            <li>Interfaz gráfica moderna con tema oscuro</li>
        </ul>
        
        <p style="color: #333333;"><b>Desarrollado para:</b><br>
        Estructura de Datos I<br>
        Universidad Rafael Landívar<br>
        2025</p>
        
        <p style="color: #333333;"><b>Desarrollado por:</b><br>
        Jordin García</p>""")
        
        # Configurar los botones
        msg_box.setStandardButtons(QMessageBox.Ok)
        
        # Mostrar el diálogo
        msg_box.exec_()
    
    def _on_play_button_clicked(self):
        """
        Manejador para el evento de clic en el botón de reproducción/pausa.
        """
        # Actualizar el icono de la acción del menú
        if self.player_widget.audio_player.is_playing():
            self.play_action.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.play_action.setText("&Reproducir")
        else:
            self.play_action.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.play_action.setText("&Pausar")
    
    def _on_stop_button_clicked(self):
        """
        Manejador para el evento de clic en el botón de detención.
        """
        # Restaurar el icono de la acción del menú
        self.play_action.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_action.setText("&Reproducir")
    
    def _on_next_button_clicked(self):
        """
        Manejador para el evento de clic en el botón de siguiente.
        """
        # Avanzar a la siguiente canción en la lista
        next_song = self.playlist_widget.next_song()
        
        # Si hay una siguiente canción, cargarla
        if next_song:
            self.player_widget.load_song(next_song)
            self.status_label.setText(f"Reproduciendo: {next_song.titulo}")
    
    def _on_prev_button_clicked(self):
        """
        Manejador para el evento de clic en el botón de anterior.
        """
        # Retroceder a la canción anterior en la lista
        prev_song = self.playlist_widget.cancion_anterior()
        
        # Si hay una canción anterior, cargarla
        if prev_song:
            self.player_widget.load_song(prev_song)
            self.status_label.setText(f"Reproduciendo: {prev_song.titulo}")
    
    def _on_song_finished(self):
        """
        Manejador para el evento de finalización de reproducción.
        """
        # Restaurar el icono de la acción del menú
        self.play_action.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_action.setText("&Reproducir")
        
        # Avanzar automáticamente a la siguiente canción
        self._on_next_button_clicked()
    
    def _on_song_selected(self, song_node):
        """
        Manejador para el evento de selección de canción.
        
        Args:
            song_node (NodoCancion): Nodo de la canción seleccionada.
        """
        # Cargar la canción seleccionada
        self.player_widget.load_song(song_node)
        
        # Actualizar el estado
        self.status_label.setText(f"Reproduciendo: {song_node.titulo}")
        
        # Actualizar el icono de la acción del menú
        self.play_action.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.play_action.setText("&Pausar")
    
    def _on_song_added(self, song_node):
        """
        Manejador para el evento de canción agregada.
        
        Args:
            song_node (NodoCancion): Nodo de la canción agregada.
        """
        # Si es la primera canción, cargarla automáticamente
        if self.playlist_widget.lista_reproduccion.tamanio == 1:
            self.player_widget.load_song(song_node)
            self.playlist_widget.set_current_song(song_node)  # Actualizar visualización
            self.status_label.setText(f"Reproduciendo: {song_node.titulo}")
            self.play_action.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.play_action.setText("&Pausar")
        else:
            self.status_label.setText(f"Canción agregada: {song_node.titulo}")
    
    def _on_song_removed(self, song_node):
        """
        Manejador para el evento de canción eliminada.
        
        Args:
            song_node (NodoCancion): Nodo de la canción eliminada.
        """
        # Actualizar el estado
        self.status_label.setText(f"Canción eliminada: {song_node.titulo}")
        
        # Si la canción eliminada es la que se está reproduciendo,
        # detener la reproducción o cargar la nueva canción actual
        if song_node == self.player_widget.get_current_song():
            current_song = self.playlist_widget.get_current_song()
            if current_song:
                self.player_widget.load_song(current_song)
                self.status_label.setText(f"Reproduciendo: {current_song.titulo}")
            else:
                self.player_widget.audio_player.stop()
                self.player_widget.current_song = None
                self.player_widget.title_label.setText("No hay canción seleccionada")
                self.player_widget.artist_label.setText("")
                self.play_action.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
                self.play_action.setText("&Reproducir")
    
    def _apply_dark_theme(self):
        """
        Aplica un tema oscuro a la aplicación.
        """
        # Definir una paleta oscura
        palette = QPalette()
        
        # Colores de fondo
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        
        # Colores de texto
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        
        # Colores de selección
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        
        # Roles deshabilitados
        palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
        
        # Aplicar la paleta
        self.setPalette(palette)
        
        # Estilo adicional para los widgets
        self.setStyleSheet("""
            QMainWindow {
                background-color: #353535;
            }
            QLabel {
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #5A5A5A;
                color: #FFFFFF;
                border: 1px solid #5A5A5A;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #6A6A6A;
            }
            QPushButton:pressed {
                background-color: #7A7A7A;
            }
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #4A4A4A;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #2A82DA;
                border: 1px solid #2A82DA;
                width: 18px;
                margin: -2px 0;
                border-radius: 3px;
            }
            QTableView {
                background-color: #252525;
                alternate-background-color: #2D2D2D;
                color: #FFFFFF;
                gridline-color: #353535;
            }
            QHeaderView::section {
                background-color: #3F3F3F;
                color: #FFFFFF;
                padding: 4px;
                border: 1px solid #5F5F5F;
            }
            QMenuBar {
                background-color: #353535;
                color: #FFFFFF;
            }
            QMenuBar::item:selected {
                background-color: #454545;
            }
            QMenu {
                background-color: #353535;
                color: #FFFFFF;
            }
            QMenu::item:selected {
                background-color: #454545;
            }
            QStatusBar {
                background-color: #252525;
                color: #FFFFFF;
            }
        """)
        
        # Aplicar tema oscuro a la barra de menús
        self.menuBar().setStyleSheet("""
            QMenuBar {
                background-color: #353535;
                color: #FFFFFF;
            }
            QMenuBar::item {
                background-color: transparent;
            }
            QMenuBar::item:selected {
                background-color: #454545;
            }
        """)
        
        # Aplicar tema oscuro al menú
        qApp = QApplication.instance()
        qApp.setStyleSheet("""
            QMenu {
                background-color: #353535;
                color: #FFFFFF;
                border: 1px solid #5A5A5A;
            }
            QMenu::item:selected {
                background-color: #454545;
            }
        """)
    
    def closeEvent(self, event):
        """
        Manejador para el evento de cierre de la ventana.
        
        Args:
            event: Evento de cierre.
        """
        # Detener la reproducción
        self.player_widget.audio_player.stop()
        
        # Aceptar el evento para cerrar la ventana
        event.accept() 