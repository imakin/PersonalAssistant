/**
 * @file quest.c
 * @author Izzulmakin 2016-05-8
 */

#include "quest.h"

linkedlist* node_stack;
uint8_t node_stack_step = 0;

void tQuest_init(tQuest *self)
{
	self->next_node = &tQuest_next_node;
	
	//prepare memory to save the result
	free(pixelsearch_result);
	pixelsearch_result = malloc(30*sizeof(uint32_t));
	node_stack = linkedlist_new(node_stack);
}

void tQuest_next_node(tQuest *self)
{
	int8_t step = 0;
	long color;
	int x,y;
	all_stop = 0;

	
	printlog("processing next node\n");
	while (all_stop!=1)
	{
		while (all_stop!=1)
		{
			//settings
			pixelsearch_skip = 3;
			pixelsearch_node_range_min = 50;
			pixelsearch_result_num = 0;
			int tries;
			for (tries=0;tries<1; tries++)
			{
				pixelsearch_refresh_image();
				pixelsearch_nothread(
					greensearch,
					80,100,
					957, 530,
					&quest_testcolor_nodegreen,
					PIXELSEARCH_FLAG_DEFAULT
				);
			}
			int iii;
			//~ char *buff = malloc(sizeof(char)*64);
			char buff[64];
			char *buff_nodes = malloc(sizeof(char)*100);
			buff_nodes[0] = 0;
			for (iii=0;iii<pixelsearch_result_num;iii++)
			{
				sprintf(buff, "%d_", pixelsearch_result[iii]
					);
				strcat(buff_nodes, buff);
				AU3_MouseMove(
							(long)(pixelsearch_result[iii]>>16),
							(long)(pixelsearch_result[iii]&0x0000ffff),
							10
						);
				AU3_Sleep(2000);
			}
			printlog(buff_nodes);
			if (pixelsearch_result_num>1)
				cloud_data_write("multiplenextnode", buff_nodes);
			free(buff_nodes);
			
			long action;
			uint8_t found=0;
			while (found!=1) {
				action = (long)atoi(cloud_data_read("multiplenextnode_pick"));
				for (iii=0;iii<pixelsearch_result_num;iii++)
				{
					if (action==pixelsearch_result[iii]){
						found=1;
						break;
					}
				}
				AU3_Sleep(1000);
			}
			printlog("\nordered to go %x: (%d,%d)\n", action, action>>16, action&0x0000ffff);
			//~ free(buff);
			AU3_MouseMove(action>>16, action&0x0000ffff, 10);
			printlog("will click this in 4 seconds\n");
			AU3_Sleep(4000);
			AU3_MouseClick((lpcwstr)"LEFT", (long)(action>>16), (long)(action&0x0000ffff), 10, -1);
			exec("click.exe");
			printlog("clicked\n");
			AU3_Sleep(1000);
		}
		AU3_Send((lpcwstr)"J",0);
		return;
	}
}

/** search for explorable greendot 
 * @param color test color bgr value 
 * @param x test position
 * @param y test position */
uint8_t quest_testcolor_nodegreen(long color, long x, long y)
{
	if (
		   (color>0x002200)
		&& ((color&0xff0000)==0)
		&& ((color&0x0000ff)==0)
	)
		return 1;
	return 0;
	//~ if (color==0x00f800 || color==0x00e400){
		//~ printlog("found color is %x ",color);
		//~ return 1;
	//~ }
	//~ return 0;
		
}


/**
 * search for path
 * @param color test color BGR value 
 * @param x test position
 * @param y test position 
 * @return 0 false 1 true
 */
uint8_t quest_testcolor_path(long color, long x, long y)
{
	int r,g,b;
	r = (int) (color & 0x0000ff);
	g = (int) ((color & 0x00ff00) >> 8);
	b = (int) (color >> 16);
	
	if ( (g>r) && (b>r) && (g>200) && (b>200) )
	{
		return 1;
	}
	return 0;
}


/** search for mid, blue dot where we currently in 
 * @param color test color BGR value 
 * @param x test position
 * @param y test position 
 * @return 0 false 1 true 
 * */
uint8_t quest_testcolor_nodemid(long color, long x, long y)
{
	int r,g,b;
	r = (int) (color & 0x0000ff);
	g = (int) ((color & 0x00ff00) >> 8);
	b = (int) (color >> 16);
	if (
		(g-r) > 40 && 
		(b-r) > 40
	) {
		// avoid cosmic class logo from Saturation calculation cdif/cmax 
		// with (cmax!=0)
		// cosmic class logo might found in gate node
		if (  (g>b) && (((g-r)*100/g) > 50)  )
				return 0;
		else if (((b-r)*100/b) > 50)
				return 0;
		printlog("sat : %d, %d\n", (((g-r)*100/g)), (((b-r)*100/b)));
		
		//~ AU3_MouseMove(x,y,10);
		int found=pixelsearch_result_num;
		//NEXT CHECK
		pixelsearch_skip = 3;
		pixelsearch_node_range_min = 3;
		
		printlog("check left. ");
		pixelsearch_nothread(
					left,
					x-20, y-1,
					x+1, y+1,
					&quest_testcolor_nodehousing,
					PIXELSEARCH_FLAG_EXITONFOUND
				);
		
		if (pixelsearch_result_num==found)
		{
			pixelsearch_skip = 3;
			pixelsearch_node_range_min = 50;
			return 0;
		}
		
		printlog("check right. ");
		pixelsearch_nothread(
					right,
					x-1, y-1,
					x+20, y+1,
					&quest_testcolor_nodehousing,
					PIXELSEARCH_FLAG_EXITONFOUND
				);
		
		if (pixelsearch_result_num==found)
		{
			pixelsearch_skip = 3;
			pixelsearch_node_range_min = 50;
			return 0;
		}
		
		printlog("check up. ");
		pixelsearch_nothread(
					upper,
					x-1, y-20,
					x+1, y+1,
					&quest_testcolor_nodehousing,
					PIXELSEARCH_FLAG_EXITONFOUND
				);
		
		if (pixelsearch_result_num==found)
		{
			pixelsearch_skip = 3;
			pixelsearch_node_range_min = 50;
			return 0;
		}
		
		printlog("check bottom. ");
		pixelsearch_nothread(
					bottom,
					x-1, y-1,
					x+1, y+20,
					&quest_testcolor_nodehousing,
					PIXELSEARCH_FLAG_EXITONFOUND
				);
		
		if (pixelsearch_result_num==found)
		{
			pixelsearch_skip = 3;
			pixelsearch_node_range_min = 50;
			return 0;
		}
		
		pixelsearch_skip = 3;
		pixelsearch_node_range_min = 50;
		pixelsearch_result_num = found;
		return 1;
	}
	return 0;
}

/**
 * test if this color is housing of node 
 */
uint8_t quest_testcolor_nodehousing(long color, long x, long y)
{
	int r,g,b;
	r = (int) (color & 0x0000ff);
	g = (int) ((color & 0x00ff00) >> 8);
	b = (int) (color >> 16);
	if (abs(r-g) < 15)
	if (abs(r-b) < 15)
		return 1;
	return 0;
}

/** test if this path is explored path or not 
 * @param x path test x point
 * @param y path test y point
 * @return 0 if not explored
 * */
uint8_t quest_test_explored(long x, long y)
{
	int i;
	for (i=0; i<30; i++)
	{
		if (quest_testcolor_path(AU3_PixelGetColor(x,y), x, y))
		{
			return 0;
		}	
		AU3_Sleep(50);
	}
	return 1;
}


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
uint8_t quest_find_nodes(long x1, long y1, long x2, long y2)
{
	int tries = 3;
	int orig_result = pixelsearch_result_num;
	while (tries>0 && pixelsearch_result_num==orig_result)
	{
		pixelsearch_nothread(
						mypath,
						x1, y1,
						x2, y2,
						&quest_testcolor_path,
						PIXELSEARCH_FLAG_EXITONFOUND
					);
		tries-=1;
	}
	if (pixelsearch_result_num>orig_result)
	{
		AU3_MouseMove(
					(long)(pixelsearch_result[pixelsearch_result_num-1]>>16),
					(long)(pixelsearch_result[pixelsearch_result_num-1]&0x0000ffff),
					10
				);
		if (quest_test_explored(
					(long)(pixelsearch_result[pixelsearch_result_num-1]>>16),
					(long)(pixelsearch_result[pixelsearch_result_num-1]&0x0000ffff)
				))
		{
			pixelsearch_result_num = orig_result;
			return 1;
		}
		pixelsearch_result_num = orig_result;
		return 2;
	}
	else
		return 0;
}
