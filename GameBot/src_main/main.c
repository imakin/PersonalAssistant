#include <Windows.h>
#include <process.h>
#include "../lib/AutoIt3.h"
#include "quest.h"

int APIENTRY WinMain(HINSTANCE hInstance,
                     HINSTANCE hPrevInstance,
                     LPSTR     lpCmdLine,
                     int       nCmdShow)
//~ int main(int argc, char *argv[])
{
	#if DEBUG==1
	AllocConsole();
	freopen("CONOUT$", "w", stdout);
	#endif
	printf("Izzulmakin");
	printlog("\n");
	AU3_MouseClick((lpcwstr)"LEFT", (long)(1), (long)(1), 10, 1);
	AU3_MouseClick((lpcwstr)"LEFT", (long)(1), (long)(10), 10, 1);
	AU3_Sleep(5000);
	Quest_new(Quest);
	Quest->next_node(Quest);
	AU3_Sleep(10000);
	
	return 0;
}


