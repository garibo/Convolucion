from tkinter import *
from sys import argv
from PIL import Image, ImageTk
from datetime import *

def armarVentana(imagen):
	ventana = Tk()
	ventana.title("Filtro Imagenes")

	marco = Frame(ventana)
	b6 = Button(marco, text='Original', command=botonOriginal)
	b1 = Button(marco, text='Escala Grises', command=botonGris)
	b2 = Button(marco, text='Filtro Difusion', command=botonFiltroVecinos)	
	b3 = Button(marco, text='Convolucion', command=botonConvolucion)
	b4 = Button(marco, text='Binarizacion', command=botonBinarizacion)
	b5 = Button(marco, text='Bordes', command=botonBordes)
	b7 = Button(marco, text='Ruido Sal y Pimienta')
	b8 = Button(marco, text='Quitar Ruido')
	b6.pack(side=LEFT)
	b1.pack(side=LEFT)
	b2.pack(side=LEFT)
	b3.pack(side=LEFT)
	b4.pack(side=LEFT)
	b5.pack(side=LEFT)
	b7.pack(side=LEFT)
	b8.pack(side=LEFT)
	marco.pack()

	return ventana

def filtroGrisesPromedio(imagen):
	x, y = imagen.size
	px = imagen.load()
	imagenGrises = Image.new('RGB',(x,y))
	for i in range(x):
		for j in range(y):
			pixeles = px[i,j]
			prom = int(sum(pixeles) / 3)
			imagenGrises.putpixel((i,j),(prom,prom,prom))
	return imagenGrises

def filtroPromedio(imagen):
	x,y = imagen.size
	pixeles = imagen.load()
	imagenFiltrada = Image.new('RGB',(x,y))
	c = 1
	for i in range(x):
		for j in range(y):
			px = pixeles[i,j]
			try:
				p1 = pixeles[i+1,j]
				c += 1
			except:
				p1 = (0,0,0)
			try:
				p2 = pixeles[i-1,j]
				c += 1
			except:
				p2 = (0,0,0)
			try:
				p3 = pixeles[i,j+1]
				c += 1
			except:
				p3 = (0,0,0)
			try:
				p4 = pixeles[i,j-1]
				c += 1
			except:
				p4 = (0,0,0)
			
			if(c > 4): 
				c = 4
			r = p1[0] + p2[0] + p3[0] + p4[0]
			g = p1[0] + p2[0] + p3[0] + p4[0]
			b = p1[0] + p2[0] + p3[0] + p4[0]
			
			imagenFiltrada.putpixel((i,j),(int(r/c),int(g/c),int(b/c)))
			c = 0
	return imagenFiltrada

def filtroConvolucion(imagen):
	x,y = imagen.size
	px = imagen.load()
	#MX = [[-1,0,1],[-1,0,1],[-1,0,1]] #mascara lineas horizontales
	MX = [[-1,0,1],[-2,0,2],[-1,0,1]]
	#MY = [[1,1,1],[0,0,0],[-1,-1,-1]] #mascara lineas verticales
	MY = [[1,2,1],[0,0,0],[-1,-2,-1]]

	imagenNuevaX = Image.new('RGB',(x,y))
	imagenNuevaY = Image.new('RGB',(x,y))
	imn = Image.new('RGB',(x,y))
	for j in range(y):
		for i in range(x):
			sumatoria = 0
			sumatoriay = 0
			for mj in range(-1,2):
				for mx in range(-1,2):
					try:
						sumatoria += MX[mj+1][mx+1]*px[i+mx,j+mj][1]
						sumatoriay += MY[mj+1][mx+1]*px[i+mx,j+mj][1] 
					except:
						sumatoria += 0
						sumatoriay += 0
			punto1 = sumatoria
			punto2 = sumatoriay
			#Normalizar
			if(punto1 < 0):
				punto1 = 0
			if(punto1 > 255):
				punto1 = 255
			if(punto2 < 0):
				punto2 = 0
			if(punto2 > 255):
				punto2 = 255
			imagenNuevaX.putpixel((i,j),(punto1,punto1,punto1))
			imagenNuevaY.putpixel((i,j),(punto2,punto2,punto2))
	px1 = imagenNuevaX.load()
	px2 = imagenNuevaY.load()
	#Mezclar las mascaras
	for i in range(x):
		for j in range(y):
			p1 = px1[i,j]
			p2 = px2[i,j]
			r = int(( p1[0] + p2[0] ) / 2)
			g = int(( p1[1] + p2[1] ) / 2)
			b = int(( p1[2] + p2[2] ) / 2)
			imn.putpixel((i,j),(r,g,b))
	imagenNuevaX.show()
	imagenNuevaY.show()
	return imn


def filtroBinarizacion(imagen, umbral):
	x,y = imagen.size
	px = imagen.load()
	imagenBinarizada = Image.new('RGB',(x,y))
	for i in range(x):
		for j in range(y):
			vRGB = px[i,j][1]
			if (vRGB > umbral):
				imagenBinarizada.putpixel((i,j), (255,255,255))
			else:
				imagenBinarizada.putpixel((i,j), (0,0,0))
	return imagenBinarizada



def refresca(imagen):
	im = ImageTk.PhotoImage(imagen)
	global label
	label = Label(image=im)
	label.imagen = im
	label.pack()

def botonGris():
	global imSerializable
	label.destroy()
	imSerializable = filtroGrisesPromedio(imSerializable)
	refresca(imSerializable)	

def botonOriginal():
	global imSerializable
	global original
	imSerializable = original
	label.destroy()
	refresca(imSerializable)

def botonFiltroVecinos():
	global imSerializable
	label.destroy()
	imSerializable = filtroPromedio(imSerializable)
	refresca(imSerializable)

def botonConvolucion():
	print ("inicio ejecucion: {}".format(datetime.today()))
	global imSerializable
	label.destroy()
	imSerializable = filtroConvolucion(imSerializable)
	refresca(imSerializable)
	print ("final ejecucion: {}".format(datetime.today()))

def botonBinarizacion():
	global imSerializable
	label.destroy()
	imSerializable = filtroBinarizacion(imSerializable,int(argv[2]))
	refresca(imSerializable)

def botonBordes():
	label.destroy()
	global imSerializable
	global original
	print ("inicio proceso: {}".format(datetime.today()))
	imSerializable = original
	print ("imagen original: {}".format(datetime.today()))
	imSerializable = filtroGrisesPromedio(imSerializable)
	print ("imagen en grises: {}".format(datetime.today()))
	imSerializable = filtroPromedio(imSerializable)
	print ("imagen con filtro: {}".format(datetime.today()))
	imSerializable = filtroConvolucion(imSerializable)
	print ("imagen con convolucion: {}".format(datetime.today()))
	imSerializable = filtroBinarizacion(imSerializable,int(argv[2]))
	print ("imagen con binarizacion: {}".format(datetime.today()))
	refresca(imSerializable)
	print ("final proceso: {}".format(datetime.today()))

def main():
	global imSerializable
	global original
	imSerializable = Image.open(argv[1])
	original = imSerializable
	v = armarVentana(imSerializable)
	refresca(imSerializable)
	v.mainloop()

main()
