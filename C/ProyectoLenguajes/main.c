

#include <ctype.h>       
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include "tinydir.h"

char * archivoaChar(FILE *archivo);

int main(int argc, char** argv) {
    
    int op, flag1;
    char * cadena = malloc(200);
    char * cadena2 = malloc(200);
    char * palabra = malloc(200);
    op = 0;
    while(op!=5){
        printf("Seleccione una opcion: \n 1.-Ingrese archivos \n 2.-Eliminar palabras \n 3.-Ingresar Palabras de Busqueda \n 4.-Mostrar Estadisticas \n 5.-Salir \n");
        scanf("%i", &op);
    
        switch(op){
            case 1:
                printf("Ingrese el directorio de los archivos: \n");
                scanf("%s", cadena);
                strcat(cadena2, "Robocopy");
                strcat(cadena2, cadena);
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

//Convierte un archivo a un arreglo de chars y lo retorna
char * archivoaChar(FILE *archivo){ 
    int i;
    fseek(archivo, 0, SEEK_END); 
    int tamanoArchivo = ftell(archivo); //nos devuelve el tamaño del texto
    char *str= malloc(200);
    fseek(archivo,0,SEEK_SET);
    for(i = 0; i < tamanoArchivo; i++)
    {
          fscanf(archivo, "%c", &str[i]);
    }
    getchar();
    return str;
}


