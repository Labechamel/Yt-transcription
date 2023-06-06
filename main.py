import sys
import os
import time

# pour QT
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
# pour le telechargement de la video
from yt_dlp import YoutubeDL
# pour la transcription whisper
import whisper


class MyWindow(QWidget):
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# la partie suivante est pour l'interface graphique, realiséé avec QT
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transcription Labechamelle")
        self.layout = QVBoxLayout()
        
        self.input_label = QLabel("Past your URL here :")
        self.input_text = QLineEdit()
        
        self.url_audio_label = QLabel("URL Audio Save localy :")
        self.url_audio_text = QLabel()
        
        self.url_video_label = QLabel("URL Video Save localy :")
        self.url_video_text = QLabel()
        
        # on met un text au debut pour que l'utilisateur sache quoi choisir
        self.model_combobox_label = QLabel("Whisper model sizes, check your GPU and the Whisper Github page for makking the perfect choice :")
        # le combobox pour choisir le model
        self.model_combobox = QComboBox()
        self.model_combobox.addItem("Tiny")
        self.model_combobox.addItem("Base")
        self.model_combobox.addItem("Small")
        self.model_combobox.addItem("Medium")
        self.model_combobox.addItem("Large")
        
        # le bouton pour envoyer
        self.send_button = QPushButton("Start")
        self.send_button.clicked.connect(self.on_send_button_clicked)
        self.input_text.returnPressed.connect(self.on_send_button_clicked)
        
        self.output_label = QLabel("Output :")
        self.output_text = QLabel()
        
        # Appliquer une couleur de fond aux zones de sortie
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
        self.layout.addWidget(self.output_label)
        self.layout.addWidget(self.output_text)
        
        self.setLayout(self.layout)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# la partie suivante est pour la definition des variables url et nom de la video, permet de les definir pour les utiliser dans les autres fonctions
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def define_variables(self):
        url_de_la_video = self.input_text.text()
        nom_de_la_video = YoutubeDL().extract_info(url_de_la_video, download=False)['title']
        return url_de_la_video, nom_de_la_video

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# la partie suivante est pour la correction du nom de la video, les caracteres speciaux sont remplacés par des espaces
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def correction_nom_fichier(self, nom_de_la_video):
        liste_caracteres_speciaux = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '.', '#', '!', '$', '%', '&', "'", '(', ')', '+', ',', ';', '=', '@', '[', ']', '^', '_', '`', '{', '}', '~']
        nom_de_la_video = nom_de_la_video[:60]
        for i in liste_caracteres_speciaux:
            nom_de_la_video = nom_de_la_video.replace(i, '')
        return nom_de_la_video

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# la partie suivante est pour le telechargement de la video 
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def download_audio(self, url, nom_video):
        options = {
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
                'format': 'bestvideo+bestaudio',
                'outtmpl': f'video/{nom_video}.%(ext)s',
            }
        else:
            options = {
                'outtmpl': f'video/{nom_video}.%(ext)s',
            }
        with YoutubeDL(options) as ydl:
            ydl.download([url])
    
    def execution_dl(self, url_video, nom_video):
        url = url_video
        
        if not os.path.exists('audio/' + nom_video):
            os.mkdir('audio/' + nom_video)
        else:
            pass
        if not os.path.exists('video/' + nom_video):
            os.mkdir('video/' + nom_video)
        else:
            pass
        self.download_audio(url, nom_video)
        self.download_video(url, nom_video)
        extention_video = YoutubeDL().extract_info(url, download=False)['ext']
        os.rename('video/' + nom_video + '.' + extention_video, 'video/' + nom_video + '/' + nom_video + '.' + extention_video)
        os.rename('audio/' + nom_video + '.mp3', 'audio/' + nom_video + '/' + nom_video + '.mp3')
        self.url_audio_text.setText('audio/' + nom_video + '/' + nom_video + '.mp3')
        self.url_video_text.setText('video/' + nom_video + '/' + nom_video + '.' + extention_video)
        
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# La partie suivante est pour la transcription whisper
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def whisper_transcribe(self, url, model):
        # Chargez le modèle en fonction de la sélection
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
            # Gestion d'erreur si le modèle sélectionné n'est pas valide
            self.output_text.setText("Invalid model selected.")
            
        url_audio = r'' + url

        start_time = time.time()

        result = model.transcribe(url_audio, verbose=False)
        
        elapsed_time = time.time() - start_time

        print("Elapsed time:", elapsed_time)

        try:
            os.mkdir("audio\\" + url_audio.split("\\")[-1].split(".")[0])
        except:
            pass

        with open("audio/" + url_audio.split("/")[-1].split(".")[0] + "/" + url_audio.split("/")[-1].split(".")[0] + ".srt", "w") as f:
            for segment in result["segments"]:
                start_time = "{:02d}:{:02d}:{:02d},000".format(int(segment["start"] // 3600), int((segment["start"] // 60) % 60), int(segment["start"] % 60))
                end_time = "{:02d}:{:02d}:{:02d},000".format(int(segment["end"] // 3600), int((segment["end"] // 60) % 60), int(segment["end"] % 60))
                f.write(start_time + " --> " + end_time + "\n")
                f.write(segment["text"] + "\n\n")
            
        print("The transcription is finished!")
        return elapsed_time
    
    def execution_traduction(self, selected_model):
        url = self.url_audio_text.text()
        time_elapsed = self.whisper_transcribe(url, selected_model)

        # on va déplacer le fichier crée dans le dossier du nom de la video mais dans le dossier video
        os.rename("audio/" + url.split("/")[-1].split(".")[0] + "/" + url.split("/")[-1].split(".")[0] + ".srt", "video/" + url.split("/")[-1].split(".")[0] + "/" + url.split("/")[-1].split(".")[0] + ".srt")

        self.output_text.setText("Transcription completed successfully! " + "\n" + "Elapsed time: " + str(time_elapsed) + " seconds !" + "\n" + "The transcription is in the folder video and the name of the video enjoy !")

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# la partie suivante est pour l'envoie de l'url, c'est ici que tout se passe et que tout se déclenche
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def on_send_button_clicked(self):
        url_video, nom_video = self.define_variables()
        nom_video = self.correction_nom_fichier(nom_video)
        
        
         # Obtenir le modèle sélectionné
        selected_model = self.model_combobox.currentText()

        self.output_text.setText("Downloading...")
        QApplication.processEvents()

        self.execution_dl(url_video, nom_video)

        self.output_text.setText("Transcribing...")
        QApplication.processEvents()

        # Passer le modèle sélectionné à la méthode execution_traduction()
        self.execution_traduction(selected_model)
        self.input_text.clear()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
