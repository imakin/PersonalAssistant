#include "arena.h"


uint8_t arena_tier = 2;
uint8_t arena_continue = 1;
uint8_t arena_stop  = 0;

void arena_change_tier()
{
	if (arena_tier==2)
	{
		arena_tier = 3;
		printlog("arena tier is now 3");
	}
	else if (arena_tier==3)
	{
		arena_tier = 4;
		printlog("arena tier is now all tier, no event");
	}
	else
	{
		arena_tier = 2;
		printlog("arena tier is now 2");
	}
}

void start_arena()
{
	arena_stop = 0;
	while (1) 
	{
		calibrate_window();
		sleep(500);
		AU3_MouseClickDrag("left", 130, 255, 700, 255, 10);
		sleep(1000);
		
		//~ if (!(
		
	}
}


