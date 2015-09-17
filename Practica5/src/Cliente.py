import pyaudio
import numpy as np
import cv2
import multiprocessing as mp
import time
import xmlrpclib
import numpy
from cStringIO import StringIO
CHUNK = 1024
CHANNELS = 1 
RATE = 44100
RECORD_SECONDS = 2
cap = cv2.VideoCapture(0)
from numpy.lib import format

class Cliente:
	def __init__(self, ipContacto):
		self.s = xmlrpclib.ServerProxy("http://"+str(ipContacto)+":8000/")
		queue = mp.Queue()
		p = mp.Process(target=self.graba, args=(queue,))
		p.start()

	def cambiarDireccion(self, ip):
		self.s = xmlrpclib.ServerProxy("http://"+str(ip)+":8000/")

	def conectarse(self,ip,usuario):
		return self.s.conectar(ip,usuario)

	def actualizarC(self,ipC):
		return self.s.actualizar(ipC)

	def desconectarse(self,ip):
		return self.s.desconectar(ip)

	def enviar(self, mensaje, usuario):
		exito = self.s.recibir(str(usuario) + ": " + str(mensaje))
		if exito:
			return True
		return False

	def grabarAudio(self):
		chunk = 1024
		FORMAT = pyaudio.paInt16
		canales= 2
		frecuencia = 44100
		segundos = 5
    
		q = pyaudio.PyAudio()
		stream = q.open(format = FORMAT,channels = canales,rate = frecuencia,input = True,output = True,frames_per_buffer = chunk)

		audio = [] 
		for i in range(0, frecuencia / chunk * segundos):
			data = stream.read(chunk)
			audio.append(data)

		return ''.join(audio)

	def enviarAudio(self,audio):
		return self.s.playAudio(xmlrpclib.Binary(audio))

	def toString(data):
		f= StringIO()
		format.write_array(f,data)
		return f.getvalue()

	def graba(self,q):
		while(True):
			ret, frame = cap.read()
			cv2.imshow('Cliente',frame) 
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			data = xmlrpclib.Binary(toString(frame))
			proxy.playVideo(data) 
		cap.release()
		cv2.destroyAllWindows()
