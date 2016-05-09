/**
 * @file common.h
 * @author Izzulmakin 2016-05-10
 */

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


extern uint8_t makin_pixelsearch_skip;
/**
 * pixel search color with threading
 * @see makin_pixelsearch_param
 * @param param is a pointer to a set of 5 datas, comprises:
 * 	- 	4 long* starts from index 0 to 3 is x1,y1,x2,y2 which represent 
 * 		the rectangle area to search.
 * 	-	index 4 is the function pointer to the test of the color 
 * 		will be called like test_color(color_value) and shall return 1 for true, 0 for false
 */ 
void makin_pixelsearch(void *param);


/**
 * create a param named "name" to be used in makin_pixelsearch
 * @param name the name of the param variable
 * @param x1 the area to search rectangle x1
 * @param y1 the area to search rectangle y1
 * @param x2 the area to search rectangle x2
 * @param y2 the area to search rectangle y2
 * @param test_color the method for the color test to search
 * 		this shall be defined in uint8_t test_methodname(long color)
 * 		and must return 1 if color match desired color, or return 0 if not
 */
#define makin_pixelsearch_param(name, x1,y1, x2,y2, test_color) \
	uint32_t *name; \
	name = malloc(4*sizeof(uint32_t) + sizeof(*test_color)); \
	name[0] = x1; \
	name[1] = y1; \
	name[2] = x2; \
	name[3] = y2; \
	name[4] = &test_color;


#endif
