"""
Módulo que implementa la reproducción de audio utilizando PyQt5.

Este módulo contiene la clase AudioPlayer, que utiliza QMediaPlayer de PyQt5
para reproducir archivos de audio y controlar la reproducción.
"""

from PyQt5.QtCore import QUrl, pyqtSignal, QObject
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class AudioPlayer(QObject):
    """
    Clase que gestiona la reproducción de archivos de audio.
    
    Utiliza QMediaPlayer de PyQt5 para reproducir archivos de audio y
    proporciona métodos para controlar la reproducción (play, pause, stop)
    y el volumen. Emite señales para notificar eventos como cambios de estado,
    posición y duración.
    
    Attributes:
        media_player (QMediaPlayer): Objeto para reproducir archivos multimedia.
        current_file (str): Ruta del archivo actualmente cargado.
        
    Signals:
        positionChanged: Emitido cuando cambia la posición de reproducción.
        durationChanged: Emitido cuando se determina la duración de la canción.
        stateChanged: Emitido cuando cambia el estado de reproducción.
        mediaStatusChanged: Emitido cuando cambia el estado del medio.
        playbackCompleted: Emitido cuando finaliza la reproducción de una canción.
    """
    
    # Definición de señales personalizadas
    positionChanged = pyqtSignal(int)         # Posición actual en milisegundos
    durationChanged = pyqtSignal(int)         # Duración total en milisegundos
    stateChanged = pyqtSignal(int)            # Estado de reproducción
    mediaStatusChanged = pyqtSignal(int)      # Estado del medio
    playbackCompleted = pyqtSignal()          # Finalización de reproducción
    
    def __init__(self):
        """
        Inicializa el reproductor de audio.
        """
        super().__init__()
        
        # Crear el reproductor multimedia
        self.media_player = QMediaPlayer()
        self.current_file = ""
        
        # Conectar señales del reproductor a métodos de manejo
        self.media_player.positionChanged.connect(self._on_position_changed)
        self.media_player.durationChanged.connect(self._on_duration_changed)
        self.media_player.stateChanged.connect(self._on_state_changed)
        self.media_player.mediaStatusChanged.connect(self._on_media_status_changed)
    
    def load(self, file_path):
        """
        Carga un archivo de audio para su reproducción.
        
        Args:
            file_path (str): Ruta al archivo de audio.
        """
        # Convertir la ruta del archivo a QUrl
        url = QUrl.fromLocalFile(file_path)
        
        # Crear contenido multimedia y establecerlo en el reproductor
        content = QMediaContent(url)
        self.media_player.setMedia(content)
        self.current_file = file_path
    
    def play(self):
        """
        Inicia o reanuda la reproducción.
        """
        self.media_player.play()
    
    def pause(self):
        """
        Pausa la reproducción.
        """
        self.media_player.pause()
    
    def stop(self):
        """
        Detiene la reproducción y reinicia la posición.
        """
        self.media_player.stop()
    
    def seek(self, position):
        """
        Establece la posición de reproducción.
        
        Args:
            position (int): Posición en milisegundos.
        """
        self.media_player.setPosition(position)
    
    def set_volume(self, volume):
        """
        Establece el volumen de reproducción.
        
        Args:
            volume (int): Nivel de volumen (0-100).
        """
        self.media_player.setVolume(volume)
    
    def get_volume(self):
        """
        Obtiene el volumen actual.
        
        Returns:
            int: Nivel de volumen (0-100).
        """
        return self.media_player.volume()
    
    def get_position(self):
        """
        Obtiene la posición actual de reproducción.
        
        Returns:
            int: Posición actual en milisegundos.
        """
        return self.media_player.position()
    
    def get_duration(self):
        """
        Obtiene la duración del archivo actual.
        
        Returns:
            int: Duración en milisegundos.
        """
        return self.media_player.duration()
    
    def is_playing(self):
        """
        Verifica si el reproductor está reproduciendo.
        
        Returns:
            bool: True si está reproduciendo, False en caso contrario.
        """
        return self.media_player.state() == QMediaPlayer.PlayingState
    
    def is_paused(self):
        """
        Verifica si el reproductor está en pausa.
        
        Returns:
            bool: True si está en pausa, False en caso contrario.
        """
        return self.media_player.state() == QMediaPlayer.PausedState
    
    def _on_position_changed(self, position):
        """
        Manejador para cambios en la posición de reproducción.
        
        Args:
            position (int): Posición actual en milisegundos.
        """
        # Reenviar la señal a los observadores
        self.positionChanged.emit(position)
    
    def _on_duration_changed(self, duration):
        """
        Manejador para cambios en la duración del medio.
        
        Args:
            duration (int): Duración en milisegundos.
        """
        # Reenviar la señal a los observadores
        self.durationChanged.emit(duration)
    
    def _on_state_changed(self, state):
        """
        Manejador para cambios en el estado de reproducción.
        
        Args:
            state (QMediaPlayer.State): Nuevo estado del reproductor.
        """
        # Reenviar la señal a los observadores
        self.stateChanged.emit(state)
    
    def _on_media_status_changed(self, status):
        """
        Manejador para cambios en el estado del medio.
        
        Args:
            status (QMediaPlayer.MediaStatus): Nuevo estado del medio.
        """
        # Reenviar la señal a los observadores
        self.mediaStatusChanged.emit(status)
        
        # Emitir señal cuando el medio ha llegado al final
        if status == QMediaPlayer.EndOfMedia:
            self.playbackCompleted.emit() 