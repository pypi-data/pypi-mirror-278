from PyQt6.QtWidgets import QMainWindow, QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QWidget, QPushButton, QSlider, QHBoxLayout
from PyQt6. QtGui import QGuiApplication, QIcon
from PyQt6 import QtCore
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl
from enum import Enum
import threading


class AppMode(Enum):
    normal = 1
    debug = 2

class BaseQMainWindow(QMainWindow):
    def __init__(self, width, height, mode):
        super().__init__()
        self.mode = mode
        if mode == AppMode.normal:
            self.monitor = QGuiApplication.screens()[0].geometry()
        elif mode == AppMode.debug:
            if len(QGuiApplication.screens()) > 1:
                self.monitor = QGuiApplication.screens()[2].geometry()
            elif len(QGuiApplication.screens()) > 0:
                self.monitor = QGuiApplication.screens()[1].geometry()
            else :
                self.monitor = QGuiApplication.screens()[0].geometry()
        self.setGeometry(self.monitor.left(), self.monitor.top(), width, height)
        self.keyInfo = []
    
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
        elif e.key() == QtCore.Qt.Key.Key_H:
            print("==================================")
            for idx, info in enumerate(self.keyInfo):
                print(f"{idx}. {info}")
            print("==================================")

class BaseQDialog(QDialog):
    def __init__(self, width, height, mode):
        super().__init__()
        self.mode = mode
        if mode == AppMode.normal:
            self.monitor = QGuiApplication.screens()[0].geometry()
        elif mode == AppMode.debug:
            if len(QGuiApplication.screens()) > 1:
                self.monitor = QGuiApplication.screens()[2].geometry()
            elif len(QGuiApplication.screens()) > 0:
                self.monitor = QGuiApplication.screens()[1].geometry()
            else :
                self.monitor = QGuiApplication.screens()[0].geometry()
        self.setGeometry(self.monitor.left(), self.monitor.top(), width, height)

class StoppableThread(threading.Thread):
    
    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
    
class MLPDataSaveQDialog(BaseQDialog):
    def __init__(self, width, height, mode):
        super().__init__(width, height, mode)
        self.setWindowTitle("HELLO!")

        QBtn = QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.mainLayout = QVBoxLayout()
        message = QLabel("Yes : 모든 정보 저장 | No : OutLier만 저장")

        self.mainLayout.addWidget(message)
        self.mainLayout.addWidget(self.buttonBox)
        self.setLayout(self.mainLayout)

class VideoPlayer(BaseQMainWindow):
    def __init__(self, videoPath):
        super().__init__(800, 600, AppMode.normal)
        self.setWindowTitle('Video Player')
        
        self.mediaPlayer = QMediaPlayer(self)
        self.audioOutput = QAudioOutput(self)
        self.mediaPlayer.setAudioOutput(self.audioOutput)

        videoWidget = QVideoWidget(self)
        self.mediaPlayer.setVideoOutput(videoWidget)

        self.playButton = QPushButton('')
        self.playButton.setIcon(QIcon('./imgs/play.png'))
        self.playButton.clicked.connect(self.togglePlayback)

        self.stopButton = QPushButton('')
        self.stopButton.setIcon(QIcon('./imgs/GymateLogo.png'))
        self.stopButton.clicked.connect(self.stopVideo)

        self.forwardButton = QPushButton('')
        self.forwardButton.setIcon(QIcon('./imgs/fast.png'))
        self.forwardButton.clicked.connect(self.forwardVideo)

        self.backwardButton = QPushButton('')
        self.backwardButton.setIcon(QIcon('./imgs/slow.png'))
        self.backwardButton.clicked.connect(self.backwardVideo)

        self.positionSlider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)

        controlLayout = QHBoxLayout()
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.stopButton)
        controlLayout.addWidget(self.backwardButton)
        controlLayout.addWidget(self.forwardButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.videoPath = videoPath
        self.playVideo()

    def togglePlayback(self):
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.mediaPlayer.pause()
            self.playButton.setIcon(QIcon('./imgs/play'))
        else:
            self.mediaPlayer.play()
            self.playButton.setIcon(QIcon('./imgs/pause'))

    def stopVideo(self):
        self.mediaPlayer.stop()
        self.playButton.setIcon(QIcon('./imgs/play'))

    def forwardVideo(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() + 10000)  # 10 seconds forward

    def backwardVideo(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() - 10000)  # 10 seconds backward

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def playVideo(self):
        url = QUrl.fromLocalFile(self.videoPath)
        self.mediaPlayer.setSource(url)
        self.mediaPlayer.play()