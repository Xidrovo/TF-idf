__author__ = 'CltControl'
import shutil
import os

op=1 # variable para switch

#Creacion de archivo con stopwords modificadas
# La idea es tener 2 archivos de stopwords uno que tendra las stopwords por default
# y otro que tendra las de por default mas las añadidas por el usuario a travez de la
# segunda opcion del menu principal
if not os.path.exists("custom"):
    os.makedirs("custom")
shutil.copy("stopwords.txt", "custom\\stopwords.txt")

# Creacion de carpeta para guardar los archivos a examinar
if not os.path.exists("files"):
    os.makedirs("files")

#Menu principal

#A continuacion se creara un 'switch'usando un diccionario, ya que no existen los switches en python
def cero(): #case 0
    print("Adios!")

def uno():    #case 1
    a=input("Ingrese el directorio de los archivos")
    shutil.copytree(a,"\\files")

#def dos():   #case2 en construccion


def default(): #  default
    print("Opcion Invalida")



#switch
# uso un diccionario (python) como un switch (c )
switch = {
        '1': uno,
        '0': cero
        }

#Opciones del menu principal
while (op!='0'):
    op=input("""
    Selecione una opcion:
    1.-Ingrese archivos
    2.-Eliminar palabras
    3.-Ingresar Palabras de Busqueda
    4.- Mostrar Estadisticas

    """)
    try:
        switch[op]() #selecciona opcion del switch
    except KeyError:
        default()  #si la opcion ingresada no es valida el dicionario devuelve una exception la que es manejada como un default


#Practicas de python no parar bola xD
#f = open("C:\\Users\\CltControl\\Desktop\\hola.txt", "r+")
#a=f.read()
#print (a)
# f.close()

