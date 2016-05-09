/**
 * @file common.c
 * @author Izzulmakin 2016-05-10
 */
 #include "common.h"


/** allstop flag, if 1 then must go idle */
uint8_t all_stop = 0;

uint8_t makin_pixelsearch_skip = 5;
/**
 * pixel search color with threading
 * @param param is a pointer to a set of 5 datas, comprises:
 * 	- 	4 uint32_t* starts from index 0 to 3 is x1,y1,x2,y2 which  
 * 		represent the rectangle area to search.
 * 	-	index 4 is the function pointer to the test of the color. 
 * 		return value type is uint8_t will be called like 
 * 		param[4](color_value) and shall return 1 for true, 0 for false
 *  -
 */ 
void makin_pixelsearch(void *param)
{
	uint32_t *data = (uint32_t *)param;
	uint8_t (*test_method)(long color);
	test_method = data[4];
	uint32_t x,y;
	long color;
	for (y=data[1]; y<data[3]; y+= makin_pixelsearch_skip)
	for (x=data[0]; x<data[2]; x+= makin_pixelsearch_skip)
	{
		color = AU3_PixelGetColor((long)x, (long)y);
		if (test_method(color))
		{
			AU3_MouseMove((long)x, (long)y, 40);
			return;
		}
	}
	
}

