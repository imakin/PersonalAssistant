;Shift+alt
HotKeySet("+!a", "startArena")
HotKeySet("+!z", "changeArenaTier")
HotKeySet("+!s", "idle")
HotKeySet("+!d", "fight")
HotKeySet("+!f", "findMatch")
HotKeySet("+!g", "nextNode")
HotKeySet("+!p", "playthegame")
HotKeySet("+!c", "calibrateWindow")


;This indicates which arena tier shall be played, possible is 2, or 3
$arena_tier = 2
$arena_continue = 1
$allstop = 0
Do
   Sleep(1)
Until False


Func idle()
   $allstop = 1
   MsgBox(0, "now", "terminated", 1)
   Do
	  Sleep(1)
   Until False
EndFunc   ;==>Terminate
 
 
Func playthegame()
   MouseClick("left", 26, 750) ;window start menu
   MouseClick("left", 70, 400) ;bluestack app
   Sleep(90000)
   MsgBox(0, "now", "i will now move the bluestack window", 5)
   MouseClickDrag("left", 90, 30, 75, 15)
   Sleep(2000)
   MouseClick("left", 913, 307) ;click the game 
   Sleep(60000)
   playthearena()
EndFunc
Func playthearena()
   MouseClick("left", 162, 51)
   Sleep(1000)
   MouseClick("left", 271, 135) ;fight button
   Sleep(20000)
   MouseClick("left", 535, 313) ;versus
   Sleep(20000)
   startArena()
EndFunc

Func changeArenaTier()
   if ($arena_tier==2) Then
	  $arena_tier = 3
	  MsgBox(0, "arena tier", "arena tier is now 3", 2)
   Else
	  $arena_tier = 2
	  MsgBox(0, "arena tier", "arena tier is now 2", 2)
   EndIf
EndFunc

;Starts the arena (Fight menu), and continue (tier *2)
Func startArena()
   $allstop = 0
   Do
	  Sleep(500)
	  MouseClickDrag("left", 130, 255, 700, 255);drag left mosst for foolproof
	  Sleep(1000)
	  if ($arena_tier==2) Then
		 ;Send("9")
		 MouseClick("left", 386, 446)
		 Sleep(5000)
		 MouseClick("left", 413, 522);double check
		 MouseClick("left", 433, 522);double check
	  Else
		 MouseClick("left", 830, 510)
		 Sleep(5000)
		 MouseClick("left", 760, 508);double check
	  EndIf
	  Sleep(5000)
	  Local $current_arena_tier  = $arena_tier
	  $arena_continue = 1
	  askForHelp()
	  if ($arena_continue==1) Then
		 ; We have energy, continue;else change arena tier in next loop
		 addToTeam()
		 findMatch()
		 fightArena()
	  EndIf
	  
   Until ($allstop==1)
EndFunc

Func askForHelp()
   Local $carryon = 1
   Do
	  ;Detect if we can ask for help
	  Local $helpbutton = PixelGetColor(260, 175)
	  Local $red = BitShift($helpbutton, 16)
	  Local $green = BitShift(BitAND($helpbutton, 0x00FF00), 8)
	  Local $blue = BitAND($helpbutton, 0x0000FF)
	  if ($green > $red) Then
		 if ($green > $blue) Then
			Send("Q")
			Sleep(3000)
		 Else
			$carryon = 0
		 EndIf
	  Else
		 $carryon = 0
	  EndIf
   Until ($carryon==0)
   
   ;Detect if less than 3 champion has energy
   Local $redtag = PixelGetColor(630,188)
   Local $red = BitShift($redtag, 16)
   Local $green = BitShift(BitAND($redtag, 0x00FF00), 8)
   Local $blue = BitAND($redtag, 0x0000FF)
   if (($red-80) > $green) Then
	  if (($red-80) > $blue) Then
		 MsgBox(0, "Out of energy", "we're out of energy", 3)
		 $arena_continue = 0
		 Sleep(4000)
		 MouseClick("left", 57, 55)
		 if ($arena_tier==2) Then
			$arena_tier = 3
		 Else
			$arena_tier = 2
		 EndIf
		 Sleep(7000)
	  EndIf
   EndIf
   
   ;Detect if there are any Reconnect popup
   if (PixelGetColor(490,320)==0x2b2c30) Then
	  if (getDominantColor(PixelGetColor(490,350))=="green") Then
		 MsgBox(0, "popup", "I'll press the popup button in 5", 5)
		 Sleep(6000)
		 MouseClick("left", 490, 350)
		 Sleep(7000)
	  EndIf
   EndIf
   
   ;detect if we're in useless milestone info
   if (getDominantColor(PixelGetColor(934,555))=="green") Then
	  if ((PixelGetColor(492,337)==0x2b2c30)) Then
		 MsgBox(0, "milestone", "I assume we're in milestone info", 3)
		 Sleep(1000)
		 $arena_continue = 0
		 MouseClick("left", 57, 55)
		 Sleep(7000)
	  EndIf
   EndIf
   
EndFunc

;arena
Func addToTeam()
   MouseClickDrag("left", 319, 235, 145, 135)
   sleep(500)
   MouseClickDrag("left", 319, 235, 145, 210)
   sleep(500)
   MouseClickDrag("left", 319, 235, 145, 290)
   sleep(500)
EndFunc

;Arena
Func findMatch()
   Sleep(500)
   MouseClick("left", 109, 547)
   Sleep(4000)
   MouseClick("left", 687, 445)
   Sleep(3000)
   Send("0")
   Sleep(8000)
EndFunc

;Fight in arena
Func fightArena()
   $seq = 0
   $stop = 0
   $allstop = 0
   Do
	  Send("0")
	  Sleep(10);
	  if (Mod($seq, 4)==0) Then
		 Send("K")
	  EndIf
	  $seq = $seq + 1
	  if ($seq>15) then
		 Send("{SPACE}")
		 if ($seq>20) Then
			$seq = 0
		 EndIf
	  EndIf
	  if (getDominantColor(PixelGetColor(144,541))=="red") then
		 Send("{SPACE}")
	  EndIf
	  
	  ;indicates fight has ended (loading screen)
	  $loading = PixelGetColor(640, 540);
	  if ($loading==0x025c00) Then
		 $loading = PixelGetColor(620, 300)
		 if ($loading==0x161a1b) Then
			$stop = 1
			MsgBox(0, "popup", "shall i press back button?", 2)
			Sleep(2000)
			MouseClick("left", 57, 55); back because we might ended up in 3* 4* tier arena
			Sleep(10000)
		 EndIf
	  EndIf
	  
	  ;or chat bar has been clicked
	  if ($loading==0x161a1d) Then
		 if (PixelGetColor(136,540)==0x292c30) Then
			$stop = 1
			MsgBox(0,"chat", "this is chat window", 2)
			Sleep(1000)
			MouseClick("left", 943, 52); close
			Sleep(2000)
		 EndIf
	  EndIf
	  
	  ; or the case if we ended up in view rewards
	  $loading = PixelGetColor(480,270)
	  if ($loading==0x2b2c30) Then
		 $loading = PixelGetColor(480,330)
		 if ($loading==0x2b2c30) Then
			$stop = 1
			Sleep(3000)
			MouseClick("left", 57, 55); back because we ended up in 3* 4* tier arena
			Sleep(10000)
		 EndIf
	  ElseIf ($loading==0x000000) Then
		 ; stuck in alliance quest window; todo alliance quest window with empty quest
		 if (PixelGetColor(838,366)==0x2b2c30) Then
			$stop = 1
			MsgBox(0,"alliance q", "alliance quest cuy", 2);
			$arena_tier = 2
			Sleep(2000)
			MouseClick("left", 57, 55); 
			Sleep(10000)
		 EndIf
	  EndIf
	  
	  ;stuck in alliance quest window
	  $loading = PixelGetColor(384,142)
	  if ($loading==0x1a1a1a) Then
		 if (PixelGetColor(551,142)==0x1a1a1a) Then
			if (Not(PixelGetColor(504,142)==0x1a1a1a)) Then
			   $stop = 1
			   MsgBox(0,"alliance q", "empty alliance quest cuy", 2);
			   $arena_tier = 2
			   Sleep(2000)
			   MouseClick("left", 57, 55); 
			   Sleep(10000)
			EndIf
		 EndIf
	  EndIf
	  
	  ; or the case we stuck in team adding
	  if (PixelGetColor(18, 130)==0x2b2c30) Then ; the left bar team list
		 if (PixelGetColor(936,511)==0x2b2c30) Then ;the champion filter button
			$stop = 1
			Sleep(1000)
			MouseClick("left", 57, 55); back
			Sleep(10000)
		 EndIf
	  EndIf
   Until ($stop==1 or $allstop==1)
EndFunc


;FIGHT In quest
Func fight()
   $seq = 0
   $stop = 0
   $allstop = 0
   Do
	  Send("0")
	  Sleep(30);
	  $seq = $seq + 1
	  if (Mod($seq, 4)==0) Then
		 Send("K")
	  EndIf
	  if ($seq>12) then
		 Send("{SPACE}")
		 if ($seq>20) Then
			$seq = 0
		 EndIf
	  EndIf
	  
	  if (Mod($seq,2)==0) Then
		 $loading = PixelGetColor(958, 577);
		 if ($loading==0x1d2630) Then 
		 ;indicates fight has ended
			$loading = PixelGetColor(923, 491)
			if ($loading==0xc1c1c2) Then
			   $stop = 1
			   Sleep(3000)
			   Send("J")
			EndIf
		 ElseIf ($loading==0x07090c) Then
			if (PixelGetColor(825,105)==0x2b2c30) Then
			   $stop = 1
			   Sleep(3000)
			   Send("J")
			EndIf
		 ;Elseif (PixelGetColor(486,310)==0xeeeeee) Then
			;we're in loading  screen
			;$stop = 1
			;Sleep(3000)
			;Send("J")
		 EndIf
	  EndIf
   Until ($stop==1 or $allstop==1)
EndFunc


Func nextNode()
   $allstop = 0
   Do
	  Local $step = 0
	  Do
		 $step = $step + 1
		 if ($step == 10) Then
			MouseClickDrag("left", 450, 320, 642, 346)
		 ElseIf ($step == 20) Then
			MouseClickDrag("left", 450, 320, 200, 200)
			MouseClickDrag("left", 450, 320, 300, 300)
		 ElseIf ($step == 30) Then
			MouseClickDrag("left", 700, 100, 100, 400)
		 ElseIf ($step == 40) Then
			MouseClickDrag("left", 100, 400, 700, 100)
			MouseClickDrag("left", 100, 400, 700, 100)
			$step = 0
		 EndIf
		 Send("J")
		 Sleep(200)
		 $greendot = PixelSearch(80,100, 957, 530, 0x00f800)
		 if (@error) Then
			$greendot = PixelSearch(80,100, 957, 530, 0x00e400)
		 EndIf
	  Until not(@error)
	  Send("J")
	  MouseMove($greendot[0], $greendot[1])
	  MsgBox(0, "now", "i will click this in 4s", 1)
	  Sleep(4000)
	  MouseClick("left", $greendot[0], $greendot[1])
	  Sleep(10000)
	  fight()
	  Sleep(4000)
	  Send("J")
   Until ($allstop==1)
EndFunc

Func getDominantColor($color)
   Local $red = BitShift($color, 16)
   Local $green = BitShift(BitAND($color, 0x00FF00), 8)
   Local $blue = BitAND($color, 0x0000FF)
   if ($red > $green And $red > $blue) Then
	  Return ("red")
   ElseIf ($green > $blue And $green > $red) Then
	  Return ("green")
   ElseIf ($blue > $red And $blue > $green) Then
	  Return ("blue")
   Else
	  if ($red > $green or $red > $blue) Then
		 Return ("red")
	  ElseIf ($green > $blue or $green > $red)  Then
		 Return ("green")
	  Else
		 Return ("blue")
	  EndIf
   EndIf
EndFunc

;Calibrate the bluestack window position
;@param $width the width of the screen to search
;@param $height the height of the screen to search
Func calibrateWindow($width=1366,$height=768)
   ;searching bluestack logo
   Local $repeat = 1
   Do
	  $icon = PixelSearch(0,0,1366,768, 0x79af1b);
	  if (@error) Then
		 MsgBox(0,"failed", "can't find bluestack window", 3)
	  Else
		 $find  = PixelSearch($icon[0]-8, $icon[1], $icon[0]+8, $icon[1]+10, 0xf6d502)
		 if (not(@error)) Then
			$find = PixelSearch($icon[0]-8,$icon[1], $icon[0]+8, $icon[1]+10, 0xdd3a17)
			if (not(@error)) Then
			   MouseClickDrag("left", $icon[0]+14, $icon[1], 30, 12)
			   $repeat = 0
			EndIf
		 EndIf
		 ;next color
	  EndIf
	  
   Until ($repeat==0)
EndFunc