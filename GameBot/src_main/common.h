/**
 * @file common.h
 * @author Izzulmakin 2016-05-10
 * provide commonly used api
 */

#ifndef __COMMON_H__
#define __COMMON_H__

#include <Windows.h>
#include "../lib/AutoIt3.h"
//~ #include "../lib/new/AutoItX3_DLL.h" //CPP
#include <stdint.h>
#include <stdio.h>
#include <math.h>

/** my custom api in Django */
/** global pointer refer to value returned by cloud_data_read */
extern char * cloud_data_value;
/** read data in server */
char * cloud_data_read(char *name);
/** write data in server */
void cloud_data_write(char *name, char *value);

#define sleep(ms) AU3_Sleep(ms)

typedef LPCWSTR lpcwstr;

/** allstop flag, if 1 then must go idle */
extern uint8_t all_stop;

typedef struct linkedlist_st linkedlist;
struct linkedlist_st {
	long *data;
	linkedlist *next;
	linkedlist **multinext;
	linkedlist **multiprev;
	linkedlist *prev;
	
	void (*push)(linkedlist *self, linkedlist *new_data);
	linkedlist * (*tail)(linkedlist *self);
	/// TODO: if required linkedlist * (*destroy_tail)(linkedlist *self);
};
/**
 * create linkedlist object <br/>
 * usages: linkedlist *linkedlistpointer = new_linkedlist(linkedlistpointer)
 */
#define linkedlist_new(self) \
	malloc(sizeof(linkedlist)); \
	self->next = 0; \
	self->prev = 0;
	

/** windows */
#define popen _popen
#define pclose _pclose

/**
 * execute program and get stdoutput. 
 * Node pls free the return value manually when done using
 * @param cmd cmd string to be executed in shell
 */
char* exec(char* cmd);

extern wchar_t debugstring[200];

/** log prints only if DEBUG is not 0 */
#define DEBUG 1
/** log prints only if DEBUG is not 0 */
#if DEBUG==1
	#define printlog(...) printf(__VA_ARGS__)
#else
	#define printlog(...) (void)(__VA_ARGS__)
#endif
	//~ wsprintfW(debugstring, format, __VA_ARGS__); \
	//~ AU3_ToolTip((LPCWSTR)debugstring, 100,750);
	//~ printf
	


#endif
