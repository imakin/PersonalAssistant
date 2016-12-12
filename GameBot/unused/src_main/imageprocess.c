#include "imageprocess.h"

/** allstop flag, if 1 then must go idle */
uint8_t all_stop = 0;

/** pixelsearch found node minimum range to be recognized as new node
 * in data association */
uint8_t pixelsearch_node_range_min = 50;

/** where the result saved, in each item array value will be saved 
 * ((x<<16) | y) in which x and y is less than 0xFFFF
 */
uint32_t *pixelsearch_result=NULL;

/** flag valued 1 if a thread is currently updating pixelsearch_result */
uint8_t pixelsearch_result_lock = 0;

/** how much has found pixelsearch_result data saved */
uint8_t pixelsearch_result_num = 0;

/** specify the skipped pixel when doing the search **/
uint8_t pixelsearch_skip = 5;

/** store the number of currently worked job */
uint8_t pixelsearch_jobs = 0;

/** param used in nothread pixelsearch */
uint32_t *pixelsearch_nothread_param;

/* image processing with windows gdi32 */
/** this variable specify the state of hdc: 
 * <ul>
 * 	<li> not ready: value 0 </li>
 * 	<li> currently initiated: value 1 </li>
 * 	<li> ready to use: value 2 </li>
 * </ul>
 */
uint8_t pixelsearch_hdc_ready; 

FARPROC pGetPixel = 0;
HINSTANCE hGDI = 0;

COLORREF 	img_color_dword;
HDC 		img_hdc_optimized;
HDC			img_hdc;
LPRGBQUAD 	img_bitpointer;
BITMAPINFO 	img_bitmap;
HBITMAP 	img_hbitmap2;
HBITMAP 	img_hbmpold;


/**
 * for any pixelsearch-pixel-point long format, get x
 */
long pixelsearch_get_x(long pixel)
{
	return pixel>>16;
}
/**
 * for any pixelsearch-pixel-point long format, get y
 */
long pixelsearch_get_y(long pixel)
{
	return pixel&0x0000ffff;
}



/**
 * refresh the image captured to be used by pixelsearch
 */
void pixelsearch_refresh_image()
{
	SelectObject(img_hdc_optimized, img_hbmpold);
	DeleteObject(img_hbitmap2);
	DeleteDC(img_hdc_optimized);
	ReleaseDC(NULL, img_hdc_optimized);
	ReleaseDC(NULL, img_hdc);
	
	
	img_hdc = GetDC(NULL);
	img_hdc_optimized = CreateCompatibleDC(img_hdc);
	
	img_bitmap.bmiHeader.biSize = sizeof(img_bitmap.bmiHeader);
	img_bitmap.bmiHeader.biWidth = 1366;
	img_bitmap.bmiHeader.biHeight = -768;
	img_bitmap.bmiHeader.biPlanes = 1;
	img_bitmap.bmiHeader.biBitCount = 32;
    img_bitmap.bmiHeader.biCompression = BI_RGB;
    img_bitmap.bmiHeader.biSizeImage = 0;//MAX_WIDTH * 4 * MAX_HEIGHT;
    img_bitmap.bmiHeader.biClrUsed = 0;
    img_bitmap.bmiHeader.biClrImportant = 0;
	img_hbitmap2 = CreateDIBSection(
							img_hdc_optimized, &img_bitmap, DIB_RGB_COLORS,
							(void**)(&img_bitpointer), NULL, NULL);
	img_hbmpold = (HBITMAP) SelectObject(img_hdc_optimized, img_hbitmap2);
	BitBlt(img_hdc_optimized, 0,0, 1366, 768, img_hdc, 0,0, SRCCOPY);
}

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
	pixelsearch_jobs = pixelsearch_jobs + 1;
	uint32_t *data = (uint32_t *)param;
	uint8_t (*test_method)(long color, long x, long y);
	test_method = data[6];
	uint32_t x,y;
	long color;
	
	#define MAX_WIDTH data[3]
	#define MAX_HEIGHT data[4]
	
	int i;
	for (y=data[2]; y<data[4]; y+= pixelsearch_skip){
	for (x=data[1]; x<data[3]; x+= pixelsearch_skip)
	{
		LPRGBQUAD hex_color = &img_bitpointer[(1366*y)+x];
		color = (long)(
				((hex_color->rgbBlue)<<16) |
				((hex_color->rgbGreen)<<8) |
				(hex_color->rgbRed)
			);
		
		if (test_method((long)color, (long)x, (long)y))
		{
			printlog("found color is RGB: %x, %x, %x\n", hex_color->rgbRed, hex_color->rgbGreen, hex_color->rgbBlue);
			while(pixelsearch_result_lock==1);
			pixelsearch_result_lock = 1;
			if (pixelsearch_result_num>29)
			{
				printlog("#%d maximum result has reached\n", data[0]);
				
				pixelsearch_result_lock = 0;
				free(data);
				pixelsearch_jobs = pixelsearch_jobs - 1;
				if (pixelsearch_jobs<1)
					pixelsearch_jobs = 0;
				return;
			}
			
			//simple data association
			int i;
			uint8_t skip=0;
			for (i=0;i<pixelsearch_result_num; i++)
			{
				if (abs((pixelsearch_result[i]>>16)-x) < pixelsearch_node_range_min)
				if (abs((pixelsearch_result[i]&0x0000FFFF)-y) < pixelsearch_node_range_min)
				{
					printlog("#%d found node but too close to node %d in(%d,%d)\n", data[0], i, x,y);
					pixelsearch_result_lock = 0;
					skip = 1;
				}
			}
			
			if(skip!=1)
			{
				pixelsearch_result[pixelsearch_result_num] = 
					(uint32_t)((x<<16) | (uint16_t)y);
				printlog("#%d reporting found in (%d,%d) \n", data[0], x,y);
				pixelsearch_result_num+=1;
				if ((data[7]&PIXELSEARCH_FLAG_EXITONFOUND)==PIXELSEARCH_FLAG_EXITONFOUND)
				{
					printlog("exit on first found\n");
					pixelsearch_result_lock = 0;
					free(data);
					pixelsearch_jobs = pixelsearch_jobs - 1;
					if (pixelsearch_jobs<1)
						pixelsearch_jobs = 0;
					return;
				}
			}
			pixelsearch_result_lock = 0;
		}
	}
	}
	printlog("#%d i'm out\n", data[0]);
	printlog("total found %d \n", pixelsearch_result_num);
	
	free(data);
	pixelsearch_jobs = pixelsearch_jobs - 1;
	if (pixelsearch_jobs<1)
		pixelsearch_jobs = 0;
}




/**
 * get hue from r,g,b,
 * h will be valued in 0-255, 
 * @param r red value
 * @param g green value
 * @param b blue value
 *
long color_hue(int r, int g, int b)
{
	int cmax;
	int cmin;
	int cdif;
	int h;
	
	if (r>g && r>b) cmax = r;
	if (g>r && g>b) cmax = g;
	if (b>r && b>g) cmax = b;
	
	if (r<g && r<b) cmin = r;
	if (g<r && g<b) cmin = g;
	if (b<r && b<g) cmin = b;
	
	cdif = cmax - cmin;
	
	if (cdif==0) 
		h = 0;
	else if (cmax==r)
		h = (int)(60 * (((float)((g-b)/cdif))%6));
	else if (cmax==g)
		h = (int)(60 * (((float)((b-r)/cdif))+2));
	else
		h = (int)(60 * (((float)((r-g)/cdif))+4));

	return h;
}
*/
