

#include <ctype.h>       
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
//#include "tinydir.h"
#include "generic.h"
#include "hashmap.h"


void ingresarArchivo(FILE *archivo, HashMap map, int indice);

int main(int argc, char** argv) {

    int op;
    char *dirOrigen = malloc(200);
    char * cadena = malloc(200);
    char * cadena2 = malloc(200);
    char * palabra = malloc(200);
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
                strcat(cadena2, " C:/Users/MIRIAM/Documents/NetBeansProjects/C/ProyectoLenguajes/Carpetas/Destino /E");
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
void ingresarArchivo(FILE *archivo, HashMap map, int indice){ 
    int i;
    int doc[100];
    char * pch;
    int aux[1000] = {0};
    fseek(archivo, 0, SEEK_END); 
    int tamanoArchivo = ftell(archivo); //nos devuelve el tamaño del texto
    char *str= malloc(tamanoArchivo);
    fseek(archivo,0,SEEK_SET);
    
    for(i = 0; i < tamanoArchivo; i++)
    {
          fscanf(archivo, "%c", &str[i]);
    }
    //printf("%s", str);
    pch = strtok (str," ,.-\n");//Tokeniza el arreglo de chars generado arriba
    while (pch != NULL)
    {
        //printf ("%s\n",pch);
        if(hashMapGet(map, pch)==NULL){     //Si esa palabra no está en el hashmap
            doc[i]=1;                         //Indica que aparece 1 vez en el documento i
            hashMapAdd(map, pch, doc);        //Anade la palabra y su array 
        }
        else{                                   /*Si se encuentra en el hashmap, toma el value que es un array de enteros, le sma
                                                    1 en la posicion del documento, lo elimina del hashmap y lo vuelve a anadir*/

            
            aux = hashMapGet(map, pch);         //hacer el cast de Generic a int[]

            int aux[] = {0};
            *aux = hashMapGet(map, pch);         //hacer el cast de Generic a int[]
            aux[i]++;
            hashMapSet(map,pch,aux);
            
        }
        pch = strtok (NULL, " ,.-\n\"");
        
    }
    
    
}



