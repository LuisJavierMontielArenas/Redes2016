from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from SimpleXMLRPCServer import SimpleXMLRPCServer
import pyaudio
import cv2
import numpy as np
import numpy 
import threading
CHUNK = 1024
CHANNELS = 1 
RATE = 44100
DELAY_SECONDS = 5 

frames = []
from cStringIO import StringIO
from numpy.lib import format
class Servidor:
	def __init__(self, ipPersonal):
		self.conversacion = "Bienvenido al chat"
		serv = SimpleXMLRPCServer((ipPersonal,8000),allow_none=True)
		playVThread = threading.Thread(target=self.reproduce)
		playVThread.setDaemon(True)
		playVThread.start()
		serv.register_function(self.playAudio, 'playAudio') 
		serv.register_function(self.playVideo, 'playVideo') 
		serv.register_function(self.recibir,"recibir")
		tS = threading.Thread(target=serv.serve_forever)
		tS.setDaemon(True)
		tS.start()
	
	def recibir(self,mensaje):
		self.conversacion = self.conversacion + "\n" + str(mensaje)
		self.sinMostrar = True
		return True

	def toArray(s):
	    f=StringIO(s)
	    arr=format.read_array(f)
	    return arr

	def playAudio(self,audio):
		p = pyaudio.PyAudio()
		FORMAT = p.get_format_from_width(2)
		stream = p.open(format=FORMAT,
						channels=CHANNELS,
						rate=RATE,
						output=True,
						frames_per_buffer=CHUNK)
		data = audio.data
		stream.write(data)
		stream.close()
		p.terminate()

	def playVideo(self,video):
		frames.append(toArray(video.data))
	
	def reproduce(self):
	    while True:
	        if len(frames) > 0:
	            cv2.imshow('Servidor',frames.pop(0))
	            if cv2.waitKey(1) & 0xFF==ord('q'):
	                break
	    cv2.destroyAllWindows()

	def agregarM(self,mensaje,usuario):
		self.conversacion = self.conversacion + "\n" + str(usuario) + ": " + str(mensaje)
