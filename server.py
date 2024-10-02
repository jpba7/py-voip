#!/usr/bin/env python
import pyaudio
import socket
import sys
from pydub import AudioSegment
from io import BytesIO

CHUNK = 16384
pa = pyaudio.PyAudio()

stream = pa.open(format=pyaudio.paInt16,    # Formato do audio (16 bits por amostra)
                 channels=1,                # Numero de canais (1 = mono, 2 = stereo)
                 rate=40960,                # Taxa de amostragem em Hz
                 output=True)               # Indica que é pra reproduzir o audio

# Inicialização do socket
HOST = socket.gethostname()  # Pega o nome da máquina local
PORT = 7777                  # Porta
SIZE = 32768                 # Tamanho do buffer
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))      # Associa o socket com o endereço e porta especificados

print("Server is now running\n=======================")

try:
    while True:
        data, addr = sock.recvfrom(SIZE)            # Recebe os dados do cliente
        if data:
            compressed_io = BytesIO(data)           # Cria um buffer de bytes com os dados da memória
            audio_segment = AudioSegment.from_file(compressed_io, format="mp3")  # Carrega o audio comprimido
            stream.write(audio_segment.raw_data)    # Stream the received audio data
            sock.sendto(b'ACK', addr)               # Manda o Ack
except ConnectionResetError as e:
    print(f"Erro de conexão: {e}")
finally:
    sock.close()
    stream.close()
    pa.terminate()
