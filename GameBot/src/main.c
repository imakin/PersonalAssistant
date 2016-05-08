#include <Windows.h>
#include "../lib/AutoIt3.h"
#include "quest.h"
//~ #include <winuser.h>


int APIENTRY WinMain(HINSTANCE hInstance,
                     HINSTANCE hPrevInstance,
                     LPSTR     lpCmdLine,
                     int       nCmdShow)
{
	
	AU3_Init();
	AU3_Sleep(1000);
	Quest_new(Quest);
	Quest->next_node(Quest);
	return 0;
}

//~ int main(int argc, char *argv[])
//~ {
	//~ AU3_Init();
	//~ AU3_Sleep(1000);
	//~ Quest_new(Quest);
	//~ Quest->next_node(Quest);
	//~ 
//~ }
