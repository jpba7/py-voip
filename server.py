#!/usr/bin/env python
import pyaudio
import socket
import sys
from pydub import AudioSegment
from io import BytesIO

# Pyaudio Initialization
chunk = 16384
pa = pyaudio.PyAudio()

# Opening of the audio stream
stream = pa.open(format = pyaudio.paInt16,
                channels = 1,
                rate = 40960,
                output = True)

# Socket Initialization
host = socket.gethostname() # Pega o nome da máquina local
port = 7777
size = 32768
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host,port))

print("Server is now running\n=======================")

# Funcionalidade principal
try:
    while True:
        data, addr = sock.recvfrom(size)
        if data:
            compressed_io = BytesIO(data)
            audio_segment = AudioSegment.from_file(compressed_io, format="mp3")
            stream.write(audio_segment.raw_data)  # Stream the received audio data
            sock.sendto(b'ACK', addr)  # Send an ACK
except ConnectionResetError as e:
    print(f"Erro de conexão: {e}")
finally:
    sock.close()
    stream.close()
    pa.terminate()