from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, Qt
from random import randint
import threading
import sys


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 100)")
        self.setWindowTitle("Video Player")
        self.setGeometry(600, 400, 600, 400)
        self.media_player = QMediaPlayer()
        self.video_widget = QVideoWidget()
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setSource(QUrl.fromLocalFile("sprites/video/eyes.mp4"))
        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.media_player.play()
        threading.Timer(5,  self.close).start()

    def closed(self):
        self.close()

def main():
    app = QApplication(sys.argv)
    video_player = VideoPlayer()
    video_player.show()
    video_player.move(randint(0, 1920), randint(0, 1080))
    sys.exit(app.exec())