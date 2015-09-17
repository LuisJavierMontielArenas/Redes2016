from PyQt4 import QtGui, QtCore
from Servidor import Servidor
from Cliente import Cliente
import threading
import time, sys
import multiprocessing as mp

class Chat(QtGui.QWidget):

	def __init__(self):
		super(Chat, self).__init__()
		self.initUI()

	def initUI(self):
		self.usuario, ok = QtGui.QInputDialog.getText(self,'Usuario','Ingresa Tu Nombre:')
		self.ipP, ok2 = QtGui.QInputDialog.getText(self, 'IP Personal','Ingresa tu direccion IP:')
		ipC, ok3 = QtGui.QInputDialog.getText(self, 'IP Servidor','Ingresa la direccion IP del servidor:')

		self.servidor = Servidor(self.ipP)
		self.cliente = Cliente(ipC)
		self.lista = self.conectarse()

		self.cont = QtGui.QTextEdit(self)
		self.cont.setText(self.lista)

		self.conv = QtGui.QTextEdit(self)
		self.conv.setText(self.servidor.conversacion)

		self.nuevaIP = QtGui.QTextEdit(self)

		self.msj = QtGui.QTextEdit(self)

		self.env = QtGui.QPushButton('Enviar', self)
		self.env.clicked.connect(self.enviar)

		self.act = QtGui.QPushButton('Actualizar', self)
		self.act.clicked.connect(self.mostrar)

		self.audio = QtGui.QPushButton('Audio', self)
		self.audio.clicked.connect(self.mandarAudio)

		self.video = QtGui.QPushButton('Video', self)
		self.video.clicked.connect(self.mandarVideo)

		self.actC = QtGui.QPushButton('Refrescar', self)
		self.actC.clicked.connect(self.refrescar)

		self.cambiarIP = QtGui.QPushButton('Cambiar IP', self)
		self.cambiarIP.clicked.connect(self.cambiarCliente)

		self.cerrar = QtGui.QPushButton('Cerrar Sesion', self)
		self.cerrar.clicked.connect(self.cerrarS)

		hbox = QtGui.QHBoxLayout()
		hbox.addStretch(1)

		vbox = QtGui.QVBoxLayout()
		vbox.addStretch(1)

		vbox2 = QtGui.QVBoxLayout()
		vbox2.addStretch(1)

		vbox.addWidget(self.conv,20)

		grid = QtGui.QGridLayout()
		grid.addWidget(self.msj,0,0)
		grid.addWidget(self.env,0,1)
		grid.addWidget(self.audio,1,1)		
		grid.addWidget(self.act,1,0)
		grid.addWidget(self.video,2,0)

		vbox.addLayout(grid,5)
		vbox2.addWidget(self.cont,6)
		vbox2.addWidget(self.actC)
		vbox2.addWidget(self.nuevaIP,2)
		vbox2.addWidget(self.cambiarIP)
		vbox2.addWidget(self.cerrar)

		hbox.addLayout(vbox)
		hbox.addLayout(vbox2)

		self.setLayout(hbox)

		self.setGeometry(100, 100, 600, 600)
		self.setWindowTitle('Chat')
		self.setWindowIcon(QtGui.QIcon('yahoo_chat.png'))
		self.show()

	def conectarse(self):
		return self.cliente.conectarse(self.ipP,self.usuario)

	def mostrar(self):
		self.conv.setText(self.servidor.conversacion)

	def mandarAudio(self):
		m = self.cliente.grabarAudio()
		self.cliente.enviarAudio(m)

	def mandarVideo(self):
		self.cliente.graba()

	def refrescar(self):
		self.lista = self.cliente.actualizarC(self.ipP)
		self.cont.setText(self.lista)

	def cambiarCliente(self):
		self.cliente.cambiarDireccion(str(self.nuevaIP.toPlainText()))

	def cerrarS(self):
		self.cliente.desconectarse(self.ipP)

	def enviar(self):
		m = str(self.msj.toPlainText())
		exito = self.cliente.enviar(m,self.usuario)
		if exito:
			self.servidor.agregarM(m,self.usuario)
			self.conv.setText(self.servidor.conversacion)
			self.msj.clear()

def main():
	app = QtGui.QApplication(sys.argv)
	chat = Chat()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
