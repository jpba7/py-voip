This is a forked repository from @mayankDhiman. I adapted some things for my assignment and fixed some errors that were happening (when I was using a Windows 11 machine).

I added some features like mp3 compression and decompression (even not being ideal for VoIP due to slow compression, but it was a requirement for my assignment).
For the compression to work, you have to install FFmpeg on your computer (https://www.ffmpeg.org/download.html).

Changed the packet format to UDP, so it can be more like a real VoIP application.

I probably forgot some details that were needed for it to run properly in this readme. If you want some help, send me a message on telegram (www.t.me/jpbimbato) or Instagram (@pedrobimbato).

### Implementation of Voice over Internet Protocol (VOIP) in Python3
It is an implementation of Voice over Internet Protocol in Python3 for Windows.

### Running instructions
- Create a virtual environment, using `python -m venv env`
- Install portaudio in your computer with apt install or winget
- Install FFmpeg (https://www.ffmpeg.org/download.html)
- Install all the dependencies using `pip install -r requirements.txt` (probably forgot some, check that)
- Start the server using `python server.py`
- Start the client using `python client.py`, this should start a window with a _Push_ button to record the voice. 
- Push the button in window, speak something, your voice should be audible on speaker where the server is located. 
- Considering the client & server will run on the same machine, I have used `socket.gethostname()` method, if using on different machines, we are supposed to put the address of the host available to both machines

### Keywords
Networking, Internet Protocols
