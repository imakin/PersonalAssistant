#ifndef __COMMON_H__
#define __COMMON_H__

#include <Windows.h>
#include "../lib/AutoIt3.h"
#include <stdint.h>
#include <stdio.h>

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

#endif
