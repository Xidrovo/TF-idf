

#include <ctype.h>       
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include "uthash.h"
#define maxArchivos 100

typedef struct Lista {
    char *nombrePalabra;
    int *frecuencias;
    UT_hash_handle hh; 
    
}Lista;


void ingresarArchivo(FILE *archivo, int indice);
void addPalabra(char *name, int indice);
Lista *buscarPalabra(char *name);

int main(int argc, char** argv) {

    int op;
    char *dirOrigen = malloc(200);
    char * cadena = malloc(200);
    char * cadena2 = malloc(200);
    char * palabra = malloc(200);
    static struct Lista *listaPalabras = NULL; //se declara como estatico para que las funciones puedan modificarlo libremente
    FILE *f1 = fopen("Doc2.txt", "r");
    //cadena = archivoaChar(f1);
    op = 0;
    while(op!=5){
        printf("Seleccione una opcion: \n 1.-Ingrese archivos \n 2.-Eliminar palabras \n 3.-Ingresar Palabras de Busqueda \n 4.-Mostrar Estadisticas \n 5.-Salir \n");
        scanf("%i", &op);
    
        switch(op){
            case 1:
                printf("Ingrese el directorio de los archivos: \n");
                scanf("%s", dirOrigen);
                strcat(cadena2, "Robocopy");
                strcat(cadena2, dirOrigen);
                strcat(cadena2, "C:Users/Home/Documents/GitHub/TF-idf/C/ProyectoLenguajes/Carpetas/Destino/Destino/Destino /E");
                system(cadena2);
                //system( "ROBOCOPY " + cadena + " C:/Users/MIRIAM/Documents/NetBeansProjects/C/ProyectoLenguajes/Carpetas/Destino /E");              
                break;
            case 2:
                printf("Ingrese las palabras a eliminar: \n");
                scanf("%s", palabra);
                break;
            case 3:
                printf("Ingresar palabras de búsqueda: ");
                scanf("%s", palabra);
                break;
            case 4:
                break;
        }
    }
    

    
    return (EXIT_SUCCESS);
}

//Convierte un archivo a un arreglo de chars, lo tokeniza e ingresa sus palabras a un hashmap
void ingresarArchivo(FILE *archivo, int indice){ 
    int i;
    char * pch;
    fseek(archivo, 0, SEEK_END); 
    int tamanoArchivo = ftell(archivo); //nos devuelve el tamaño del texto
    char *str= malloc(tamanoArchivo);
    fseek(archivo,0,SEEK_SET);
    
    for(i = 0; i < tamanoArchivo; i++)
    {
          fscanf(archivo, "%c", &str[i]);
    }
    for ( ; *str; ++str) *str = tolower(*str);//pasa todo el texto a minusculas  
    pch = strtok (str," ,.-\n");//Tokeniza el arreglo de chars generado arriba
    
    while (pch != NULL)//Mientras siga encontrando palabras tokenizadas
    {
        addPalabra(pch,indice);  
        pch = strtok (NULL, " ,.-\n\"");
    }  
   }

//añade una nueva palabra con arreglo de frecuencias inicializado en cero
//y si encuentra una existente igual, le suma uno a la frecuencia
void addPalabra(char *name,int ind) {
    struct Lista *s;
    int arr[maxArchivos]={0};
    HASH_FIND_STR(listaPalabras, *name, s );
    
    if(s==NULL){//Si no encuentra la palabra la añade
        s = (struct Lista*)malloc(sizeof(struct Lista));
        s->nombrePalabra= name;
        arr[ind]=1;
        s->frecuencias= *arr ;
        strcpy(s->nombrePalabra, name);
        HASH_ADD_STR(listaPalabras,nombrePalabra, s); 
    }
    else {
        arr=s->frecuencias;
        arr[ind]= arr[ind] + 1;//añade uno a la frecuencia de la palabra
        HASH_REPLACE(hh, listaPalabras, nombrePalabra, strlen(name), *arr, s->*frecuencias);//remplaza el valor dentro del mapa
    }
}

//busca una palabra dentro del mapa
Lista *buscarPalabra(char *name) {
    struct Lista *s;
    HASH_FIND_STR(listaPalabras, *name, s );  /* s: output pointer */
    return s;
}



