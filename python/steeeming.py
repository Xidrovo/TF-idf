__author__ = 'CltControl'
import shutil
import os
import snowballstemmer
import matplotlib.pyplot as plt
import numpy as np
import unicodedata
#from matplotlib.dates import date2num
#import datetime
#import plotly.plotly as py
#import plotly.plotly as py
#import plotly.graph_objs as go
#py.sign_in('riascos', 'cxzmphb1r2') # ni idea :T
import math

#descarguen matplotlib!!!!!!
#descarguen numpy
#http://www.lfd.uci.edu/~gohlke/pythonlibs/   --- python -m pip install nombre.whl


#-----Variables-----
op = 1 # variable para switch
HashTable = {} #Hashmap de frecuencias
MAXDOC = 0
stemmer = snowballstemmer.stemmer('spanish') #selecciona el idioma para steeming
Palabras=[]
activarStem="0"
buscar=""
#-------------------


#Creacion de archivo con stopwords modificadas
# La idea es tener 2 archivos de stopwords uno que tendra las stopwords por default
# y otro que tendra las de por default mas las anadidas por el usuario a travez de la
# segunda opcion del menu principal
if not os.path.exists("custom"):
    os.makedirs("custom")
shutil.copy("stopwords.txt", "custom\\stopwords.txt")

# Creacion de carpeta para output de analisis
if not os.path.exists("Analisis de Contenido"):
    os.makedirs("Analisis de Contenido")

#Menu principal

#A continuacion se creara un 'switch'usando un diccionario, ya que no existen los switches en python
def cero(): #case 0
    print("Adios!")

def uno():    #case 1
    a=input("Ingrese el directorio de los archivos")
    shutil.copytree(a,"files")

def dos():   #case2 en construccion
    f=open("custom\\stopwords.txt","a")
    str=input("Ingrese la palabra que desea eiminar: ")
    f.write(str + "\n")
    f.close()

def tres():

    global buscar
    buscar = input("Ingrese la palabra que desea buscar: ")
    print("Desea Activar el Stemming?\n Escriba 1 para activar\nEscriba cualquier otra cosa para desactivar")
    global activarStem
    activarStem = input()
    SoloGenerarHashmap()
    Var = ""

    try:
        for x in HashTable.get((buscar)):
            Var = Var + " " + str(x)

        print("Tf por Documento: {0:20} ==> {1:10}".format(buscar, Var))
        print("             {0:20} ==> {1:10}".format("Idf:", calcularIDF(buscar)))

    except Exception:
        print ( "La palabra no esta en el documento!" )

#remueve tildes de las palabras
#recibe una lista de strings
#devuelde el string sin tildes
def removerTildes(palabras):
    retorno = []
    for palabra in palabras :
        retorno.append( ''.join(c for c in unicodedata.normalize('NFD', palabra)
                      if unicodedata.category(c) != 'Mn'))
    return retorno

#Este metodo requerira el nombre del documento y un indice del doc.
#Este metodo me dara un set con las palabras que no estan en stopwords las cuales seran usadas para el hashmap.
def GenerarFrecuencias(Documento, indice):
    StopWords = LeerStopWords()
    global Palabras
    with open('files\\' + Documento, 'r') as myfile:
        Palabras.clear()
        data = myfile.read()
        Palabras = data.split()
        toLower(Palabras)#convierto los strings en palabras a minusculas
        toLower(StopWords)
        StopWords = removerTildes(StopWords)
        Palabras=noPunct(Palabras)
        Palabras = BorrarNumeros(Palabras)
        removeAll(Palabras,StopWords)  # palabras - Stopwords
        Palabras = removerTildes(Palabras)

        global activarStem #activo o desactivo el steming
        global buscar


        if activarStem=="1":
            buscar=stemmer.stemWord(buscar)
            for x in range(len(Palabras)):
                Palabras[x] = stemmer.stemWord(Palabras[x])
        else:
            Palabras.clear()
            Palabras = data.split()
            toLower(Palabras)#convierto los strings en palabras a minusculas
            toLower(StopWords)
            Palabras=noPunct(Palabras)
            Palabras = BorrarNumeros(Palabras)
            removeAll(Palabras,StopWords)  # palabras - Stopwords
        for x in Palabras:
            Temp = x
            ListaTemp = []
            if Temp.lower() in HashTable:
                ListaTemp = HashTable.get(Temp.lower())
                Numero = ListaTemp[indice] + 1

                ListaTemp[indice] = Numero
                HashTable[Temp.lower()] = ListaTemp
            else:
                for iteration in range(MAXDOC):
                    ListaTemp.append(0)
                ListaTemp[indice] = 1
                HashTable[x.lower() ] = ListaTemp

        myfile.close()

#elimino las puntuaciondes de todos los documentos
#recibe una lista de  strings a estos les quita los signos de puntuacion y retorna una lista de strings sin puntuaciones
#para enterder mejor revisar documentacion de translate() y maketrans() ojo que es diferente para python 2
def noPunct(palabra):
    palabra2=[]
    punct=[";",":",".",",","\"","\\","?","¿","¡","!","#","%","&","/","1","2","3","4","5","6","7","8","9","0"," ","-","_","(",")","\"","\'","\´","\”","\“"]
    punctuation="".join(punct)
    for x in palabra:
         palabra2.append(x.translate(str.maketrans("","",punctuation)))
    return palabra2

#Convierte los strings almacenados en un arreglo a minusculas
#no devuelve nada, modifica los valores de la lista directamente
def toLower(lista):
    for x in range(len(lista)):
        try:
            int(x)
            lista.remove(x)
        except Exception:
            lista[x]=lista[x].lower()

#Suma la frecuencia de las palabras por documentos (Not sure if this going to be usesfull~
def GenerarCorpus():
    ListaRetorno = []
    for x in HashTable.keys():
        Cont = 0
        for y in HashTable.get(x):
            Cont = Cont + float(y)
        ListaRetorno.append([x, Cont])

    ListaRetorno = SortList(ListaRetorno)
    ListaRetorno = ListaRetorno[::-1]

    return ListaRetorno

#Retorna una lista ordenada dada la siguiente estructura:
    #Hashmap[Key] -> [ListaDeValores]
#Suma la lista de valores para una misma palabra, y retonra una lista solo con las palabras.
def LlavesHashOrdenada(hashtfidf):
    ListaRetorno = []
    for x in hashtfidf.keys():
        Cont = 0
        try:
            for y in hashtfidf.get(x):
                Cont = Cont + float(y)
        except Exception:
                Cont = hashtfidf.get(x)
        ListaRetorno.append([x, Cont])

    ListaRetorno = SortList(ListaRetorno)
    ListaRetorno = ListaRetorno[::-1]

    return ListaRetorno

def GeneracionDeCorpus(hashmap):
    listaRetorno = []
    for x in HashTable.keys():
        Cont = 0
        for y in HashTable.get(x):
            Cont = Cont + float(y)
        listaRetorno.append([x, Cont])

    listaRetorno = SortList(listaRetorno)
    listaRetorno = listaRetorno[::-1]

    return  listaRetorno
#Imprime una lista de palabras junto a la suma total de su frecuencia
def ImprimirCorpus(Corpus):
    for x in Corpus:
        print ("{0:20} ==> {1:10}" .format(x[0], x[1]) )
#Imprime tooodas las palabras con su frecuencia por documento
def ImprimirFullCorpus(Corpus):
    esTitulo = True
    Cont = 0
    for Palabra in Corpus:
        Cont += 1
        listaTemp = HashTable.get(Palabra[0])
        strTemp = ""
        primerTexto = "Palabras: \t\t\t\t\t\t\t\t"
        temp2 = ""
        for y in List:
            temp2 = temp2 + "{0:20}".format(str(y))
        primerTexto = primerTexto + temp2
        for x in listaTemp:
            strTemp = strTemp + "\t\t\t\t" + str(x)

        if (esTitulo):
            print (primerTexto)
            esTitulo = False
        print ("{0:20} ==> {1:10}".format(Palabra[0], strTemp ) )
        if (Cont >= 50):
            break

#Coge los documentos de la carpeta "file"
def GenerarHashmap():
    global List
    List = os.listdir("files")
    Cont = 0
    global HashTable
    HashTable = {}
    global MAXDOC
    MAXDOC = len(List)
    for x in List:
        GenerarFrecuencias(x, Cont)
        Cont = Cont + 1
    listaPalabrasOrdenadas = GenerarCorpus()
    ImprimirFullCorpus(listaPalabrasOrdenadas)

#Ls msma func{on que generar hasmap... con la diferencia que esta no la imprime.
def SoloGenerarHashmap():
    List = os.listdir("files")
    Cont = 0
    global HashTable
    HashTable = {}
    global MAXDOC
    MAXDOC = len(List)
    for x in List:
        GenerarFrecuencias(x, Cont)
        Cont = Cont + 1

#remueve los elementos de la lista 2 que estan la lista 1
def removeAll(lista1,lista2):
    i=0
    temp = ""
    while i<len(lista1): #for x in lista1:
        for y in lista2:
            temp = lista1[i].lower()
            if temp == y.lower():
                lista1.remove(lista1[i])
                i -= 1
                break
            if lista1[i].lower() == '':
                lista1.remove(lista1[i])
                i -= 1
                break

        i += 1

def graficoTf(topDiezTf):
    n = len(os.listdir("files")) #numero de bloques de barras en este caso documentos
    ind = np.arange(n) #espacio entre bloque de barras
    width = 0.07 #ancho de cada barra
    rectangulos = []
    leyendasX = []
    cont = 0
    fig, ax = plt.subplots() #grupo de barras
    for x in topDiezTf:
        #print(topDiezTf[x][1])
        rects1 = ax.bar(ind + (width * cont), x[1], width, color= 'r') #por cada vuelta genero un set de barras del Tf de una palabra en los documentos
        for y in ind:
            ax.text(rects1[0].get_x() + y,rects1[0].get_height()/2.,x[0],rotation='vertical')# imprimo texto en los rectangulos.   formato de funcion text(posX,posY,String,Rotacion)

        rectangulos.append(rects1)
        cont += 1
    for x in os.listdir("files"):
        leyendasX.append(x)

    ax.set_ylabel('TF')
    ax.set_title('Documentos')
    ax.set_xticks(ind + (5 * width))
    ax.set_xticklabels(leyendasX) #leyendas en x ----> palabras
    def autolabel(rects):  #genera los labels de os rectangulos
         # attach some text labels
         for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,'%d' % int(height),ha='center', va='bottom')

         for x in rectangulos:
            autolabel(x)


    plt.show()


#recibe una matriz Palabras vs Idf --> (String, int) y crea un grafico a partir de ella
def graficoIdf(topDiezIdf):
    n = 10 #numero de bloques de barras en este caso palabras
    ind = np.arange(n) #espacio entre bloque de barras
    width = 0.35 #ancho de cada barra
    rectangulos = []
    leyendasX = []
    idfs = [] #aqui guardare las alturas de las barras
    fig, ax = plt.subplots() #ax es el grupo de barras
    for x in topDiezIdf:
        idfs.append(x[1])
        leyendasX.append(x[0])
    rects1 = ax.bar(ind , idfs, width, color= 'b') #por cada vuelta genero la barra del Tf de una palabra en un documento
    rectangulos.append(rects1)
    ax.set_ylabel('Idf')
    ax.set_title('Palabras')
    ax.set_xticks(ind + (width / 2) )
    ax.set_xticklabels(leyendasX) #leyendas en x ----> palabras

    plt.show()

def graficoTfIdf(topDiezTfIdf):
    n = len(os.listdir("files")) #numero de bloques de barras en este caso documentos
    ind = np.arange(n) #espacio entre bloque de barras
    width = 0.07 #ancho de cada barra
    rectangulos = []
    leyendasX = []
    cont = 0
    fig, ax = plt.subplots() #grupo de barras
    for x in topDiezTfIdf:
        #print(topDiezTf[x][1])nombre
        i=0
        for i in range(len(x[1])):
            x[1][i] = math.ceil(float(x[1][i]))
        rects1 = ax.bar(ind + (width * cont), x[1], width, color= 'r') #por cada vuelta genero un set de barras del Tf de una palabra en los documentos
        for y in ind:
            ax.text(rects1[0].get_x() + y,rects1[0].get_height()/2.,x[0],rotation='vertical')# imprimo texto en los rectangulos.   formato de funcion text(posX,posY,String,Rotacion)

        rectangulos.append(rects1)
        cont += 1
    for x in os.listdir("files"):
        leyendasX.append(x)

    ax.set_ylabel('TF - Idf')
    ax.set_title('Documentos')
    ax.set_xticks(ind + (5 * width))
    ax.set_xticklabels(leyendasX) #leyendas en x ----> palabras
    def autolabel(rects):  #genera los labels de os rectangulos
         # attach some text labels
         for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,'%d' % int(height),ha='center', va='bottom')

         for x in rectangulos:
            autolabel(x)


    plt.show()

#Retorna una nueva lista el cual ignora los números.
def BorrarNumeros(lista):
    Index = 0
    NuevLista = []
    for x in lista:
        try:
            int( float(x) )
        except Exception:
            NuevLista.append(x)

    return  NuevLista


#Devuelve una lista con cada palabra del stopword
def LeerStopWords():
    with open('custom\\stopwords.txt', 'r') as myfile:
        data = myfile.read()
        myfile.close()
        return data.split()



def default(): #  default
    print("Opcion Invalida")
#Crea un Hashmaps con resultados de TfIdf por palabra y documentos
#Crea un Hashmap con resultado de Idf, por palabra, devuelve su idf.
def TfIdf():
    global HashTable
    global HashTfIdf
    global HashIdf
    global  List

    global activarStem
    activarStem = "1"
    SoloGenerarHashmap()
    HashIdf = {}
    HashTfIdf  = {}
    topDiez = []
    Cont = 0
    List = listaDeDocumentos()

    #Hago una lista ordenada de acuerdo a la suma de las frecuencias
    listaDePalabrasOrdenadas = GenerarCorpus()
    #Las 10 palabras que estén al inicio (el top diez) será almacenado en una función
    for ignore in listaDePalabrasOrdenadas:
        topDiez.append(ignore)
        if (Cont >= 10):
            break
        Cont += 1
    hashTf = {}
    listaPrueba = []
    Cont = 0
    #Guardo en un hashmap la palabra con su frecuencia separada por documentos
    #La estructura de este hashmap es identica al de 'hashtable'
    for nombrePalabra in topDiez:
        hashTf[nombrePalabra[0]] = HashTable.get(nombrePalabra[0])
        listaPrueba.append(nombrePalabra[0])
        pruebaDos = []
        pruebaDos.append(nombrePalabra[0])
        pruebaDos.append(HashTable.get(nombrePalabra[0]))
        listaPrueba[Cont] = pruebaDos
        Cont += 1

    generarDocTfConMatriz(listaPrueba, "Analisis de Tf")
    Cont = 0
    listatemporito = []
    #Genero una lista dle tamaño relavito a la cantidad de documentos.
    for x in listaDeDocumentos():
        for key in HashTable.keys():
            HashIdf[key] = calcularIDF(key)
            #Si el elemento fue inspeccionado anteriormente, uso sus valores
            #Esto es para no perder el valor
            if key.lower() in HashTfIdf:
                listatemporito = HashTfIdf[key.lower()]
            else:
                listatemporito = []
                for numeros in listaDeDocumentos():
                    listatemporito.append(0)

            listatemporito[Cont] = tfIdf(key, Cont)
            HashTfIdf[key] = listatemporito
        Cont += 1

    Cont = 0
    listaOrdenadaTfIdf = []
    for tfIdfOrdenado in LlavesHashOrdenada(HashTfIdf):
        listaOrdenadaTfIdf.append(tfIdfOrdenado[0])
        pruebaDos = []
        pruebaDos.append(tfIdfOrdenado[0])
        pruebaDos.append(HashTfIdf.get(tfIdfOrdenado[0]))
        listaOrdenadaTfIdf[Cont] = pruebaDos
        Cont += 1
        if (Cont >= 10):
            break

    Cont = 0
    listaOrdenadaIdf = []
    for tfIdfOrdenado in LlavesHashOrdenada(HashIdf):
        listaOrdenadaIdf.append(tfIdfOrdenado[0])
        pruebaDos = []
        pruebaDos.append(tfIdfOrdenado[0])
        pruebaDos.append(HashIdf.get(tfIdfOrdenado[0]))
        listaOrdenadaIdf[Cont] = pruebaDos
        Cont += 1
        if (Cont >= 10):
            break

    generarDocTfConMatriz(listaOrdenadaTfIdf, "Analisis de tf-Idf")
    generarDocIdf(listaOrdenadaIdf)
    graficoTf(listaPrueba)
    graficoIdf(listaOrdenadaIdf)
    graficoTfIdf(listaOrdenadaTfIdf)


#recibe un "String" que representa una palabra
#devuleve el IDF de esa palabra en el corppus
#Idf retorna lo siguiente: log ((CantidadDeDocumentos / EnCuantasDeEsaLaPalabraAparece))
def calcularIDF(palabra):
    docsWithPalabra=0
    if palabra in HashTable: # calculo el numero de documentos que contienen la palabra y lo guardo en docsWithPalabra
        listaTempo = HashTable.get(palabra)
        for x in range(len(listaTempo)):
            if float(listaTempo[x])!= float(0) :
                docsWithPalabra += 1
        if (docsWithPalabra != 0):
            return math.log(len( listaTempo )/docsWithPalabra,10)
        else:
            return 0
    else:
        return 0

#Retorna una lista con todos los documentos de la carpeta 'files'
def listaDeDocumentos():
    listaDeDocs = os.listdir("files")
    return listaDeDocs

#EL TF alcula el numero de veces que aparece una palabra en un documento
#recibe una palabra (String) y un int que representa el indice del documento en el hashmap
#Según tengo entedido... el Tf retorna la frecuencia de esa palabra relativa a la cantidad de palabras existentes en el doc.
#Si una palabra se repite 3 veces, y el doc tiene 100 palabras. Su tf es "3/100"
#O eso dice en este link: http://www.tfidf.com/
def calcularTf(palabra, documento):
    if palabra in HashTable:
        listaTemporal = HashTable.get(palabra)
        return listaTemporal[documento]
    else:
        return 0

#calcula el tfIdf
#recibe un string que representa una palabra y un entero que representa el documento en el que se va a calcular el tdfIdf
#devuelve el Tdf-Idf
def tfIdf(palabra, documento):
    return (format(float(calcularTf(palabra,documento)) * float(calcularIDF(palabra)), '0.6f'))

#Genera un archivo con el Tf o el TfIdf de cada palabra por documento
#recibe un hashtable que contiene el Tf o TfIdf por documento de cada palabra y el nombre del documento
#no retorna nada
def generarDocTfConMatriz(hashTf, nombreArchivo):
    docTf = open("Analisis de Contenido\\" + str(nombreArchivo) + ".txt",'w')
    listaTemp = os.listdir("files")
    docTf.write("{0:20}".format("Palabras" + "\t\t\t"))
    for x in listaTemp:#imprimo nombres de documentos
        docTf.write(x + "\t\t")
    docTf.write("\n")

    for x in hashTf:
        testo = ""
        for y in x[1]:
            testo =  testo + "\t\t\t" + str(y)
        docTf.write("{0:20}: {1:15}".format(x[0], testo))
        docTf.write("\n")

    docTf.close()

#Genera un archivo con el Idf de cada palabra por documento
#recibe un hashtable que contiene el Idf por documento de cada palabra
#no retorna nada
def generarDocIdf(hashIdf):
    docIdf = open("Analisis de Contenido\\Analisis de Idf.txt",'w')
    listaTemp = os.listdir("files")
    docIdf.write("{0:20} {1:20}".format("Palabra", "Idf"))
    docIdf.write("\n")
    for x in hashIdf:
        docIdf.write("{0:20}: {1:20}".format(str(x[0]), str(x[1])) )
        docIdf.write("\n")

    docIdf.close()

#Ordena una lista de manera ascendente.

def SortList(lista):
    NuevaLista = []
    Index = 0
    for x in lista:
        booleano = 1
        if (len(NuevaLista) == 0):
            NuevaLista.append(x)
        else:
            Index = 0
            for y in range(len(NuevaLista)):
                if x[1] < NuevaLista[y][1]:
                    NuevaLista.insert(Index, x)
                    booleano = 0
                    break
                Index += 1

            if (booleano == 1):
                NuevaLista.append(x)
    return NuevaLista

#switch
# uso un diccionario (python) como un switch (c )
switch = {
        '1': uno,
        '0': cero,
        '2': dos,
        '3': tres,
        '4': GenerarHashmap,
        '5': TfIdf,

        }

#Opciones del menu principal
while (op!='0'):
    activarStem="0"
    op=input("""
    Selecione una opcion:
    1.-Ingrese archivos
    2.-Eliminar palabras
    3.-Ingresar Palabras de Busqueda
    4.- Mostrar Estadisticas
    5.- Generar Documentos Tf , Idf y Tf-Idf
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

#Como hacer Stemming aquí abajo
#----------------------------------------------------------
    #stemmer = snowballstemmer.stemmer('spanish')
    #print(stemmer.stemWord("Pensando"))
#----------------------------------------------------------


#Ejemplo de como usar la libreria de tf-idf
# def tf(word, blob):
#     return blob.words.count(word) / len(blob.words)
#
# def n_containing(word, bloblist):
#     return sum(1 for blob in bloblist if word in blob)
#
# def idf(word, bloblist):
#     return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))
#
# def tfidf(word, blob, bloblist):
#     return tf(word, blob) * idf(word, bloblist)
#
# document1 = tb("""Python is a 2000 made-for-TV horror movie directed by Richard
# Clabaugh. The film features several cult favorite actors, including William
# Zabka of The Karate Kid fame, Wil Wheaton, Casper Van Dien, Jenny McCarthy,
# Keith Coogan, Robert Englund (best known for his role as Freddy Krueger in the
# A Nightmare on Elm Street series of films), Dana Barron, David Bowe, and Sean
# Whalen. The film concerns a genetically engineered snake, a python, that
# escapes and unleashes itself on a small town. It includes the classic final
# girl scenario evident in films like Friday the 13th. It was filmed in Los Angeles,
#  California and Malibu, California. Python was followed by two sequels: Python
#  II (2002) and Boa vs. Python (2004), both also made-for-TV films.""")
#
# document2 = tb("""Python, from the Greek word (πύθων/πύθωνας), is a genus of
# nonvenomous pythons[2] found in Africa and Asia. Currently, 7 species are
# recognised.[2] A member of this genus, P. reticulatus, is among the longest
# snakes known.""")
#
# document3 = tb("""The Colt Python is a .357 Magnum caliber revolver formerly
# manufactured by Colt's Manufacturing Company of Hartford, Connecticut.
# It is sometimes referred to as a "Combat Magnum".[1] It was first introduced
# in 1955, the same year as Smith & Wesson's M29 .44 Magnum. The now discontinued
# Colt Python targeted the premium revolver market segment. Some firearm
# collectors and writers such as Jeff Cooper, Ian V. Hogg, Chuck Hawks, Leroy
# Thompson, Renee Smeets and Martin Dougherty have described the Python as the
# finest production revolver ever made.""")
#
# bloblist = [document1, document2, document3]
# for i, blob in enumerate(bloblist):
#     print("Top words in document {}".format(i + 1))
#     scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
#     sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
#     for word, score in sorted_words[:3]:
#         print("Word: {}, TF-IDF: {}".format(word, round(score, 5)))

#
# import numpy as np   http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.bar
# import matplotlib.pyplot as plt
#
# N = 5
# menMeans = (20, 35, 30, 35, 27)
# menStd = (2, 3, 4, 1, 2)
#
# ind = np.arange(N)  # the x locations for the groups
# width = 0.35       # the width of the bars
#
# fig, ax = plt.subplots()
# rects1 = ax.bar(ind, menMeans, width, color='r')
#
# womenMeans = (25, 32, 34, 20, 25)
# womenStd = (3, 5, 2, 3, 3)
# rects2 = ax.bar(ind + width, womenMeans, width, color='y', yerr=womenStd)
#
# # add some text for labels, title and axes ticks
# ax.set_ylabel('Scores')
# ax.set_title('Scores by group and gender')
# ax.set_xticks(ind + width)
# ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))
#
# #ax.legend((rects1[0], rects2[0]), ('Men', 'Women'))
#
#
# def autolabel(rects):
#     # attach some text labels
#     for rect in rects:
#         height = rect.get_height()
#         ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
#                 '%d' % int(height),
#                 ha='center', va='bottom')
#
# #autolabel(rects1)
# #autolabel(rects2)
#
# plt.show()
