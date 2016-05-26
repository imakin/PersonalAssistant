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
	
	printlog("processing next node\n");
	while (all_stop!=1)
	{
		while (all_stop!=1)
		{
			/*step += 1;
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
			AU3_Sleep(200);*/
			
			/* here we search for the next node button */
			
			//TODO: NOt bruteforce search but start looking at current node and its white link instead 
			// for faster performance
			
			//prepare memory to save the result
			free(pixelsearch_result);
			pixelsearch_result = malloc(30*sizeof(uint32_t));
			
			
			pixelsearch_skip = 5;
			pixelsearch_node_range_min = 50;
			pixelsearch_nothread(
					mysearch,
					//~ 0,
					//~ 430,270,
					//~ 540,340,
					474,292,
					502,314,
					&quest_testcolor_nodemid,
					PIXELSEARCH_FLAG_EXITONFOUND
				);
			
			//we can assume there only 1 found for mid node
			AU3_MouseMove(
							(long)(pixelsearch_result[0]>>16),
							(long)(pixelsearch_result[0]&0x0000ffff),
							10
						);
			long midx, midy;
			midx = pixelsearch_result[0]>>16;
			midy = (long)(pixelsearch_result[0]&0x0000ffff);
			
			pixelsearch_skip = 1;
			printlog("search node North\n");
			printf("found status %d\n",
				quest_find_nodes(midx-15, midy-60,
							midx+15, midy-58)
			);
			
			printlog("search node North East\n");
			printf("found status %d\n",
				quest_find_nodes(midx+50, midy-45,
							midx+60, midy-30)
			);
			
			printlog("search node East\n");
			printf("found status %d\n",
				quest_find_nodes(midx+58, midy-15,
							midx+60, midy+15)
			);

			printlog("search node SouthEast\n");
			printf("found status %d\n",
				quest_find_nodes(midx+30, midy+50,
							midx+45, midy+60)
			);

			printlog("search node South\n");
			printf("found status %d\n",
				quest_find_nodes(midx-15, midy+58,
							midx+15, midy+60)
			);
			
			
			while(1){
				AU3_Sleep(1000);
			}
			
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
		AU3_Sleep(10);
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
	while (tries>0 && pixelsearch_result_num<2)
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
	if (pixelsearch_result_num>1)
	{
		pixelsearch_result_num = 1;//reset
		AU3_MouseMove(
					(long)(pixelsearch_result[1]>>16),
					(long)(pixelsearch_result[1]&0x0000ffff),
					10
				);
		if (quest_test_explored(
					(long)(pixelsearch_result[1]>>16),
					(long)(pixelsearch_result[1]&0x0000ffff)
				))
			return 1;
		return 2;
	}
	else
		return 0;
}
