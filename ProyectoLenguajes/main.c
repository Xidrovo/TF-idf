

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <dirent.h>


/*
 * 
 */
int main(int argc, char** argv) {
    DIR *dp;
    struct dirent *ep;
    int op, flag1;
    char * cadena = malloc(200);
    char * palabra = malloc(200);
    printf("Seleccione una opcion: \n 1.-Ingrese archivos \n 2.-Eliminar palabras \n 3.-Ingresar Palabras de Busqueda \n 4.-Mostrar Estadisticas \n 5.-Salir \n");
    scanf("%i", &op);
    while(op!=5){
        switch(op){
            case 1:
                printf("Ingrese el directorio de los archivos: \n");
                scanf("%s", cadena);
                dp = opendir();
                
                // system("copy C:\origen\archivo1.txt C:\destino")
                // system("")
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

