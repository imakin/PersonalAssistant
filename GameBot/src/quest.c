/**
 * @file quest.c
 * @author Izzulmakin 2016-05-8
 */

#include "quest.h"

void tQuest_init(tQuest *self)
{
	self->next_node = &tQuest_next_node;
}

void tQuest_next_node(tQuest *self)
{
	int8_t step = 0;
	long color;
	int x,y;
	POINT pos;//microsoft doc 
	//~ pos = malloc(sizeof(POINT));
	all_stop = 0;
	long node_found = 0;
	linkedlist *node, *map;
	node = malloc(sizeof(linkedlist));
	node->data1 = NULL;
	node->data2 = NULL;
	node->next = NULL;
	node->prev = NULL;
	
	map = malloc(sizeof(linkedlist));
	map->multinext = NULL;//malloc(3*sizeof(linkedlist*))
	map->prev = NULL;
	
	while (all_stop!=1)
	{
		while (all_stop!=1)
		{
			step += 1;
			if (step==10)
			{
				AU3_MouseClickDrag((lpcwstr)"left", 450, 320, 642, 346, 10);
			}
			else if (step==20)
			{
				AU3_MouseClickDrag((lpcwstr)"left", 450, 320, 200, 200, 10);
				AU3_MouseClickDrag((lpcwstr)"left", 450, 320, 300, 300, 10);
			}
			else if (step==30)
			{
				AU3_MouseClickDrag((lpcwstr)"left", 700, 100, 100, 400, 10);
			}
			else if (step>=40)
			{
				AU3_MouseClickDrag((lpcwstr)"left", 100, 400, 700, 100, 10);
				AU3_MouseClickDrag((lpcwstr)"left", 100, 400, 700, 100, 10);
				step = 0;
			}
			AU3_Send((lpcwstr)"J",0);
			AU3_Sleep(200);
			
			AU3_ToolTip((lpcwstr)"I'm processing the possible node searching", 100, 100);
			/* here we search for the next node button */
			for (y=245; y<525; y+=5)
			{
				for (x=80;x<955; x+=5)
				{
					
					color = AU3_PixelGetColor(x, y);
					if (
						   (color>0x002200)
						&& ((color&0xff0000) == 0)
						&& ((color&0x0000ff)==0x000000)
					)
					{
						// only test if not the first occurence
						if (node->prev!=NULL)
						{
							// test if node is already saved
							if (abs(x-node->prev->data1)<70)
							if (abs(y-node->prev->data2)<70)
								continue;
							//Following way is slower
							/*if ( sqrt(
									pow(y - node->prev->data2, 2)+
									pow(x - node->prev->data1, 2)
								) < 70)
								continue;*/
						}
						
						node->data1 = x;
						node->data2 = y;
						node->next = malloc(sizeof(linkedlist));
						node->next->prev = node;
						node = node->next;
						node_found += 1;
					}
				}
			}
			//TODO: save it in map
			node = node->prev; //current pointer is empty
			while (node!=NULL)
			{
				printf("found in (%d,%d)\n", node->data1, node->data2);
				node = node->prev;
			}
			printf("\n%d \n", node_found);
			return;
			//~ if (AU3_error())
				//~ AU3_PixelSearch(80,100, 957,530, 0x00e400, 0,1, pos);
			//~ if (!AU3_error())
				//~ break;
		}
		AU3_Send((lpcwstr)"J",0);
		//~ AU3_MouseMove(pos.x, pos.y, 10);
		//~ AU3_ToolTip((lpcwstr)"I will click this in 4", pos.x, pos.y);
		return;
	}
}
