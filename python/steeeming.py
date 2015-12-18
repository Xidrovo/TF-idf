__author__ = 'CltControl'
import shutil
import os
import snowballstemmer
#import string


#-----Variables-----
op = 1 # variable para switch
HashTable = {} #Hashmap de frecuencias
MAXDOC = 0
stemmer = snowballstemmer.stemmer('spanish') #selecciona el idioma para steeming

activarStem="0"
buscar=""
#-------------------


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

        print("{0:20} ==> {1:10}".format(buscar, Var))
    except Exception:
        print ( "La palabra no está en el documento!" )

#Este método requerirá el nombre del documento y un índice del doc.
#Este método me dará un set con las palabras que no están en stopwords las cuales serán usadas para el hashmap.
def GenerarFrecuencias(Documento, indice):
    StopWords = LeerStopWords()
    global Palabras
    with open('files\\' + Documento, 'r') as myfile:
        global Palabras
        data = myfile.read()
        Palabras = data.split()
        toLower(Palabras)#convierto los strings en palabras a minusculas
        toLower(StopWords)
        Palabras=noPunct(Palabras)
        Palabras = BorrarNumeros(Palabras)
        removeAll(Palabras,StopWords)  # palabras - Stopwords

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
    punct=[";",":",".",",","\"","\\","?","¿","¡","!","#","%","&","/","1","2","3","4","5","6","7","8","9","0"," ","-","_","(",")","\"","\'","\´","\”","\“"]#caracteres a ingnorar
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
            Cont = Cont + y
        ListaRetorno.append([x, Cont])

    ListaRetorno = SortList(ListaRetorno)
    ListaRetorno = ListaRetorno[::-1]

    return ListaRetorno

#Imprime una lista de palabras junto a la suma total de su frecuencia
def ImprimirCorpus(Corpus):
    for x in Corpus:
        print ("{0:20} ==> {1:10}" .format(x[0], x[1]) )
#Imprime tooodas las palabras con su frecuencia por documento
def ImprimirFullCorpus(Corpus):
    esTitulo = True
    for Palabra in Corpus:
        listaTemp = HashTable.get(Palabra[0])
        strTemp = ""
        primerTexto = "Plabras: \t\t\t\t\t\t\t\t"
        temp2 = ""
        for y in List:
            temp2 = temp2 + "{0:15}".format(str(y))
        primerTexto = primerTexto + temp2
        for x in listaTemp:
            strTemp = strTemp + "\t\t\t\t" + str(x)

        if (esTitulo):
            print (primerTexto)
            esTitulo = False
        print ("{0:20} ==> {1:10}".format(Palabra[0], strTemp ) )

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

def TfIdf():
    listaDeTamano = []
    global List
    global HashTable
    List = os.listdir("files")
    for x in List:
        with open('files\\' + x, 'r') as myfile:
            data = myfile.read()
            Palabras = data.split()
        listaDeTamano.append( len(Palabras) )

    SoloGenerarHashmap()
    listaPalabrasOrdenadas = GenerarCorpus()

    for y in HashTable.keys():
        TempList = HashTable.get(y)
        for z in range(len(TempList)):
            TempList[z] = TempList[z] / listaDeTamano[z]

        HashTable[y] = TempList
    TopDiez = []
    Cont = 0
    for NoOptimo in listaPalabrasOrdenadas:
        TopDiez.append(NoOptimo)
        Cont += 1
        if (Cont >= 10):
            break

    ImprimirFullCorpus( listaPalabrasOrdenadas )
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
        '4': GenerarHashmap
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
