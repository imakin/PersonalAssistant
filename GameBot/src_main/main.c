#include <Windows.h>
#include <process.h>
#include "../lib/AutoIt3.h"
#include "quest.h"

int APIENTRY WinMain(HINSTANCE hInstance,
                     HINSTANCE hPrevInstance,
                     LPSTR     lpCmdLine,
                     int       nCmdShow)
{
	
	//~ FARPROC pGetPixel;
//~ 
	//~ HINSTANCE _hGDI = LoadLibrary("gdi32.dll");
	//~ if(_hGDI)
	//~ {
		//~ pGetPixel = GetProcAddress(_hGDI, "GetPixel");
		//~ HDC _hdc = GetDC(NULL);
		//~ if(_hdc)
		//~ {
			//~ int i;
			//~ int _red;
			//~ int _green;
			//~ int _blue;
			//~ COLORREF _color;
			//~ 
				//~ _color = (*pGetPixel) (_hdc, 20 ,20);
//~ 
				//~ _red = GetRValue(_color);
				//~ _green = GetGValue(_color);
				//~ _blue = GetBValue(_color);
//~ 
			//~ ReleaseDC(NULL, _hdc);    
			//~ printlog("col %d, Red: %d, Green: %d, Blue: %d", _color, _red, _green, _blue);
		//~ }
		//~ FreeLibrary(_hGDI);
	//~ }
	
	AU3_Init();
	AU3_Sleep(1000);
	Quest_new(Quest);
	Quest->next_node(Quest);
	//~ get_pixel_color(
	
	//_beginthread( threadtest2, 0, NULL );
	while(1){}
	
	return 0;
}
