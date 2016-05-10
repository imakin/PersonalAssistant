/**
 * @file common.c
 * @author Izzulmakin 2016-05-10
 * provide commonly used api
 */
 #include "common.h"


/** allstop flag, if 1 then must go idle */
uint8_t all_stop = 0;

/** pixelsearch found node minimum range to be recognized as new node
 * in data association */
#define NODE_RANGE_MIN 50

/** where the result saved, in each item array value will be saved 
 * ((x<<16) | y) in which x and y is less than 0xFFFF
 */
uint32_t *pixelsearch_result=NULL;

/** flag valued 1 if a thread is currently updating pixelsearch_result */
uint8_t pixelsearch_result_lock = 0;

/** how much has found / in what index the latest pixelsearch_result is saved */
uint8_t pixelsearch_result_num = 0;

/** specify the skipped pixel when doing the search **/
uint8_t pixelsearch_skip = 5;


/**
 * pixel search color for threading
 * @see pixelsearch_param
 * @see pixelsearch_result
 * @see pixelsearch_result_num
 * @param param is a pointer to a set of 5 datas, comprises:
 * <ul>
 * <li> first index of param is the thread_id</li>
 * <li> 4 uint32_t* starts from index 1 to 4 is x1,y1,x2,y2 which  
 * 		represent the rectangle area to search. </li>
 * <li> index 5 is the function pointer to the test of the color. 
 * 		return value type is uint8_t will be called like 
 * 		param[5](color_value) and shall return 1 for true, 0 for false</li>
 * <li> index 6 will be the array/pointer where the value will be saved
 * 		it must be array of uint32_t which will save the position of saved</li>
 * 	this param will be freed upon the end of the process of this function
 */ 
void pixelsearch(void *param)
{
	uint32_t *data = (uint32_t *)param;
	uint8_t (*test_method)(long color);
	test_method = data[6];
	uint32_t x,y;
	long color;
	
	printf("node seach thread #%d started\n", data[0]);
	
	for (y=data[2]; y<data[4]; y+= pixelsearch_skip){
	for (x=data[1]; x<data[3]; x+= pixelsearch_skip)
	{
		color = AU3_PixelGetColor((long)x, (long)y);
		if (test_method(color))
		{
			while(pixelsearch_result_lock==1);
			pixelsearch_result_lock = 1;
			if (pixelsearch_result_num>29)
			{
				printf("#%d maximum result has reached\n", data[0]);
				pixelsearch_result_lock = 0;
				return;
			}
			
			//simple data association
			int i;
			for (i=0;i<pixelsearch_result_num; i++)
			{
				if (abs((pixelsearch_result[i]>>16)-x) < NODE_RANGE_MIN)
				if (abs((pixelsearch_result[i]&0x0000FFFF)-y) < NODE_RANGE_MIN)
				{
					printf("#%d found node but too close to node %d in(%d,%d)\n", data[0], i, x,y);
					pixelsearch_result_lock = 0;
					return;
				}
			}
			
			pixelsearch_result[pixelsearch_result_num] = 
				(uint32_t)((x<<16) | (uint16_t)y);
			printf("#%d reporting found in (%d,%d) \n", data[0], x,y);
			pixelsearch_result_num+=1;
			pixelsearch_result_lock = 0;
		}
	}
	printf("#%d reached %d \n", data[0], y);}
	//~ free(data[6]);
	free(data);
	printf("#%d **** this ****! i'm out\n", data[0]);
}

