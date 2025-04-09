"""
Módulo que implementa el widget de controles de reproducción.

Este módulo contiene la implementación del widget que proporciona
controles para reproducir, pausar, detener, avanzar y retroceder,
así como para controlar el volumen y mostrar el progreso de la
canción actual.
"""

from PyQt5.QtWidgets import (QWidget, QPushButton, QSlider, QLabel,
                           QHBoxLayout, QVBoxLayout, QStyle,
                           QSizePolicy, QFrame)
from PyQt5.QtCore import Qt, QTime, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor

from player.audio_player import AudioPlayer


class PlayerWidget(QWidget):
    """
    Widget que proporciona controles para el reproductor de audio.
    
    Este widget contiene botones de control, una barra de progreso,
    control de volumen y visualización de información de la canción actual.
    
    Attributes:
        audio_player (AudioPlayer): Reproductor de audio.
        current_song (object): Canción actual.
        
    Signals:
        play_button_clicked: Emitido cuando se hace clic en el botón de reproducción.
        stop_button_clicked: Emitido cuando se hace clic en el botón de detención.
        next_button_clicked: Emitido cuando se hace clic en el botón de siguiente.
        prev_button_clicked: Emitido cuando se hace clic en el botón de anterior.
        song_finished: Emitido cuando se completa la reproducción de una canción.
    """
    
    # Definición de señales
    play_button_clicked = pyqtSignal()
    stop_button_clicked = pyqtSignal()
    next_button_clicked = pyqtSignal()
    prev_button_clicked = pyqtSignal()
    song_finished = pyqtSignal()
    
    def __init__(self, parent=None):
        """
        Inicializa el widget de controles de reproducción.
        
        Args:
            parent: Widget padre (opcional).
        """
        super().__init__(parent)
        
        # Inicializar el reproductor de audio
        self.audio_player = AudioPlayer()
        self.current_song = None
        
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
        
        # Panel de información de la canción actual
        self.song_info_frame = QFrame()
        self.song_info_frame.setFrameShape(QFrame.StyledPanel)
        self.song_info_frame.setFrameShadow(QFrame.Raised)
        
        song_info_layout = QVBoxLayout(self.song_info_frame)
        
        # Etiqueta para el título de la canción
        self.title_label = QLabel("No hay canción seleccionada")
        self.title_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.title_label.setFont(font)
        
        # Etiqueta para el artista
        self.artist_label = QLabel("")
        self.artist_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(10)
        self.artist_label.setFont(font)
        
        # Agregar etiquetas al layout de información
        song_info_layout.addWidget(self.title_label)
        song_info_layout.addWidget(self.artist_label)
        
        # Barra de progreso
        progress_layout = QHBoxLayout()
        
        # Etiqueta para el tiempo transcurrido
        self.time_label = QLabel("00:00")
        
        # Slider para el progreso
        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setRange(0, 100)
        self.progress_slider.setValue(0)
        self.progress_slider.setTracking(False)  # Solo enviar valor cuando se suelta
        
        # Etiqueta para la duración total
        self.duration_label = QLabel("00:00")
        
        # Agregar widgets al layout de progreso
        progress_layout.addWidget(self.time_label)
        progress_layout.addWidget(self.progress_slider)
        progress_layout.addWidget(self.duration_label)
        
        # Botones de control
        controls_layout = QHBoxLayout()
        
        # Botón para ir a la canción anterior
        self.prev_button = QPushButton()
        self.prev_button.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.prev_button.setToolTip("Canción anterior")
        
        # Botón para reproducir/pausar
        self.play_button = QPushButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.setToolTip("Reproducir")
        
        # Botón para detener
        self.stop_button = QPushButton()
        self.stop_button.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stop_button.setToolTip("Detener")
        
        # Botón para ir a la siguiente canción
        self.next_button = QPushButton()
        self.next_button.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.next_button.setToolTip("Siguiente canción")
        
        # Agregar botones al layout de controles
        controls_layout.addStretch()
        controls_layout.addWidget(self.prev_button)
        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.stop_button)
        controls_layout.addWidget(self.next_button)
        controls_layout.addStretch()
        
        # Control de volumen
        volume_layout = QHBoxLayout()
        
        # Etiqueta para el volumen
        self.volume_label = QLabel()
        self.volume_label.setPixmap(self.style().standardPixmap(QStyle.SP_MediaVolume))
        
        # Slider para el volumen
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)  # Volumen inicial
        
        # Agregar widgets al layout de volumen
        volume_layout.addWidget(self.volume_label)
        volume_layout.addWidget(self.volume_slider)
        
        # Agregar todos los layouts al layout principal
        main_layout.addWidget(self.song_info_frame)
        main_layout.addLayout(progress_layout)
        main_layout.addLayout(controls_layout)
        main_layout.addLayout(volume_layout)
        
        # Establecer el layout
        self.setLayout(main_layout)
        
        # Establecer el volumen inicial
        self.audio_player.set_volume(self.volume_slider.value())
    
    def _connect_signals(self):
        """
        Conecta las señales de los widgets con sus manejadores.
        """
        # Conectar botones
        self.play_button.clicked.connect(self._on_play_clicked)
        self.stop_button.clicked.connect(self._on_stop_clicked)
        self.next_button.clicked.connect(self._on_next_clicked)
        self.prev_button.clicked.connect(self._on_prev_clicked)
        
        # Conectar sliders
        self.progress_slider.sliderReleased.connect(self._on_progress_changed)
        self.volume_slider.valueChanged.connect(self._on_volume_changed)
        
        # Conectar señales del reproductor
        self.audio_player.positionChanged.connect(self._on_position_changed)
        self.audio_player.durationChanged.connect(self._on_duration_changed)
        self.audio_player.stateChanged.connect(self._on_state_changed)
        self.audio_player.playbackCompleted.connect(self._on_playback_completed)
    
    def _on_play_clicked(self):
        """
        Manejador para el evento de clic en el botón de reproducción/pausa.
        """
        if not self.current_song:
            return
        
        # Si está reproduciendo, pausar
        if self.audio_player.is_playing():
            self.audio_player.pause()
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.play_button.setToolTip("Reproducir")
        # Si está pausado o detenido, reproducir
        else:
            self.audio_player.play()
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.play_button.setToolTip("Pausar")
        
        # Emitir señal
        self.play_button_clicked.emit()
    
    def _on_stop_clicked(self):
        """
        Manejador para el evento de clic en el botón de detención.
        """
        if not self.current_song:
            return
        
        self.audio_player.stop()
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.setToolTip("Reproducir")
        
        # Emitir señal
        self.stop_button_clicked.emit()
    
    def _on_next_clicked(self):
        """
        Manejador para el evento de clic en el botón de siguiente.
        """
        # Emitir señal
        self.next_button_clicked.emit()
    
    def _on_prev_clicked(self):
        """
        Manejador para el evento de clic en el botón de anterior.
        """
        # Emitir señal
        self.prev_button_clicked.emit()
    
    def _on_progress_changed(self):
        """
        Manejador para el evento de cambio en la barra de progreso.
        """
        if not self.current_song:
            return
        
        # Obtener la posición seleccionada
        position = self.progress_slider.value()
        duration = self.audio_player.get_duration()
        
        # Convertir de porcentaje a milisegundos
        position_ms = int(position * duration / 100)
        
        # Establecer la posición
        self.audio_player.seek(position_ms)
    
    def _on_volume_changed(self, value):
        """
        Manejador para el evento de cambio en el control de volumen.
        
        Args:
            value (int): Nuevo valor del volumen (0-100).
        """
        self.audio_player.set_volume(value)
    
    def _on_position_changed(self, position):
        """
        Manejador para el evento de cambio en la posición de reproducción.
        
        Args:
            position (int): Posición actual en milisegundos.
        """
        # Actualizar la etiqueta de tiempo
        time = QTime(0, 0)
        time = time.addMSecs(position)
        self.time_label.setText(time.toString("mm:ss"))
        
        # Actualizar la barra de progreso solo si no está siendo arrastrada
        duration = self.audio_player.get_duration()
        if duration > 0 and not self.progress_slider.isSliderDown():
            # Convertir a porcentaje (0-100)
            position_percent = int(position * 100 / duration)
            self.progress_slider.setValue(position_percent)
    
    def _on_duration_changed(self, duration):
        """
        Manejador para el evento de cambio en la duración del medio.
        
        Args:
            duration (int): Duración en milisegundos.
        """
        # Actualizar la etiqueta de duración
        time = QTime(0, 0)
        time = time.addMSecs(duration)
        self.duration_label.setText(time.toString("mm:ss"))
    
    def _on_state_changed(self, state):
        """
        Manejador para el evento de cambio en el estado de reproducción.
        
        Args:
            state (QMediaPlayer.State): Nuevo estado del reproductor.
        """
        pass  # Ya manejamos los cambios de estado en otros métodos
    
    def _on_playback_completed(self):
        """
        Manejador para el evento de finalización de reproducción.
        """
        # Restaurar el botón de reproducción
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.setToolTip("Reproducir")
        
        # Emitir señal
        self.song_finished.emit()
    
    def load_song(self, song_node):
        """
        Carga una canción en el reproductor.
        
        Args:
            song_node (NodoCancion): Nodo de la canción a cargar.
        """
        if not song_node:
            return
        
        # Guardar referencia a la canción actual
        self.current_song = song_node
        
        # Cargar el archivo de audio
        self.audio_player.load(song_node.ruta)
        
        # Actualizar la información de la canción
        self.title_label.setText(song_node.titulo)
        self.artist_label.setText(song_node.artista)
        
        # Reiniciar la barra de progreso
        self.progress_slider.setValue(0)
        self.time_label.setText("00:00")
        
        # Iniciar la reproducción automáticamente
        self.audio_player.play()
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.play_button.setToolTip("Pausar")
    
    def get_current_song(self):
        """
        Obtiene la canción actual.
        
        Returns:
            NodoCancion: El nodo de la canción actual, o None si no hay ninguna.
        """
        return self.current_song 