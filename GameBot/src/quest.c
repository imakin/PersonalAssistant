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
	all_stop = 0;
	
	printf("processing next node\n");
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
			
			//~ AU3_ToolTip((lpcwstr)"I'm processing the possible node searching", 100, 100);
			/* here we search for the next node button */
			///TODO: use threading, split screen area, and data association
			///TODO: update threading to output all found occurence not only first occurence
			free(pixelsearch_result);
			pixelsearch_result = malloc(30*sizeof(uint32_t));
			//part it from x100-950 y80-530
			pixelsearch_param(param0, 0, 100+(283*0), 80+(150*0), 100+(283*1), 80+(150*1), &tQuest_test_color);
			_beginthread(pixelsearch, 0, (void*)param0);
			pixelsearch_param(param1, 1, 100+(283*1), 80+(150*0), 100+(283*2), 80+(150*1), &tQuest_test_color);
			_beginthread(pixelsearch, 0, (void*)param1);
			pixelsearch_param(param2, 2, 100+(283*2), 80+(150*0), 100+(283*3), 80+(150*1), &tQuest_test_color);
			_beginthread(pixelsearch, 0, (void*)param2);
			
			pixelsearch_param(param3, 3, 100+(283*0), 80+(150*1), 100+(283*1), 80+(150*2), &tQuest_test_color);
			_beginthread(pixelsearch, 0, (void*)param3);
			pixelsearch_param(param4, 4, 100+(283*1), 80+(150*1), 100+(283*2), 80+(150*2), &tQuest_test_color);
			_beginthread(pixelsearch, 0, (void*)param4);
			pixelsearch_param(param5, 5, 100+(283*2), 80+(150*1), 100+(283*3), 80+(150*2), &tQuest_test_color);
			_beginthread(pixelsearch, 0, (void*)param5);
			
			pixelsearch_param(param6, 6, 100+(283*0), 80+(150*2), 100+(283*1), 80+(150*3), &tQuest_test_color);
			_beginthread(pixelsearch, 0, (void*)param6);
			pixelsearch_param(param7, 7, 100+(283*1), 80+(150*2), 100+(283*2), 80+(150*3), &tQuest_test_color);
			_beginthread(pixelsearch, 0, (void*)param7);
			pixelsearch_param(param8, 8, 100+(283*2), 80+(150*2), 100+(283*3), 80+(150*3), &tQuest_test_color);
			_beginthread(pixelsearch, 0, (void*)param8);
			
			while (1){
				int i,j;
				for (i=0;i<1000; i++)
				for (j=0;j<1000; j++);
			}
			//~ while (pixelsearch_result_num==0)
				//~ AU3_Sleep(100);
		}
		AU3_Send((lpcwstr)"J",0);
		return;
	}
}

uint8_t tQuest_test_color(long color)
{
	if (
		   (color>0x002200)
		&& ((color&0xff0000)==0)
		&& ((color&0x0000ff)==0)
	)
		return 1;
	return 0;
}
