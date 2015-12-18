#include "hashmap.h"
#include <string.h>

void hashMapInit(HashMap M){
	int i;
	for(i=0;i<B;i++){
		M[i].e = EMPTY;
		M[i].key = NULL;
		M[i].value = NULL;
	}
}

void hashMapAdd(HashMap M,Generic key, Generic value){
	unsigned int collision=0, code=hashCode(key);
	while (M[code].e != EMPTY && keyComp(M[code].key,key)!=0)		
		code = reHashCode(code,++collision);
		if (collision>=B) return; // Hash lleno
	if (M[code].e == EMPTY ){
		hashMapSet(M,key,value,FULL,code);
	}
}
void hashMapDel(HashMap M,Generic key){
	hashMapSet(M,key,NULL,DELETE,hashCode(key));
}

Generic hashMapGet(HashMap M, Generic key){
	unsigned int collision=0,code=hashCode(key);
	while(M[code].e == FULL){
		if(keyComp(M[code].key,key)==0)
			return M[code].value;
		code = reHashCode(code, ++collision);
		if (collision>=B) return NULL; // No esta
	}
	return NULL;
}

void hashMapSet(HashMap M, Generic key, Generic value, State e, unsigned int code){
	M[code].key = key;
	M[code].value = value;
	M[code].e = e;
}

int keyComp(Generic key1, Generic key2){
	return strcmp((char*)key1, (char*)key2);
}

unsigned int hashCode(Generic key){
	return (unsigned int)strlen((char *)key)%B;
}
unsigned int reHashCode(unsigned int collision, unsigned int code){
	return (code + collision) % B;
};
