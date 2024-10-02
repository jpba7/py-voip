import pyaudio
import socket
import sys
import time
import threading
from tkinter import *
from pydub import AudioSegment
from io import BytesIO

chunk = 16384 
FORMAT = pyaudio.paInt16  
CHANNELS = 1  
RATE = 40960

p = pyaudio.PyAudio() # Cria um objeto pyaudio

# Cria um stream de audio
stream = p.open(format = FORMAT,            # Formato do audio (16 bits por amostra)
                channels = CHANNELS,        # Numero de canais (1 = mono, 2 = stereo)       
                rate = RATE,                # Taxa de amostragem em Hz
                input = True,               # Indica que é para gravar o audio
                frames_per_buffer = chunk)  # Tamanho do buffer de audio

# Inicialização do socket
host = socket.gethostname() # Pega o nome da máquina local
port = 7777
size = 32768 # Tamanho do buffer
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Criação do socket (AF_INET = IPv4, SOCK_DGRAM = UDP)
s.connect((host,port)) # Conecta o socket com o servidor específicado

class VOIP_FRAME(Frame):
    def OnMouseDown(self, event):
        self.mute = False
        self.speakStart()
        
    def muteSpeak(self, event):
        self.mute = True
        print("Você foi mutado")
        
    def speakStart(self):
        t = threading.Thread(target=self.speak)
        t.start()
                
    def speak(self):
        print("Você está desmutado")
        while self.mute is False:
            data = stream.read(chunk)
            audio_segment = AudioSegment(data, sample_width=2, frame_rate=RATE, channels=CHANNELS)
            compressed_io = BytesIO()
            audio_segment.export(compressed_io, format="mp3", bitrate="32k")
            compressed_data = compressed_io.getvalue()
            s.send(compressed_data)
            s.recv(size)
        
    def createWidgets(self):
        self.speakb = Button(self)
        self.speakb["text"] = "Falar"
        self.speakb.pack({"side": "left"})

        self.speakb.bind("<ButtonPress-1>", self.OnMouseDown)
        self.speakb.bind("<ButtonRelease-1>", self.muteSpeak)

    def __init__(self, master=None):
        self.mute = True
        Frame.__init__(self, master)
        self.mouse_pressed = False
        self.pack()
        self.createWidgets()

root = Tk()
app = VOIP_FRAME(master=root)
app.mainloop()
root.destroy()
s.close()
stream.close()
p.terminate()