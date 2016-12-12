#include <stdio.h>
#include <Windows.h>
#include "../lib/AutoIt3.h"


void cout_colour(int x, int y)
{
    HWND hWnd = GetDesktopWindow();
    HDC hdc = GetDC(NULL);

    RECT rect;
    GetWindowRect(hWnd, &rect);

    int MAX_WIDTH = rect.right - rect.left;
    int MAX_HEIGHT = rect.bottom - rect.top;

    printf(" Max %d, %d\n", MAX_WIDTH, MAX_HEIGHT);
    

    HDC hdcTemp = CreateCompatibleDC(hdc);

    BITMAPINFO bitmap;
    bitmap.bmiHeader.biSize = sizeof(bitmap.bmiHeader);
    bitmap.bmiHeader.biWidth = MAX_WIDTH;
    bitmap.bmiHeader.biHeight = -MAX_HEIGHT;
    bitmap.bmiHeader.biPlanes = 1;
    bitmap.bmiHeader.biBitCount = 32;
    bitmap.bmiHeader.biCompression = BI_RGB;
    bitmap.bmiHeader.biSizeImage = 0;
    bitmap.bmiHeader.biClrUsed = 0;
    bitmap.bmiHeader.biClrImportant = 0;

    LPRGBQUAD bitPointer;
    HBITMAP hBitmap2 = CreateDIBSection(hdcTemp, &bitmap, DIB_RGB_COLORS, (void**)&bitPointer, 0, 0);

    HBITMAP hbmpOld = (HBITMAP) SelectObject(hdcTemp, hBitmap2);
    BitBlt(hdcTemp, 0, 0, MAX_WIDTH, MAX_HEIGHT, hdc, 0, 0, SRCCOPY);

    LPRGBQUAD hex_color = &bitPointer[(MAX_WIDTH*y)+x];
    int red = hex_color->rgbRed;
    int green = hex_color->rgbGreen;
    int blue = hex_color->rgbBlue;

    printf("r%d g%d b%d\n", red, green, blue);
    wchar_t t[100];
	wsprintfW(t, L"%d, %d, %d\0", red, green, blue);
	AU3_ToolTip((LPCWSTR)t, 100,100);

    SelectObject(hdcTemp, hbmpOld);
    DeleteObject(hBitmap2);
    DeleteDC(hdcTemp);

    ReleaseDC(hWnd, hdc);
}

void get_pixel(int x, int y)
{
    HWND hWnd = GetDesktopWindow();
    HDC hdc = GetDC(NULL);

    COLORREF hex_color = GetPixel(hdc, x, y);
    int red = GetRValue(hex_color);
    int green = GetGValue(hex_color);
    int blue = GetBValue(hex_color);

	printf("slow r%d g%d b%d\n", red, green, blue);
    
    ReleaseDC(hWnd, hdc);
}

int main()
{
	AllocConsole();
	printf("hai\n");
    cout_colour(1, 1);
    get_pixel(1, 1);
    while(1);
    return 0;
}
