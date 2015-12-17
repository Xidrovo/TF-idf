__author__ = 'CltControl'
import shutil
import os

op = 1 # variable para switch
HashTable = {} #Hashmap de frecuencias
MAXDOC = 0
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

#Este método requerirá el nombre del documento y un índice del doc.
#Este método me dará un set con las palabras que no están en stopwords las cuales serán usadas para el hashmap.
def GenerarFrecuencias(Documento, indice):
    ListaTemp = []
    StopWords = LeerStopWords()
    setDePalabras = set()
    with open('files\\' + Documento, 'r') as myfile:
        data = myfile.read()
        Palabras = data.split()
        setDePalabras  = (set(Palabras) - set(StopWords))

        for x in setDePalabras:
            Temp = ""
            Temp = x
            ListaTemp = []
            if Temp.lower() in HashTable:
                ListaTemp = HashTable.get(Temp.lower())
                ListaTemp[indice] = ListaTemp[indice] + 1
                print (ListaTemp)
                HashTable[Temp.lower()] = ListaTemp
            else:
                for iteration in range(MAXDOC):
                    ListaTemp.append(0)
                ListaTemp[indice] = 1
                HashTable[x.lower() ] = ListaTemp


        myfile.close()

#Coge los documentos de la carpeta "file"
def GenerarHashmap():
    List = os.listdir("files")
    Cont = 0
    global MAXDOC
    MAXDOC = len(List)
    for x in List:
        GenerarFrecuencias(x, Cont)
        Cont = Cont + 1
    print (HashTable)

#Devuelve una lista con cada palabra del stopword
def LeerStopWords():
    with open('custom\\stopwords.txt', 'r') as myfile:
        data = myfile.read()
        myfile.close()
        return data.split()



def default(): #  default
    print("Opcion Invalida")



#switch
# uso un diccionario (python) como un switch (c )
switch = {
        '1': uno,
        '0': cero,
        '2': dos,
        '3': GenerarHashmap
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