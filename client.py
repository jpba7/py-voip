import pyaudio
import socket
import sys
import time
import threading
from tkinter import *
from pydub import AudioSegment
from io import BytesIO

CHUNK = 16384
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 40960

p = pyaudio.PyAudio()  # Cria um objeto pyaudio

# Cria um stream de audio
stream = p.open(format=FORMAT,            # Formato do audio (16 bits por amostra)
                channels=CHANNELS,        # Numero de canais (1 = mono, 2 = stereo)
                rate=RATE,                # Taxa de amostragem em Hz
                input=True,               # Indica que é para gravar o audio
                frames_per_buffer=CHUNK)  # Tamanho do buffer de audio

# Inicialização do socket
HOST = socket.gethostname()                             # Pega o nome da máquina local
PORT = 7777                                             # Porta
SIZE = 32768                                            # Tamanho do buffer
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # Criação do socket (AF_INET = IPv4, SOCK_DGRAM = UDP)
s.connect((HOST, PORT))                                 # Conecta o socket com o servidor específicado


class VoIPFrame(Frame):                                   # Classe que representa a janela principal
    def on_mouse_down(self, event):                       # Função que é chamada quando o botão é pressionado
        self.mute = False
        self.speak_start()

    def mute_speak(self, event):                         # Função que é chamada quando o botão é solto (muta o microfone)
        self.mute = True
        print("Você foi mutado")

    def speak_start(self):                               # Função que inicia a thread que envia o audio
        t = threading.Thread(target=self.speak)
        t.start()

    def speak(self):                                      # Função que comprime e envia o audio
        print("Você está desmutado")
        while self.mute is False:
            data = stream.read(CHUNK)                     # Lê o audio do microfone e armazena em data (dados brutos)
            audio_segment = AudioSegment(data, sample_width=2, frame_rate=RATE, channels=CHANNELS)
            compressed_io = BytesIO()                     # Cria um buffer de bytes
            audio_segment.export(compressed_io, format="mp3", bitrate="32k")  # Comprime o audio para MP3
            compressed_data = compressed_io.getvalue()    # Pega os dados comprimidos do buffer de bytes
            s.send(compressed_data)                       # Envia os dados comprimidos pro servidor
            s.recv(SIZE)                                  # Recebe um ACK do servidor

    def create_widgets(self):
        self.speakb = Button(self)
        self.speakb["text"] = "Falar"
        self.speakb.pack({"side": "left"})

        self.speakb.bind("<ButtonPress-1>", self.on_mouse_down)
        self.speakb.bind("<ButtonRelease-1>", self.mute_speak)

    def __init__(self, master=None):
        self.mute = True
        Frame.__init__(self, master)
        self.mouse_pressed = False
        self.pack()
        self.create_widgets()


root = Tk()
app = VoIPFrame(master=root)
app.mainloop()
root.destroy()
s.close()
stream.close()
p.terminate()
