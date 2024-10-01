import pyaudio
import socket
import sys
import time
import threading
from tkinter import *

chunk = 1024 
FORMAT = pyaudio.paInt16  
CHANNELS = 1  
RATE = 10240

p = pyaudio.PyAudio() # Cria um objeto pyaudio

# Cria um stream de audio
stream = p.open(format = FORMAT,            # Formato do audio (16 bits por amostra)
                channels = CHANNELS,        # Numero de canais (1 = mono, 2 = stereo)       
                rate = RATE,                # Taxa de amostragem em Hz
                input = True,               # Indica que é para gravar o audio
                frames_per_buffer = chunk)  # Tamanho do buffer de audio

# Inicialização do socket
host = 'localhost'
port = 50000
size = 1024 # Tamanho do buffer
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Criação do socket (AF_INET = IPv4, SOCK_DGRAM = UDP)
s.connect((host,port)) # Conecta o socket com o servidor específicado

class VOIP_FRAME(Frame):
    
    def OnMouseDown(self, event):
        # Evento de clique do mouse, seta a variavel self.mute para False e chama a função speakStart
        self.mute = False
        self.speakStart()
        
    def muteSpeak(self, event):
        # Quando o botão é solto, a variavel self.mute é setada para True
        self.mute = True
        print("Você foi mutado")
        
    def speakStart(self):
        # Inicializa a thread que irá enviar os dados do microfone para o servidor
        t = threading.Thread(target=self.speak)
        t.start()
                
    def speak(self):
        print("Você está desmutado")
        while self.mute is False:
            data = stream.read(chunk)
            s.send(data)
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

    