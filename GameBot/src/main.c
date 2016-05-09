#include <Windows.h>
#include <process.h>
#include "../lib/AutoIt3.h"
#include "quest.h"
//~ #include <winuser.h>

void threadtest(void*);
void threadtest2(void*);

uint8_t test_color(long color);

int APIENTRY WinMain(HINSTANCE hInstance,
                     HINSTANCE hPrevInstance,
                     LPSTR     lpCmdLine,
                     int       nCmdShow)
{
	
	AU3_Init();
	AU3_Sleep(1000);
	Quest_new(Quest);
	//~ Quest->next_node(Quest);
	
	
	makin_pixelsearch_param(myparam, 500,200, 650,300, test_color);
	
	_beginthread( makin_pixelsearch, 0, myparam );
	//_beginthread( threadtest2, 0, NULL );
	while(1){}
	
	return 0;
}

uint8_t test_color(long color)
{
	if (
		   (color>0x002200)
		&& ((color&0xff0000)==0)
		&& ((color&0x0000ff)==0)
	)
		return 1;
	return 0;
}

void threadtest(void *param)
{
	uint32_t *pos = (uint32_t *)param;
	uint8_t (*method)(long color);
	while(1){
		AU3_Sleep(2000);
		AU3_MouseMove(pos[0],pos[1],10);
		AU3_Sleep(1000);
		AU3_MouseMove(pos[2],pos[3],10);
		AU3_Sleep(1000);
		method = pos[4];
		if (method(0x00ffa0)){
			AU3_MouseMove(1200, 200, 30);
			AU3_Sleep(3000);
		}
	}
}
void threadtest2(void *param)
{
	while(1){
		AU3_Sleep(4000);
		AU3_MouseMove(0,200,10);
	}
}

//~ int main(int argc, char *argv[])
//~ {
	//~ AU3_Init();
	//~ AU3_Sleep(1000);
	//~ Quest_new(Quest);
	//~ Quest->next_node(Quest);
	//~ 
//~ }
