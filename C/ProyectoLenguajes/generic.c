
#include <generic.h>
#include <stdlib.h>

/**
* @file generic.c
* @brief Este archivo contiene la implementacion del 
* TDA Generic que representa a cualquier tipo de dato. Una variable
* Generic puede ser asignada a cualquier tipo de puntero, se le
* puede recuperar su valor y modificar su valor con las funciones
* aqui especificadas.
*
* @author Marcelo Loor
* @author Marisol Villacres
* @author Veronica Macias
*
* @date 10/26/2011
*/
Generic integerNew(int newvalue){
    Generic g;
    g = malloc(sizeof(int));
    *(int *)g = newvalue;
    return g;
}
void integerSet(Generic g, int newvalue)
{
    *(int *)g = newvalue;
}

int integerGet(Generic g){
    int valor = *(int *)g;
    return valor;

}

int integerCmp(Generic a, Generic b){
    if(integerGet(a) == integerGet(b)) return 0;
    else if(integerGet(a) > integerGet(b)) return 1;
    return -1;
}

int integerMax(Generic a, Generic b){
    if(integerGet(b) > integerGet(a)) return 1;
    return 0;
}

int integerMin(Generic a, Generic b){
    if(integerGet(b) < integerGet(a)) return 1;
    return 0;
}

void integerPrint(Generic *g){
    printf("%d ",integerGet(g));
}


Generic charNew(char newvalue){
    Generic g;
    g = malloc(sizeof(char));
    *(char *)g = newvalue;
    return g;
}

void charSet(Generic g, char newvalue){
    *(char *)g = newvalue;
}

char charGet(Generic g){
    char valor = *(char *)g;
    return valor;
}

void charPrint(Generic *g){
    printf("%c",charGet(g));
}

int charCmp(Generic a, Generic b){
    if(charGet(a) == charGet(b)) return 0;
    else if(charGet(a) > charGet(b)) return 1;
    return -1;

}

int compareWithOrderType(Generic g, Generic h, cmpfn cmp, int type){
        if(type == 0)
            return (cmp(g,h) <=0);
        else if(type == 1)
            return (cmp(g,h) > 0);
}


