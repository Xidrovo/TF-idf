/**
* @file hashmap.h
* @brief Este archivo contiene la definicion del 
* TDA hashmap que representa a una tabla de hash cerrado
*
* @author Angel L�pez
* @date 09/01/2012
*/
#ifndef HASHMAP_H
#define	HASHMAP_H

#ifdef	__cplusplus
extern "C" {
#endif

#include "generic.h"
/** @defgroup hs TDA hashMap
 * Estas definiciones y funciones componenen el TDA hashMap
 * @{
 */
	#define B 100
	typedef enum {EMPTY,FULL,DELETE} State;
/**
* @brief Definicion del tipo de dato 
*/
typedef struct Cubeta{
	Generic key;
	Generic value;
	State e;
}Cubeta;

typedef Cubeta HashMap[B];

/**
* hashMapInit inicializa la tabla de hash con valores de NULL y EMPTY
* El hast debe ser inicializado antes de usarlo
* @param HashMap Tabla de Hast a ser inicializada
*/
void hashMapInit(HashMap M);
/**
* hashMapAdd Permite agregar un par (clave, valor) a la tabla de hash
* en caso de ya existir esa clave no se inserta (no permite duplicados)
* @param M, Tabla de Hash donde se va a insertar
* @param key, Clave a ser insertada
* @param value, Valor a ser insertado
*/
void hashMapAdd(HashMap M,Generic key, Generic value);
/**
* hashMapDel Permite eliminar un par (clave, valor) a la tabla de hash
* @param M, Tabla de Hash donde se va a eliminar
* @param key, Clave de la cubeta a ser eliminada
*/
void hashMapDel(HashMap M,Generic key);
/**
* hashMapGet Permite obtener el valor de una cubeta dada la clave
* @param M, Tabla de Hash
* @param key, Clave de la cubeta que contiene el valor buscado
* @return Generic con el valor
*/
Generic hashMapGet(HashMap M, Generic key);
/**
* hashCode Funci�n de dispersi�n que genera el codigo donde se debe 
* ubicar el par (clave, valor)
* @param key, Clave para la generaci�n del codigo
* @return int con la posici�n donde se debe guardar
*/
unsigned int hashCode(Generic key);
/**
* reHashCode Funci�n de re-dispersi�n que genera el codigo donde se debe 
* ubicar el par (clave, valor)
* @param collision, n�mero de colisi�n
* @param code, Clave para la generaci�n del codigo
* @return code desplazado basado en la colisi�n
*/
unsigned int reHashCode(unsigned int collision, unsigned int code);
/**
* hashMapSet Permite establecer el par (clave, valor) en una cubeta
* de una posicion especifica
* @param M, Tabla de Hash donde se va a insertar
* @param key, Clave a ser insertada
* @param value, Valor a ser insertado
* @param e, Estado
* @param code, ubicaci�n en la tabla
*/
void hashMapSet(HashMap M, Generic key, Generic value, State e, unsigned int code);
/**
* keyComp funcion de comparaci�n de claves
* @param key1, Clave a ser comparada
* @param key2, Clave a ser comparada
* @return int, 0 si son iguales y diferente caso contrario.
*/
int keyComp(Generic key1, Generic key2);

/** @}
 */

#ifdef	__cplusplus
}
#endif
#endif	/* HASHMAP_H */