#include <Windows.h>
#include <process.h>
#include "../lib/AutoIt3.h"
#include "quest.h"


uint8_t aaaaaa(long color, long x, long y)
{
	if (color==0xFFFFFF)
		return 1;
	//~ wchar_t t[100];
	//~ wsprintfW(t, L"%d now in %d,%d\0", color, x,y);
	//~ AU3_Sleep(2000);
	//~ AU3_ToolTip((LPCWSTR)t, 100,100);
	//~ AU3_Send((lpcwstr)"H",0);
	//~ AU3_Send((lpcwstr)t,0);
	
	//~ if (color==
		//~ AU3_MouseMove(x, y, 10);
	return 0;
}

int APIENTRY WinMain(HINSTANCE hInstance,
                     HINSTANCE hPrevInstance,
                     LPSTR     lpCmdLine,
                     int       nCmdShow)
//~ int main(int argc, char *argv[])
{
	AllocConsole();
	freopen("CONOUT$", "w", stdout);
	printf("HAI");
	//~ freopen("CONIN$", "r", stdin);
	//~ AU3_MouseMove(100,100, 10);
	//~ AU3_Sleep(3000);
	//~ 
	//~ pixelsearch_nothread(my, 0,0,110,110, &aaaaaa, PIXELSEARCH_FLAG_EXITONFOUND);
	//~ while(1);
	//~ return 0;
	
	//~ printf("hahaha\n");
	//~ AU3_Init();
	
	AU3_Sleep(5000);
	Quest_new(Quest);
	Quest->next_node(Quest);
	AU3_Sleep(10000);
	//~ while(1){}
	
	return 0;
}
