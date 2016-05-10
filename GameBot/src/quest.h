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
uint8_t tQuest_test_color(long color);

#endif

