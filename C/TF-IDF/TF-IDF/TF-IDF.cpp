#include <dirent.h>
#include <io.h>
#include<unistd.h>
#include <ctype.h>       
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include "uthash.h"
#define maxArchivos 4
#define numPalabras 100

typedef struct Lista {
	char *nombrePalabra;
	int frecuencias[maxArchivos];
	UT_hash_handle hh;

}Lista;


void ingresarArchivo(FILE *archivo, int indice);
void addPalabra(char *name, int indice);
Lista *buscarPalabra(char *name);
void mostrarPalabras();
int esStopword(char *palabra);
static struct Lista *listaPalabras = NULL; //se declara como estatico para que las funciones puedan modificarlo libremente
void mostrarEstadisticas();
void imprimirArreglo(Lista * arreglo, int tamanoArreglo);
int sumatoriaDeFrecuencias(Lista *tmp);
int frecuency_sort(struct Lista *l1, struct Lista *l2);
void copiarDocumento(char source[], char target[]);
FILE *stopwords = fopen("stopwords.txt", "r");

int main(int argc, char** argv) {
	DIR *dir;
	struct dirent *ent;
	int op, x = -1, h = 0;
	char source[200] = "";
	//char source[200] = "C:\\Users\\MIRIAM\\Desktop\\edi\\ESPOL\\LibrosDeProgramacion";
	char target[200] = "C:\\Users\\HOME\\Desktop\\ProyectoLenguajes";
	char tmp[200] = "";
	//	char *dirOrigen = (char *)malloc(200);
	//char * cadena = (char *)malloc(200);
	//	char * cadena2 = (char *)malloc(200);
	char * palabra = (char *)malloc(200);
	FILE *f;
	//FILE *f2 = fopen("1.txt", "r");
	op = 0;
	//	ingresarArchivo(f2, 0);
	//	mostrarPalabras();

	while (op != 5){
		printf("Seleccione una opcion: \n 1.-Ingrese archivos \n 2.-Eliminar palabras \n 3.-Ingresar Palabras de Busqueda \n 4.-Mostrar Estadisticas \n 5.-Salir \n");
		scanf("%i", &op);


		switch (op){
		case 1:
			printf("Ingrese el directorio de los archivos: \n");
			scanf("%s", source);
			strcpy(tmp, source);
			if ((dir = opendir(source)) != NULL) {
				/* print all the files and directories within directory */
				while ((ent = readdir(dir)) != NULL) {
					strcat(source, "\\");
					strcat(source, ent->d_name);
					printf("%s \n", source);
					strcat(target, "\\");
					strcat(target, ent->d_name);
					copiarDocumento(source, target);
					if (strcmp(ent->d_name, ".") != 0 && strcmp(ent->d_name, "..") != 0){
						f = fopen(ent->d_name, "r");
						ingresarArchivo(f, h);
						h++;
					}
					strcpy(source, tmp);
					strcpy(target, "C:\\Users\\HOME\\Desktop\\ProyectoLenguajes");

					//printf ("%s\n", ent->d_name);
				}


				closedir(dir);
			}
			else {
				/* could not open directory */
				perror("");
				return EXIT_FAILURE;
			}
			//strcpy(source, target);
			/*	if ((dir = opendir (source)) != NULL) {
			while ((ent = readdir (dir)) != NULL) {
			if(x>0){
			strcat(source,"\\");
			strcat(source, ent->d_name );
			f = fopen(source, "r");
			ingresarArchivo(f, h);
			x++;
			h++;
			strcpy(source, tmp);
			}
			}*
			}*/
			//  mostrarPalabras();
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
			mostrarEstadisticas();
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
	int tamanoArchivo = ftell(archivo);//nos devuelve el tamaño del texto 
	char *str = (char *)malloc(tamanoArchivo);
	fseek(archivo, 0, SEEK_SET);

	for (i = 0; i < tamanoArchivo; i++)
	{
		fscanf(archivo, "%c", &str[i]);
	}

	str = strlwr(str);
	pch = strtok(str, " ,.-!\n\"\?\\\v\f\r\b\'!¡¿?0123456789)({}[]&%$#@|");//Tokeniza el arreglo de chars generado arriba

	while (pch != NULL)//Mientras siga encontrando palabras tokenizadas
	{
		if (esStopword(pch) == 0){
			addPalabra(pch, indice);
		}
		pch = strtok(NULL, " ,.-\n\"\?\\\v\f\r\b\'!¡¿?0123456789)({}[]&%$#@|");

	}
}

int esStopword(char *palabra){
	int i, esStop = 0;
	char *s;
	fseek(stopwords, 0, SEEK_END);
	int tamanoStopwords = ftell(stopwords); //nos devuelve el tamaño del texto de stopwords
	char *stop = (char *)malloc(tamanoStopwords);
	fseek(stopwords, 0, SEEK_SET);

	for (i = 0; i < tamanoStopwords; i++)
	{
		fscanf(stopwords, "%c", &stop[i]);
	}
	stop = strlwr(stop);
	s = strtok(stop, "\n");
	while (s != NULL){
		//printf("%i", stricmp(palabra,s));
		if (stricmp(palabra, s) == 0){
			esStop = 1;
		}
		s = strtok(NULL, "\n");
	}
	return esStop;
}

//añade una nueva palabra con arreglo de frecuencias inicializado en cero
//y si encuentra una existente igual, le suma uno a la frecuencia
void addPalabra(char *name, int ind) {
	struct Lista *s, *h;
	int arr[maxArchivos] = { 0 };
	HASH_FIND_STR(listaPalabras, name, s);

	if (s == NULL){//Si no encuentra la palabra la añade
		s = (struct Lista*)malloc(sizeof(struct Lista));
		s->nombrePalabra = name;
		arr[ind] = 1;
		memcpy(s->frecuencias, arr, maxArchivos * sizeof(int));//copia lo que se encuentra en arr dentro de s->frecuencias
		strcpy(s->nombrePalabra, name);
		HASH_ADD_STR(listaPalabras, nombrePalabra, s);
	}
	else {
		memcpy(arr, s->frecuencias, maxArchivos * sizeof(int));//copia lo que se encuentra en s->frecuencias dentro de arr
		arr[ind] = arr[ind] + 1;//añade uno a la frecuencia de la palabra
		h = (Lista*)malloc(sizeof(Lista));
		h->nombrePalabra = name;
		memcpy(h->frecuencias, arr, maxArchivos * sizeof(int));
		HASH_REPLACE_STR(listaPalabras, nombrePalabra, h, s);//remplaza el valor dentro del mapa
	}
}

//busca una palabra dentro del mapa
Lista *buscarPalabra(char *name) {
	struct Lista *s;
	HASH_FIND_STR(listaPalabras, name, s);  /* s: output pointer */
	return s;
}

void mostrarPalabras(){
	struct Lista *s;
	int i;
	//HASH_SORT(listaPalabras, frecuency_sort);
	for (s = listaPalabras; s != NULL; s = (Lista*)(s->hh.next)) {
		printf("\n%s-> ", s->nombrePalabra);
		for (i = 0; i<maxArchivos; i++){
			printf("%i, ", s->frecuencias[i]);
		}
	}
}

void mostrarEstadisticas(){
	struct Lista *s;
	int i, j = 0;
	HASH_SORT(listaPalabras, frecuency_sort);
	for (s = listaPalabras; j<50; s = (Lista*)(s->hh.next)) {
		printf("\n%s-> ", s->nombrePalabra);
		j++;
		for (i = 0; i<maxArchivos; i++){
			printf("%i, ", s->frecuencias[i]);
		}
	}
}
/*
void mostrarEstadisticas() {
/*Esta función primero debe extraer los datos del hasmap que contiene las palabras con sus frecuencias
Luego, para mostrar las estadísticas por documento, debe ordenarlas por frecuencias
Debo extraer los datos del hashmap y almacenarlos en un arreglo para poder ahí ordenarlos por su frecuencia total
*/
/*
struct Lista *arreglo =(Lista *) malloc(numPalabras * sizeof (Lista));	//aún debo ver como voy a definir ese numPalabras
struct Lista *s = NULL;
int i = 0;
int tamanoArreglo = sizeof(arreglo) / sizeof(Lista);
/*Esta parte del codigo deberia guardar los elementos dentro del hashmap a un array dinamico de Lista*/
/*	for (s = listaPalabras; s != NULL; s = (Lista *)(s->hh.next)) {
//	arreglo[i] = s;
i++;
}
/*Ahora ya tengo todos los elementos dentro del array, falta ordenarlos*/
//	HASH_SORT(listaPalabras, frecuency_sort);

/*Ya ordenado, hay que imprimir las estadísticas*/
//	imprimirArreglo(*arreglo, tamanoArreglo);
//}*/

void imprimirArreglo(Lista *arreglo, int tamanoArreglo) {
	Lista *tmp;
	int i, j;
	char *str1 = (char *)malloc(200);
	//char str1[100];
	char *idn = (char *)malloc(200);
	/*Esta parte imprime la cabecera de la tabla*/
	printf("Terminos \t");
	for (i = 0; i<maxArchivos; i++) {
		int j = i + 1;
		//strncpy(str1, "Documento", 100);
		str1 = "Documento";
		//strcat(str1, "Documento");
		strcat(str1, (char *)j);
		strcat(str1, "\t");
		printf(str1);

		//printf("Documento" + j + "\t");
	}
	//printf("Frecuencia Total");
	printf("\n");
	/*Esta parte imprime los 50 primeros datos de la tabla*/
	for (i = 0; i<50; i++) {
		tmp = &arreglo[i];
		printf("%s \t", tmp->nombrePalabra);
		for (j = 0; j<maxArchivos; j++) {

			printf("%i /t", tmp->frecuencias[j]);
		}
		//printf("%i", tmp.frecuenciaTotal);
		printf("\n");
	}
}



int sumatoriaDeFrecuencias(Lista *tmp) {
	int i, sum;
	sum = 0;
	for (i = 0; i<maxArchivos; i++) {
		sum = sum + tmp->frecuencias[i];
	}
	return sum;
}

int frecuency_sort(struct Lista *l1, struct Lista *l2) {
	/*
	Retorna:
	positivo si l1 > l2
	0 si l1 = l2
	negativo si l1 < l2
	*/
	int f1, f2;
	f1 = sumatoriaDeFrecuencias(l1);
	f2 = sumatoriaDeFrecuencias(l2);
	return f1<f2;
}

void copiarDocumento(char source[], char target[]){
	char ch;
	FILE *sourceF, *targetF;

	sourceF = fopen(source, "r");
	targetF = fopen(target, "w");
	while ((ch = fgetc(sourceF)) != EOF)
		fputc(ch, targetF);
	printf("File copied successfully.\n");
	fclose(sourceF);
	fclose(targetF);
}


