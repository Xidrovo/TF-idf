/**
   \mainpage TDA Generic \n Estructura de Datos 
   <br>
   Profesores: Angel Lopez, Daniel Ochoa, Marisol Villacres <br>
   <hr>
   \author Marisol Villacres
   \author Daniel Ochoa
   \author Angel Lopez
   \date Octubre-2011

   <br><img src="../imagenes/paneta.jpg"><br>
*/

/**
* @file generic.h
* @brief Este archivo contiene la definicion del 
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
#ifndef GENERIC_H
#define	GENERIC_H

#ifdef	__cplusplus
extern "C" {
#endif
    
#include <stdio.h>    
/** @defgroup hs TDA Generic
 * Estas definiciones y funciones componenen el TDA Generic
 * @{
 */
    
/**
* @brief Definicion del tipo de dato Generic, el cual permite crear variables a las cuales se les puede asignar cualquier tipo de dato.
*/
typedef void * Generic;

/**
* @brief Definicion de las funciones que pueden leer una linea de un archivo
 * y retornar un registro de algun TDA en forma de una variable Generica
*/
typedef Generic (*readfn)(FILE *F);

/**
* @brief Definicion de las funciones que dados dos genericos pueden
 * compararlos y retornar 0 si son iguales, 1 si el primero es mayor que el
 * segundo y -1 si el primero es menor que el segundo
*/
typedef int (*cmpfn)(Generic, Generic);

/**
* @brief Definicion de las funciones que dado un generico pueden
 * imprimirlo
*/
typedef void (*printfn) (Generic);

typedef Generic (*getkeyfn) (Generic);
/**
* integerNew permite crear un nuevo entero, asignarle un valor y retornarlo listo
* para almacenarlo en una variable de tipo Generic.
* @author Marisol Villacres
* @param newValue el valor a ser asignado en el nuevo entero
* @return retorna un nuevo entero en forma de Generic
* @date 10/26/2011
*/

/**
* integerNew permite crear un nuevo entero, asignarle un valor y retornarlo listo
* para almacenarlo en una variable de tipo Generic.
* @author Marisol Villacres
* @param newValue el valor a ser asignado en el nuevo entero
* @return retorna un nuevo entero en forma de Generic
* @date 10/26/2011
*/
Generic integerNew(int newValue);


/**
* integerSet permite asignar un valor entero a una variable de tipo Generic.
* @author Marisol Villacres
* @param g la variable generica cuyo valor se desea modificar
* @param newValue el valor que se va a asignar a la variable g
* @date 10/26/2011
*/
void integerSet(Generic g, int newValue);

/**
* integerGet permite recuperar el valor entero almacenado en una variable Generic.
* @author Marisol Villacres
* @param g la variable Generic
* @return  el valor entero almacenado dentro de un Generic
* @date 10/26/2011
*/
int integerGet(Generic g);


void integerPrint(Generic *g);

int integerCmp(Generic a, Generic b);

int integerMax(Generic a, Generic b);
int integerMin(Generic a, Generic b);

/**
* charNew permite crear un nuevo char, asignarle un valor y retornarlo listo
* para almacenarlo en una variable de tipo Generic.
* @author Marisol Villacres
* @param newValue el valor a ser asignado en el nuevo entero
* @return retorna un nuevo char en forma de Generic
* @date 10/26/2011
*/
Generic charNew(char newValue);

/**
* charSet permite asignar un valor char a una variable de tipo Generic.
* @author Marisol Villacres
* @param g la variable generica cuyo valor se desea modificar
* @param newValue el valor que se va a asignar a la variable g
* @date 10/26/2011
*/

void charSet(Generic g, char newValue);

/**
* charGet permite recuperar el valor char almacenado en una variable Generic.
* @author Marisol Villacres
* @param g la variable Generic
* @return  el valor char almacenado dentro de un Generic
* @date 10/26/2011
*/
char charGet(Generic g);

void charPrint(Generic *g);

int charCmp(Generic a, Generic b);
/** @}
 */

#ifdef	__cplusplus
}
#endif

#endif	/* GENERIC_H */

