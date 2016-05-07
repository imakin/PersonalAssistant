;Shift+alt
HotKeySet("+!a", "startArena")
HotKeySet("+!s", "idle")
HotKeySet("+!d", "fight")
HotKeySet("+!f", "findMatch")
HotKeySet("+!g", "nextNode")

;This indicates which arena tier shall be played, possible is 2, or 3
$arena_tier = 2
Do
   Sleep(1)
Until False


Func idle()
    Do
	  Sleep(1)
   Until False
EndFunc   ;==>Terminate
 
 
;Starts the arena (Fight menu), and continue (tier *2)
Func startArena()
   Do
	  Sleep(500)
	  if ($arena_tier==2) Then
		 Send("9")
	  Else
		 MouseClick("left", 830, 510)
	  EndIf
	  Sleep(3000)
	  Local $current_arena_tier  = $arena_tier
	  askForHelp()
	  if ($current_arena_tier==$arena_tier) Then
		 ; We have energy, continue;else change arena tier in next loop
		 addToTeam()
		 findMatch()
		 fightArena()
	  EndIf
	  
   Until False
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
   Local $redtag = PixelGetColor(603,187)
   Local $red = BitShift($redtag, 16)
   Local $green = BitShift(BitAND($redtag, 0x00FF00), 8)
   Local $blue = BitAND($redtag, 0x0000FF)
   if ($red > $green) Then
	  if ($red > $blue) Then
		 MsgBox(0, "Out of energy", "we're out of energy", 3)
		 Sleep(4000)
		 MouseClick("left", 57, 55)
		 if ($arena_tier==2) Then
			$arena_tier = 3
		 Else
			$arena_tier = 2
		 EndIf
		 Sleep(10000)
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
EndFunc

;Fight in arena
Func fightArena()
   $seq = 0
   $stop = 0
   Do
	  Send("0")
	  Sleep(50);
	  if (Mod($seq, 4)==0) Then
		 Send("K")
	  EndIf
	  $seq = $seq + 1
	  if ($seq>20) then
		 Send("{SPACE}")
		 $seq = 0
	  EndIf
	  
	  ;indicates fight has ended (loading screen)
	  $loading = PixelGetColor(640, 540);
	  if ($loading==0x025c00) Then
		 $loading = PixelGetColor(620, 300)
		 if ($loading==0x161a1b) Then
			$stop = 1
			Sleep(3000)
			MouseClick("left", 57, 55); back because we might ended up in 3* 4* tier arena
			Sleep(10000)
		 EndIf
	  EndIf
	  ; or the case if we ended up in view rewards
	  $loading = PixelGetColor(480,270)
	  if ($loading==0x2b2c30) Then
		 $loading = PixelGetColor(480,330)
		 if ($loading==0x2b2c30) Then
			$stop = 1
			Sleep(1000)
			MouseClick("left", 57, 55); back because we ended up in 3* 4* tier arena
			Sleep(10000)
		 EndIf
	  EndIf
   Until ($stop==1)
EndFunc


;FIGHT In quest
Func fight()
   $seq = 0
   $stop = 0
   Do
	  Send("0")
	  Sleep(30);
	  $seq = $seq + 1
	  if (Mod($seq, 4)==0) Then
		 Send("K")
	  EndIf
	  if ($seq>20) then
		 Send("{SPACE}")
		 $seq = 0
	  EndIf
	  
	  if (Mod($seq,2)==0) Then
		 ;indicates fight has ended (loading screen)
		 $loading = PixelGetColor(958, 577);
		 if ($loading==0x1d2630) Then
			$loading = PixelGetColor(923, 491)
			if ($loading==0xc1c1c2) Then
			   $stop = 1
			   Sleep(3000)
			   Send("J")
			EndIf
		 EndIf
	  EndIf
   Until ($stop==1)
EndFunc


Func nextNode()
   Do
	  Do
		 Send("J")
		 Sleep(200)
		 $greendot = PixelSearch(140,150, 800, 520, 0x00f800)
	  Until not(@error)
	  Sleep(1000)
	  MouseClick("left", $greendot[0], $greendot[1])
	  Sleep(10000)
	  fight()
   Until False
EndFunc