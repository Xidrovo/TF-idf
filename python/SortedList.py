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
                print (NuevaLista)
                if x[1] < NuevaLista[y][1]:
                    NuevaLista.insert(Index, x)
                    booleano = 0
                    break
                Index += 1

            if (booleano == 1):
                NuevaLista.append(x)
    return NuevaLista

lista = []
lista.append(["Hola", 2])
lista.append(["Halo", 4])
lista.append(["Hello", 1])
lista.append(["Holloas", 5])
lista.append(["asdas", 1])


lista = SortList(lista)
print (lista)