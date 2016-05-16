/**
 * @file quest.h
 * @author Izzulmakin 2016-05-8
 */
#ifndef __QUEST_H__
#define __QUEST_H__

#include "common.h"

typedef struct quest_st tQuest;
struct quest_st{
	/**
	 * all method linking goes here
	 */
	void (*init)(tQuest *self);
	/**
	 * Quest battlerealm pick next node
	 */
	void (*next_node)(tQuest *self);
};

/**
 * initialize quest object
 * @param name the name of object to be created
 */
#define Quest_new(name)\
	tQuest *name = malloc(sizeof(tQuest)); \
	name->init = &tQuest_init; \
	name->init(name);

void tQuest_init(tQuest *self);
void tQuest_next_node(tQuest *self);

/** color test for next node bullet to click */
uint8_t quest_testcolor_nodegreen(long color, long x, long y);


/**
 * search for path
 * @param color test color BGR value 
 * @param x test position
 * @param y test position 
 * @return 0 false 1 true
 */
uint8_t quest_testcolor_path(long color, long x, long y);

/** search for mid, blue dot where we currently in 
 * @param color test color BGR value 
 * @param x test position
 * @param y test position */
uint8_t quest_testcolor_nodemid(long color, long x, long y);

/** search for node housing */
uint8_t quest_testcolor_nodehousing(long color, long x, long y);

/** test if this path is explored path or not 
 * @param x path test x point
 * @param y path test y point
 * */
uint8_t quest_test_explored(long x, long y);

/**
 * find nodes within given search rectangle
 * by calling this function pixelsearch_result_num must be 1 and 
 * pixelsearch_result only contains the mid node
 * @param x1 region
 * @param y1 region
 * @param x2 region
 * @param y2 region
 * @return 0 if not found, 1 if found & explored, 2 if found & unexplored
 */
uint8_t quest_find_nodes(long x1, long y1, long x2, long y2);
#endif

