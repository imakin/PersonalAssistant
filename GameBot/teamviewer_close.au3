Do
   Do
	  $logo = PixelSearch(430,307, 502,381, 0x00b6fa)
	  Sleep(2000)
   Until Not(@error)
   if (PixelGetColor(843,372)==0xffffff) Then
	  if (PixelGetColor(531,427)==0xf5f7f8) Then
		 MsgBox(0, "teamviewer", "teamviewer dialog appears", 3)
		 Sleep(2000)
		 MouseClick("left", 864,430)
		 Sleep(4000)
		 MouseClick("left", 336,19)
	  EndIf
   EndIf
   Sleep(2000)
Until False