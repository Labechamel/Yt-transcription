import sys
import os
import time
import re

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QMainWindow, QProgressBar
)
from yt_dlp import YoutubeDL
import whisper


class MyWindow(QWidget):
    progress_signal = Signal(int)

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            progress_str = re.search(r'(\d+(?:\.\d+)?)%', d['_percent_str'])
            if progress_str:
                try:
                    progress = int(float(progress_str.group(1)))
                    self.progress_signal.emit(progress)
                except ValueError:
                    pass

    def define_variables(self):
        url_de_la_video = self.input_text.text()
        nom_de_la_video = YoutubeDL().extract_info(url_de_la_video, download=False)['title']
        return url_de_la_video, nom_de_la_video

    def correction_nom_fichier(self, nom_de_la_video):
        liste_caracteres_speciaux = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '.', '#', '!', '$', '%', '&', "'", '(', ')', '+', ',', ';', '=', '@', '[', ']', '^', '_', '`', '{', '}', '~']
        nom_de_la_video = nom_de_la_video[:60]
        for i in liste_caracteres_speciaux:
            nom_de_la_video = nom_de_la_video.replace(i, '')
        return nom_de_la_video

    def download_audio(self, url, nom_video):
        options = {
            'progress_hooks': [self.progress_hook],
            'format': 'bestaudio/best',
            'outtmpl': f'audio/{nom_video}.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
        }
        with YoutubeDL(options) as ydl:
            ydl.download([url])

    def download_video(self, url, nom_video):
        if 'youtube' in url:
            options = {
                'progress_hooks': [self.progress_hook],
                'format': 'bestvideo+bestaudio',
                'outtmpl': f'video/{nom_video}.%(ext)s',
            }
        else:
            options = {
                'progress_hooks': [self.progress_hook],
                'outtmpl': f'video/{nom_video}.%(ext)s',
            }
        with YoutubeDL(options) as ydl:
            ydl.download([url])

    def execution_dl(self, url_video, nom_video):
        url = url_video

        if not os.path.exists(f'audio/{nom_video}'):
            os.makedirs(f'audio/{nom_video}')
        if not os.path.exists(f'video/{nom_video}'):
            os.makedirs(f'video/{nom_video}')

        self.progress_signal.emit(0)
        
        self.download_audio(url, nom_video)
        self.download_video(url, nom_video)

        extention_video = YoutubeDL().extract_info(url, download=False)['ext']
        os.rename(f'video/{nom_video}.{extention_video}', f'video/{nom_video}/{nom_video}.{extention_video}')
        os.rename(f'audio/{nom_video}.mp3', f'audio/{nom_video}/{nom_video}.mp3')

        self.url_audio_text.setText(f'audio/{nom_video}/{nom_video}.mp3')
        self.url_video_text.setText(f'video/{nom_video}/{nom_video}.{extention_video}')

    def whisper_transcribe(self, url, model):
        if model == "Tiny":
            model = whisper.load_model("tiny")
        elif model == "Base":
            model = whisper.load_model("base")
        elif model == "Small":
            model = whisper.load_model("small")
        elif model == "Medium":
            model = whisper.load_model("medium")
        elif model == "Large":
            model = whisper.load_model("large")
        else:
            self.output_text.setText("Invalid model selected.")
            return None

        url_audio = url

        start_time = time.time()

        result = model.transcribe(url_audio, verbose=False)

        elapsed_time = time.time() - start_time

        print("Elapsed time:", elapsed_time)

        try:
            os.mkdir(f"audio/{url_audio.split('/')[-1].split('.')[0]}")
        except:
            pass

        with open(f"audio/{url_audio.split('/')[-1].split('.')[0]}/{url_audio.split('/')[-1].split('.')[0]}.srt", "w") as f:
            for segment in result["segments"]:
                start_time = "{:02d}:{:02d}:{:02d},000".format(
                    int(segment["start"] // 3600),
                    int((segment["start"] // 60) % 60),
                    int(segment["start"] % 60)
                )
                end_time = "{:02d}:{:02d}:{:02d},000".format(
                    int(segment["end"] // 3600),
                    int((segment["end"] // 60) % 60),
                    int(segment["end"] % 60)
                )
                f.write(start_time + " --> " + end_time + "\n")
                f.write(segment["text"] + "\n\n")

        print("The transcription is finished!")
        return elapsed_time

    def execution_traduction(self, selected_model):
        url = self.url_audio_text.text()
        time_elapsed = self.whisper_transcribe(url, selected_model)

        os.rename(f"audio/{url.split('/')[-1].split('.')[0]}/{url.split('/')[-1].split('.')[0]}.srt", f"video/{url.split('/')[-1].split('.')[0]}/{url.split('/')[-1].split('.')[0]}.srt")

        self.output_text.setText("Transcription completed successfully!\nElapsed time: " + str(time_elapsed) + " seconds!\nThe transcription is in the video folder.")

    def on_send_button_clicked(self):
        url_video, nom_video = self.define_variables()
        nom_video = self.correction_nom_fichier(nom_video)

        selected_model = self.model_combobox.currentText()

        self.output_text.setText("Downloading...")
        QApplication.processEvents()
        
        self.progress_bar.setValue(0)
        
        self.execution_dl(url_video, nom_video)

        self.output_text.setText("Transcribing...")
        QApplication.processEvents()

        self.execution_traduction(selected_model)
        self.input_text.clear()



    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transcription Labechamelle")
        self.layout = QVBoxLayout()

        self.input_label = QLabel("Paste your URL here:")
        self.input_text = QLineEdit()

        self.url_audio_label = QLabel("URL Audio Save locally:")
        self.url_audio_text = QLabel()

        self.url_video_label = QLabel("URL Video Save locally:")
        self.url_video_text = QLabel()

        self.model_combobox_label = QLabel("Whisper model sizes (check your GPU and the Whisper Github page for the perfect choice):")
        self.model_combobox = QComboBox()
        self.model_combobox.addItem("Tiny")
        self.model_combobox.addItem("Base")
        self.model_combobox.addItem("Small")
        self.model_combobox.addItem("Medium")
        self.model_combobox.addItem("Large")

        self.send_button = QPushButton("Start")
        self.send_button.clicked.connect(self.on_send_button_clicked)
        self.input_text.returnPressed.connect(self.on_send_button_clicked)

        self.output_label = QLabel("Output:")
        self.output_text = QLabel()

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        self.progress_signal.connect(self.update_progress)

        self.url_audio_text.setStyleSheet("background-color: #E0E0E0;")
        self.url_video_text.setStyleSheet("background-color: #E0E0E0;")
        self.output_text.setStyleSheet("background-color: black; color: white;")

        self.layout.addWidget(self.model_combobox_label)
        self.layout.addWidget(self.model_combobox)
        self.layout.addWidget(self.input_label)
        self.layout.addWidget(self.input_text)
        self.layout.addWidget(self.send_button)
        self.layout.addWidget(self.url_audio_label)
        self.layout.addWidget(self.url_audio_text)
        self.layout.addWidget(self.url_video_label)
        self.layout.addWidget(self.url_video_text)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.output_label)
        self.layout.addWidget(self.output_text)

        self.progress_signal.connect(self.update_progress)
        self.setLayout(self.layout)

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)
        self.output_text.setText(f"Downloading... {progress}%")
        QApplication.processEvents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
