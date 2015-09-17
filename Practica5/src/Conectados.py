from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from SimpleXMLRPCServer import SimpleXMLRPCServer

print "Ingrese la direccion IP de esta computadora:"
ipServidor = input()
conectados = [ipServidor,"Servidor"]

def toString(arreglo):
	cadena = ""
	i = 0
	for i in range(len(arreglo)):
		if i % 2 == 0:
			cadena = cadena+str(arreglo[i+1])+":\n"+str(arreglo[i])+"\n" 
	return cadena

def conectar(ipNueva,usuario):
	conec = []
	for i in range(len(conectados)):
		conec.append(conectados[i])
	conectados.append(ipNueva)
	conectados.append(usuario)
	return toString(conec)

def actualizar(ipC):
	conec = []
	for i in range(len(conectados)):
		conec.append(conectados[i])
	ind = conec.index(ipC)
	del conec[ind]
	del conec[ind]
	return toString(conec)

def desconectar(ipC):
	ind = conectados.index(ipC)
	del conectados[ind]
	del conectados[ind]

serv = SimpleXMLRPCServer((ipServidor,8000),allow_none=True)
serv.register_function(conectar, 'conectar')
serv.register_function(actualizar, 'actualizar')
serv.register_function(desconectar, 'desconectar')
print "Escuchando..."
serv.serve_forever()
