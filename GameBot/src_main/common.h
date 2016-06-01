/**
 * @file common.h
 * @author Izzulmakin 2016-05-10
 * provide commonly used api
 */

#ifndef __COMMON_H__
#define __COMMON_H__

#include <Windows.h>
#include "../lib/AutoIt3.h"
#include <stdint.h>
#include <stdio.h>
#include <math.h>


#define sleep(ms) AU3_Sleep(ms)

typedef LPCWSTR lpcwstr;

/** allstop flag, if 1 then must go idle */
extern uint8_t all_stop;

typedef struct linkedlist_st linkedlist;
struct linkedlist_st {
	long data1;
	long data2;
	long data3;
	long data4;
	linkedlist *next;
	linkedlist **multinext;
	linkedlist *prev;
};




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
