#include <Windows.h>
#include <process.h>
#include "../lib/AutoIt3.h"
#include "quest.h"


uint8_t test_color(long color);

int APIENTRY WinMain(HINSTANCE hInstance,
                     HINSTANCE hPrevInstance,
                     LPSTR     lpCmdLine,
                     int       nCmdShow)
{
	
	AU3_Init();
	AU3_Sleep(1000);
	Quest_new(Quest);
	Quest->next_node(Quest);
	
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

