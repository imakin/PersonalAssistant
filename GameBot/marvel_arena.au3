;Shift+alt
HotKeySet("+!a", "startArena")
HotKeySet("+!z", "changeArenaTier")
HotKeySet("+!s", "idle")
HotKeySet("+!d", "fight")
HotKeySet("+!f", "findMatch")
HotKeySet("+!g", "nextNode")
HotKeySet("+!h", "fightArena")
HotKeySet("+!j", "fightArenaMaintenanceWait")
HotKeySet("+!q", "Duel")
HotKeySet("+!p", "playthegame")
HotKeySet("+!c", "calibrateWindow")
HotKeySet("+!i", "showStatus")
HotKeySet("+!u", "updateCaptureLoading")
HotKeySet("+!e", "changeUpcomingToggle")
$duel_target = "robin agent"
$duel_target_pos = 1 ;in search position in 1st, 2nd, or 3rd
Global $status="ngondek"
Global $savepixel = 0
Global $screensave[6]
$screensave[0] = 0
$screensave[1] = 0
$screensave[2] = 0
$screensave[3] = 0
$screensave[4] = 0
$screensave[5] = 0
Global $screenloading[6]
$screenloading[0] = 0
$screenloading[1] = 0
$screenloading[2] = 0
$screenloading[3] = 0
$screenloading[4] = 0
$screenloading[5] = 0
$arena_upcoming = False

$stuckseq = 0
$arenatimersecond = 0
$stack = 0;stack of fight method state


;This indicates which arena tier shall be played, possible is 2, or 3
$arena_tier = 3
$arena_continue = 1
$allstop = 0
;Flag whether to activate quest hunting mode (do quest if there are energy)
$quest_active = False
$match_number = 0
$replay_instead_of_ngarena = True
;Multiplier streak for when to do alliance help
$alliance_help = 30
Do
   Sleep(1)
Until False

Func showStatus()
   ToolTip(StringFormat("%s, stack is: %d. limit timer counter: %d. Stuck counter: %d", $status,$stack, $arenatimersecond, $stuckseq),0,740)
EndFunc


Func idle()
   $status = "idle"
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
   Elseif ($arena_tier==3) Then
	  $arena_tier = 4
	  MsgBox(0, "arena tier", "arena tier is now alltier(when there is no event)", 2)
   ElseIf ($arena_tier==4) Then
	  $arena_tier = 5
	  MsgBox(0, "arena tier", "arena tier is now 5, the special high lvl arena(catalyst, alpha)", 2)
   Else 
	  $arena_tier = 2
	  MsgBox(0, "arena tier", "arena tier is now 2", 2)
   EndIf
EndFunc

Func changeUpcomingToggle()
   if ($arena_upcoming) Then
	  ToolTip("arena upcoming set false",1000,200)
	  $arena_upcoming = False
   Else
	  ToolTip("arena upcoming set true",1000,200)
	  $arena_upcoming = True
   EndIf
EndFunc

;Starts the arena (Fight menu), and continue (tier *2)
Func startArena()
   $status = "start arena"
   $allstop = 0
   $quest_play = False
   Do
	  $stack = $stack + 1
	  $match_number = $match_number + 1
	  calibrateWindow()
	  if ($quest_active AND PixelGetColor(203,43)==0x2b2c30) Then ;quest is active, make sure not in fight and we can click menu
		 if (checkEnergyIsFull()) Then
			;to reduce stack memory we quit but set flag
			MsgBox(0, "quest", "i want to hunt ISOs", 2)
			$quest_play = True
			$allstop = 1
		 EndIf
	  EndIf
	  ToolTip(StringFormat("match number : %d",$match_number),1000,100)
	  if (Mod($match_number, $alliance_help)==0 AND PixelGetColor(203,43)==0x2b2c30) Then
		 MouseClick("left", 190, 58) ;menu
		 Sleep(1000)
		 MouseClick("left", 190, 58) ;menu double
		 Sleep(1000)
		 if (PixelGetColor(400,92)==0x590000) Then
			;send help for the alliance
			MouseClick("left",375,131);alliance
			Sleep(10000)
			MouseClick("left",490,180);help tab
			Sleep(2000)
			Do
			   MouseClick("left",760,235);help button
			   Sleep(2000)
			Until (Not(getDominantColor(PixelGetColor(750,235))=="green"))
			
			MouseClick("left", 190, 58) ;menu
			Sleep(1000)
			MouseClick("left", 190, 58) ;menu double
			Sleep(1000)
			MouseClick("left", 270, 132) ;fight
			Sleep(8000)
		 EndIf
	  ElseIf (Mod($match_number, $alliance_help)==0) Then
		 $match_number = $match_number - 1;SO that we keep trying on the next chance 
	  EndIf
	  
	  $arena_continue = 1
	  if ($allstop==0) Then
		 checkInsideFight()
		 Sleep(500)
		 if ($arena_tier==5) Then
			MouseClickDrag("left", 700, 255, 130, 255);drag right mosst for foolproof
			Sleep(500)
			MouseClickDrag("left", 700, 255, 130, 255);drag right mosst for foolproof
			Sleep(500)
		 Else
			if ($arena_tier==3 AND isInTeamAdding() AND isInTeamAddingTier(3)) Then
			   ToolTip("In Correct Team Adding",1000,200)
			ElseIf (getDominantColor(PixelGetColor(130,532))=="green" AND getDominantColor(PixelGetColor(430,532))=="green" AND getDominantColor(PixelGetColor(868,532))=="green") Then
			   ToolTip("no need to drag left most ",1000,200)
			   checkInsideFight()
			Else
			   MouseClickDrag("left", 130, 255, 700, 255);drag left mosst for foolproof
			   checkInsideFight()
			   Sleep(1500)
			   MouseClickDrag("left", 130, 255, 700, 255);drag left mosst for foolproof
			EndIf
		 EndIf
		 checkInsideFight()
		 Sleep(1000)
		 
		 checkInsideFight()
		 
		 if ($arena_tier==3 AND isInTeamAdding() AND isInTeamAddingTier(3)) Then
			ToolTip("In Correct Team Adding when checking if in fight menu or arena menu",1000,200)
		 ElseIf (Not(getDominantColor(PixelGetColor(346,535))=="green") AND (Not($arena_tier==5))) Then
			MsgBox(0, "fight", "inside fight menu, not arena", 1)
			MouseClickDrag("left", 130, 255, 700, 255);drag left mosst for foolproof
			Sleep(400)
			MouseClick("left", 500,446)
			Sleep(2000)
			Local $wait = 0
			do
			   Sleep(1000)
			   $wait = $wait+1
			   checkInsideFight()
			Until (getDominantColor(PixelGetColor(435,525))=="green" OR ($wait>10))
		 EndIf
		 checkInsideFight()
		 ;check if currently in one of 3 fights
		 if (PixelGetColor(160,222)==0x2b2c30 AND PixelGetColor(816,222)==0x2b2c30) Then
			Local $leftresult=PixelGetColor(294,280) ;lose 721a1a red, win 26552e
			Local $rightresult=PixelGetColor(697,280)
			if ($leftresult==0x26552e OR $leftresult==0x721a1a) Then
			   if ($rightresult==0x26552e OR $rightresult==0x721a1a) Then
				  MsgBox(0, "fight", "more fight to go", 1)
				  Sleep(1000)
				  MouseClick("left", 200,200)
				  fightArena()
				  $arena_continue = 0
			   EndIf
			EndIf
		 EndIf
		 checkInsideFight()
		 if ($arena_continue==1) Then
			if ($arena_tier==2) Then
			   ;Send("9")
			   MouseClick("left", 386, 446)
			   Sleep(5000)
			   MouseClick("left", 413, 522);double check
			Elseif ($arena_tier==3) Then
			   if (isInTeamAdding() AND isInTeamAddingTier(3)) Then
				  ToolTip("In correct team adding tier 3, now to ask for help")
				  MouseClick("left", 760, 508);double check
				  Sleep(1000)
			   Else
				  MouseClick("left", 830, 510)
				  Sleep(5000)
				  MouseClick("left", 760, 508);double check
			   EndIf
			Elseif ($arena_tier==4) Then ;arena tier 4
			   MouseClick("left", 433, 522);
			   Sleep(5000);
			Else
			   
			   if (Not(getDominantColor(PixelGetColor(595,516))=="green") )Then; AND 
				  if ($arena_upcoming==False Or Not(getDominantColor(PixelGetColor(438,516))=="green")) Then; WHEN THERE ARE UPCOMING EVENT
					 MsgBox(0, "fight", "inside fight menu, not arena (special)", 1)
					 MouseClickDrag("left", 130, 255, 700, 255);drag left mosst for foolproof
					 Sleep(1000)
					 MouseClickDrag("left", 130, 255, 700, 255);drag left mosst for foolproof
					 Sleep(1000)
					 MouseClick("left", 500,446)
					 Local $wait = 0
					 do
						Sleep(1000)
						$wait = $wait+1
						;checkInsideFight()
					 Until (getDominantColor(PixelGetColor(595,516))=="green" OR ($wait>10))
					 MouseClickDrag("left", 700, 255, 130, 255);drag right mosst for foolproof
					 MouseClickDrag("left", 700, 255, 130, 255);drag right mosst for foolproof
					 Sleep(1000)
				  EndIf
			   EndIf
			   checkInsideFight()
			   if ($arena_upcoming and getDominantColor(PixelGetColor(438,516))=="green") Then ; WHEN THERE ARE UPCOMING EVENT
				  ToolTip("arena upcoming success found button",1000,200)
			      MouseClick("left",438,516)
			   Else
				  MouseClick("left", 674, 508);NORMAL POSITION
			   EndIf
			   Sleep(5000);
			EndIf
		 EndIf
		 
		 checkInsideFight()
		 Sleep(5000)
		 Local $current_arena_tier  = $arena_tier
		 
		 askForHelp()
		 checkInsideFight()
		 if ($arena_continue==1) Then
			; We have energy, continue;else change arena tier in next loop
			addToTeam()
			findMatch()
			fightArena()
		 EndIf
	  EndIf;if ($allstop==0) Then
	  
	  $stack = $stack - 1
   Until ($allstop==1)
   
   if ($quest_play) Then
	  questplay()
   EndIf
EndFunc

Func askForHelp()
   $status = "ask for help"
   Local $carryon = 1
   Do
	  checkInsideFight()
	  ;Detect if we can ask for help
	  Local $helpbutton = PixelGetColor(260, 175)
	  Local $red = BitShift($helpbutton, 16)
	  Local $green = BitShift(BitAND($helpbutton, 0x00FF00), 8)
	  Local $blue = BitAND($helpbutton, 0x0000FF)
	  if ($green > $red) Then
		 if ($green > $blue) Then
			Send("Q")
			checkInsideFight()
			Sleep(3000)
		 Else
			$carryon = 0
		 EndIf
	  Else
		 $carryon = 0
	  EndIf
	  if (checkInsideHome()) Then
		 gotoFightMenu()
		 $arena_continue = 0
		 Return
	  EndIf
   Until ($carryon==0)
   
   ;Detect if less than 3 champion has energy
   Local $redtag = PixelGetColor(630,188)
   Local $red = BitShift($redtag, 16)
   Local $green = BitShift(BitAND($redtag, 0x00FF00), 8)
   Local $blue = BitAND($redtag, 0x0000FF)
   if (($red-80) > $green) Then
	  if (($red-80) > $blue) Then
		 MsgBox(0, "Out of energy", "we're out of energy", 2)
		 $arena_continue = 0
		 checkInsideFight()
		 Sleep(4000)
		 MouseClick("left", 57, 55)
		 if ($arena_tier==2) Then
			$arena_tier = 3
		 Elseif ($arena_tier==3) Then
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
		 MsgBox(0, "milestone", "I assume we're in milestone info", 1)
		 Sleep(1000)
		 $arena_continue = 0
		 MouseClick("left", 57, 55)
		 Sleep(7000)
	  EndIf
   EndIf
   
   
   ;if we're in continue next fight
   if (getDominantColor(PixelGetColor(936,556))=="green") Then
	  if (PixelGetColor(688,436)==0x191e23) Then
		 $arena_continue = 0
		 fightArena()
	  EndIf
   EndIf
EndFunc

;arena
Func addToTeam()
   checkInsideFight()
   $status = "add to team"
   MouseClickDrag("left", 319, 235, 145, 135)
   sleep(500)
   checkInsideFight()
   MouseClickDrag("left", 319, 235, 145, 210)
   sleep(500)
   checkInsideFight()
   MouseClickDrag("left", 319, 235, 145, 290)
   sleep(500)
EndFunc

;For arena avoid class penalty
Func rearrangeTeam()
   ToolTip("rearange", 1000,200)
   ;wait until ready
   Local $wait = 10
   Do
	  ToolTip(StringFormat(" wait %d",$wait),1000,200)
	  Sleep(500)
	  $wait = $wait - 1
   Until ($wait <1 or checkInsideFight())
   Sleep(3000)
   if ($arena_continue==0) Then
	  Return
   EndIf
   Local $clear=False
   Local $c = 0
   Do
	  $clear = True
	  ToolTip(getDominantColor(PixelGetColor(421,262)),1000,200)
	  
	  if (getDominantColor(PixelGetColor(421,262))=="red") Then
		 MouseClickDrag("left", 340,225, 340,308)
		 Sleep(2000)
		 $clear = False
	  EndIf
	  if (getDominantColor(PixelGetColor(421,338))=="red") Then
		 MouseClickDrag("left", 340,308, 340,380)
		 Sleep(2000)
		 $clear = False
	  EndIf
	  if (getDominantColor(PixelGetColor(421,413))=="red") Then
		 MouseClickDrag("left", 340,380, 340,225)
		 Sleep(2000)
		 $clear = False
	  EndIf
	  
	  $c = $c+1
	  if ($c>10) Then
		 $clear = True;give up
	  EndIf
   Until ($clear or checkInsideFight())
EndFunc

;Arena
Func findMatch()
   $status = "find match"
   Sleep(500)
   MouseClick("left", 109, 547)
		 
		 checkInsideFight()
   Sleep(4000)
   
   
   PixelSearch(543,416,575,429, 0x319d32)
   if (@error) Then
	  ;highest is not easy, check if mid easy
	  PixelSearch(543,280,575,294, 0x319d32)
	  if (@error) Then
		 ;mid is not easy
		 ;MsgBox(0,"tier", "mid and high is not easy",1)
		 ToolTip("mid and high is not easy",1000,200)
		 MouseClick("left", 600,200)
	  Else
		 ToolTip("mid is easy",1000,200)
		 ;mid is easy
		 MouseClick("left", 600,320)
	  EndIf
   Else
	  ToolTip("highest is easy",1000,200)
	  ;highest is easy
	  MouseClick("left", 687, 445)
   EndIf
		 
   checkInsideFight()
   Sleep(3000)
   Send("0")
   
   rearrangeTeam()
   
   $c = PixelGetColor(841,574)
   if (GetDominantColor($c)=="green") Then
	  Sleep(3000)
   Else
	  Local $t = 0
	  Local $cont = 1
	  Do
		 Sleep(500)
		 if ($t>120) Then
			;stuck
			$cont = 0
		 EndIf
		 if (Not(PixelGetColor(841,574)==$c)) Then
			$cont = 0
		 EndIf
		 $t = $t+1
	  Until ($cont==0)
   EndIf
EndFunc

Func fightArenaMaintenanceWait()
   
   $wait = 900 ;in seconds
   $delayval = TimerInit()
   Do
	  MouseClickDrag("left",100,400,300,100)
	  $diff = TimerDiff($delayval)
	  if ($diff>20000) Then
		 $wait = $wait - 20
		 $delayval = TimerInit()
	  Else
		 Sleep(500)
	  EndIf
	  $status = StringFormat("Maintenance, Arena will be triggered in %d sec. %d", $wait, $diff)
	  showStatus()
   Until ($wait<1)
   startArena()
EndFunc

;Fight in arena
Func fightArena()
   $status = "fight arena"
   $seq = 0
   $stop = 0
   $allstop = 0
   
   ;stuck in something handler
   Local $somewhereoutsidecounter = 0
   $stuckseq = 0
   $startarena = TimerInit()
   $arenatimersecond = 0
   Do
	  $stuckseq = $stuckseq+1
	  if (Mod($stuckseq,100)==0) Then
		 $stuqseq = 1
		 ToolTip("check stuck", 1000,200)
		 if (checkStuck() and not(isInsideFight ())) Then
			ToolTip("check stuck: stuck detected",1000,200)
			$status = "state fighting. \nstuck detected."
			showStatus()
			updateCapture()
			$stop = 1
			MsgBox(0, "popup", "i guess we're stuck", 2)
			
			;stuck in leaderboard
			if (PixelGetColor(921,138)==0x292c30) Then
			   if (PixelGetColor(939,61)==0x6c6e71) Then
				  MsgBox(0, "popup", "leaderboard, ill close it", 1)
				  Sleep(2000)
				  MouseClick("left", 939,61)
				  Sleep(3000)
			   EndIf
			EndIf
			MouseClick("left", 148, 58) ;menu
			Sleep(2000)
			MouseClick("left", 270, 132) ;fight

			
			Sleep(10000)
		 Else
			ToolTip("check stuck: stuck undetected",1000,200)
			$status = "state fighting.\nstuck undetected."
			showStatus()
		 EndIf
		 updateCapture()
		 
		 ;check if too long playing maybe something is not right
		 $dif = TimerDiff($startarena)
		 if ($dif > 30000) Then
			$startarena = TimerInit()
			$arenatimersecond = $arenatimersecond + ($dif/1000)
		 EndIf
		 if ($arenatimersecond > 300) Then
			ToolTip("Too long in fight",1000,200)
			if (isInsideFight()) Then
			   ToolTip("Guess the fight stuck bug", 1000,200)
			   startOver()
			   $stop = 1
			   $allstop = 1
			Else
			   Sleep(5000)
			   MouseClick("left", 148, 58) ;menu
			   Sleep(2000)
			   MouseClick("left", 190, 58) ;menu double
			   Sleep(2000)
			   MouseClick("left", 270, 132) ;fight
			   Sleep(10000)
			EndIf
		 EndIf
	  EndIf
	  
	  Send("0")
	  Sleep(1);
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
			ToolTip("shall i press back button? (loading screen)", 1000,200)
			Sleep(2000)
			if (PixelGetColor(640, 540)==0x025c00 AND PixelGetColor(620, 300)==0x161a1b) Then
			   MouseClick("left", 57, 55); back because we might ended up in wrong 2* 3* 4* tier arena
			   Sleep(500)
			   MouseClick("left", 57, 55); back because we might ended up in wrong 2* 3* 4* tier arena
			   Sleep(10000)
			EndIf
		 EndIf
	  EndIf
	  
	  ;or chat bar has been clicked
	  if ($loading==0x161a1d) Then
		 if (PixelGetColor(15,540)==0x2a2d31) Then
			$stop = 1
			MsgBox(0,"chat", "this is chat window", 1)
			Sleep(1000)
			MouseClick("left", 943, 52); close
			Sleep(2000)
			MouseClick("left", 148, 58) ;menu
			Sleep(1000)
			MouseClick("left", 190, 58) ;menu double
			Sleep(1000)
			MouseClick("left", 270, 132) ;fight
			Sleep(5000)
		 EndIf
	  EndIf
	  
	  ; or the case if we ended up in view rewards
	  $loading = PixelGetColor(480,270)
	  if ($loading==0x2b2c30) Then
		 $loading = PixelGetColor(480,330)
		 if ($loading==0x2b2c30) Then
			ToolTip("(view rewards) ?(TODO)", 1000,200)
			Sleep(2000)
			Send("J")
			Sleep(2000)
			
			if (PixelGetColor(480,270)==0x2b2c30) Then
			   if (PixelGetColor(480,330)==0x2b2c30) Then
				  $arenatimersecond = 0
				  if ((getDominantColor(PixelGetColor(142,510))=="green") AND (getDominantColor(PixelGetColor(390,510))=="green") AND (getDominantColor(PixelGetColor(800,510))=="green")) Then
					 ToolTip("View rewards now in fight menu arena",1000,200)
				  EndIf
				  if (getDominantColor(PixelGetColor(930,560))=="green") Then
					 $stop = 1
					 MouseClick("left", 57, 55); back
					 Sleep(400)
					 MouseClick("left", 57, 55); back
					 Sleep(5000)
				  Else
					 $status = "view rewards that doesn't end yet"
					 $stop = 1
					 Send("J")
					 MouseClick("left", 57, 55); back
					 Sleep(400)
					 MouseClick("left", 57, 55); back000K0000K000 0K 0 0 0 0K 0K000
				  EndIf
			   EndIf
			EndIf
			
		 EndIf
	  ElseIf ($loading==0x000000) Then
		 ; stuck in alliance quest window; todo alliance quest window with empty quest
		 if (PixelGetColor(838,366)==0x2b2c30) Then
			$stop = 1
			MsgBox(0,"alliance q", "alliance quest cuy", 1);
			;$arena_tier = 2
			Sleep(2000)
			MouseClick("left", 57, 55); 
			Sleep(10000)
		 EndIf
	  EndIf
	  
	  ;check if in event info
	  if (PixelGetColor(50,100)==0x292c30 AND PixelGetColor(50,500)==0x292c30 AND PixelGetColor(900,100)==0x292c30 AND PixelGetColor(900,500)==0x292c30) Then
		 if (PixelGetColor(939,61)==0x6c6e71) Then
			$stop = 1
			ToolTip(1000,200, "Event board")
			MouseClick("left", 939,61)
		 EndIf
	  EndIf
	  
	  ;stuck in alliance quest window
	  $loading = PixelGetColor(384,142)
	  if ($loading==0x1a1a1a) Then
		 if (PixelGetColor(551,142)==0x1a1a1a) Then
			if (Not(PixelGetColor(504,142)==0x1a1a1a)) Then
			   $stop = 1
			   MsgBox(0,"alliance q", "empty alliance quest cuy", 1);
			   ;$arena_tier = 2
			   Sleep(2000)
			   MouseClick("left", 57, 55); 
			   Sleep(10000)
			EndIf
		 EndIf
	  EndIf
	  
	  ;MsgBox(0, "dbg", StringFormat("%X", PixelGetColor(18,130)), 1)
	  ; or the case we stuck in team adding
	  if (PixelGetColor(18, 130)==0x2b2c30) Then ; the left bar team list
		 if (PixelGetColor(936,511)==0x2b2c30) Then ;the champion filter button
			ToolTip("Team adding light", 1000,200)
			$stop = 1
			;Sleep(2000)
			if ($arena_tier==3 AND isInTeamAddingTier(3)) Then
			   ToolTip("in correct tier 3", 1000,200)
			   Sleep(1000)
			Else
			   Sleep(1000)
			   MouseClick("left", 57, 55); back
			   Sleep(1000)
			   MouseClick("left", 57, 55); back
			   Sleep(10000)
			EndIf
		 EndIf
	  EndIf
	  if (PixelGetColor(18, 130)==0x0b0b0c) Then ; the left bar team list
		 if (PixelGetColor(936,511)==0x0b0b0c) Then ;the champion filter button
			ToolTip("Team adding Dark", 1000,200)
			$stop = 1
			Sleep(1000)
			MouseClick("left", 100, 400);CLick to skip popup
			Sleep(2000)
			;Sleep(2000)
			if ($arena_tier==3 AND isInTeamAddingTier(3)) Then
			   ToolTip("in correct tier 3", 1000,200)
			Else
			   Sleep(1000)
			   MouseClick("left", 57, 55); back
			   Sleep(1000)
			   MouseClick("left", 57, 55); back
			   Sleep(10000)
			EndIf
		 EndIf
	  EndIf
	  
	  ;or the case we're in somewhere outside  (menu)
	  if (PixelGetColor(955,50)==0x2b2c30) Then
		 if (PixelGetColor(955, 562)==0x1d2630) Then
			if (Not(getDominantColor(PixelGetColor(936,556))=="green")) Then
			   $somewhereoutsidecounter = $somewhereoutsidecounter+1
			   if ($somewhereoutsidecounter>20) Then
				  MsgBox(0, "popup", "(somewhere outside for too long)", 2)
				  $stop = 1
				  Sleep(1000)
				  Send("J")
				  Sleep(1000)
				  MouseClick("left", 190, 58) ;menu
				  Sleep(1000)
				  MouseClick("left", 190, 58) ;menu double
				  Sleep(1000)
				  MouseClick("left", 270, 132) ;fight
				  Sleep(5000)
			   EndIf
			EndIf
		 EndIf
	  EndIf
	  
	  ;When blue stack service error.. The biggest to handle
	  Local $inside_launcher = False
	  Local $inside_login = False
	  $inside_launcher = False
	  Local $yellowlogo = PixelSearch(870,40,945,260, 0xf38025)
	  if (Not(@error)) Then
		 if (PixelGetColor($yellowlogo[0]+1, $yellowlogo[1]+1)==0xf38025) Then
			PixelSearch($yellowlogo[0]-10,$yellowlogo[1]-10, $yellowlogo[0]+50, $yellowlogo[1]+50, 0xffffff)
			if (Not(@error)) Then
			   $inside_launcher = True
			   ToolTip("inside launcher",1000,300)
			EndIf
		 EndIf
	  EndIf
	  ;if ((PixelGetColor(70,90)==0) AND (PixelGetColor(290,90)==0) AND (PixelGetColor(300,470)==0) AND (PixelGetColor(860,470)==0)) Then
		 ;Sleep(1000)
	  ;EndIf
	  $inside_login = False
	  if ((getDominantColor(PixelGetColor(745,500))=="blue") AND (getDominantColor(PixelGetColor(847,502))=="blue")) Then
		 if ((PixelGetColor(70,90)==0) AND (PixelGetColor(290,90)==0) AND (PixelGetColor(300,470)==0) AND (PixelGetColor(860,470)==0)  ) Then
			Sleep(2000)
			if ((getDominantColor(PixelGetColor(745,500))=="blue") AND (getDominantColor(PixelGetColor(847,502))=="blue")) Then
			   if ((PixelGetColor(70,90)==0) AND (PixelGetColor(290,90)==0) AND (PixelGetColor(300,470)==0) AND (PixelGetColor(860,470)==0)  ) Then
				  $inside_login = True
				  ToolTip("inside login",1000,300)
			   EndIf
			EndIf
		 EndIf
	  EndIf
	  if ($inside_launcher OR $inside_login) Then
		 
		 if ($inside_launcher) Then
			MsgBox(0, "bluestack", "bluestack error INSIDE LAUNCHER",20)
		 Else
			MsgBox(0, "bluestack", "bluestack error LOGIN ACCOUNT",20)
		 EndIf
		 $allstop=1
		 Sleep(2000)
		 MouseClick("left", 175,613);android window button
		 Sleep(2000)
		 MouseClickDrag("left", 900,310, 900,70);remove the bluestack service
		 Sleep(2000)
		 MouseClick("left", 121,613);android home button
		 Sleep(2000)
		 Local $repeat=10
		 Do
			MouseClickDrag("left", 500,100, 500, 550);upmost
			Sleep(1000)
			$repeat = $repeat-1
			if (PixelGetColor(175,125)==0x100c24 AND PixelGetColor(200,125)==0xf9c9c9 AND PixelGetColor(230,125)==0x3d2661 AND PixelGetColor(175,185)==0xEF1c23 AND PixelGetColor(200,185)==0x60606 AND PixelGetColor(230,185)==0x1d2735) Then
			   $repeat = 0
			EndIf
		 Until ($repeat<1)
		 MouseClick("left", 200,160);mcoc game
		 Sleep(30000)
		 Local $ccc = 0
		 Do
			ToolTip("not yet", 1000,300)
			Sleep(1000)
			$ccc = $ccc+1
		 Until ((PixelGetColor(276,172)==0x013000) OR $ccc>40)
		 gotoFightMenu()
		 Sleep(2000)
		 startArena()
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
		 
		 ;check if in event info
		 if (PixelGetColor(50,100)==0x292c30 AND PixelGetColor(50,500)==0x292c30 AND PixelGetColor(900,100)==0x292c30 AND PixelGetColor(900,500)==0x292c30) Then
			if (PixelGetColor(939,61)==0x6c6e71) Then
			   ToolTip(1000,200, "Event board (during fight)")
			   MouseClick("left", 939,61)
			EndIf
		 EndIf
	  EndIf
	  ;quest completed!
	  Local $ca = PixelGetColor(204,190)
	  if ($ca==0x2b2c30) Then
		 Local $cb = PixelGetColor(739,514)
		 if ($cb==0x2b2c30) Then
			if (getDominantColor(PixelGetColor(310,485))=="green" AND getDominantColor(PixelGetColor(741,485))=="green") Then
			   MsgBox(0,"finished", "i'm going to press the mid button (replay/next)", 2)
			   Sleep(4000)
			   MouseClick("left", 500,470)
			   Sleep(1000)
			   MouseClick("left", 500,470)
			EndIf
		 EndIf
	  EndIf

	  
   Until ($stop==1 or $allstop==1)
EndFunc

Func questplay()
   $quest_stop = 0
   Do
	  MouseClick("left", 190, 58) ;menu
	  Sleep(1000)
	  MouseClick("left", 190, 58) ;menu double
	  Sleep(1000)
	  MouseClick("left", 190, 58) ;menu double
	  Sleep(1000)
	  MouseClick("left", 190, 58) ;menu double
	  Sleep(1000)
	  MouseClick("left", 270, 132) ;fight
	  Sleep(500)
	  MouseClick("left", 270, 132) ;fight double
	  Sleep(10000)
	  
	  MouseClickDrag("left", 130, 255, 700, 255);drag left mosst for foolproof
	  Sleep(1000)
	  MouseClickDrag("left", 130, 255, 700, 255);drag left mosst for foolproof
	  Sleep(1000)
	  
	  MouseClick("left", 271,430);Event quest
	  Sleep(5000)
	  
	  ;Event specific 
	  MouseClick("left", 100,480)
	  Sleep(1000)
	  MouseClick("left", 100,480)
	  Sleep(3000)
	  MouseClick("left", 172,350)
	  Sleep(3000)
	  MouseClick("left", 384,294)
	  Sleep(3000)
	  MouseClick("left", 544,268)
	  ToolTip("3", 1000,100)
	  Sleep(3000)
	  ToolTip("2", 1000,100)
	  Sleep(3000)
	  ToolTip("1", 1000,100)
	  Sleep(3000)
	  MouseClick("left", 877,547)
	  ToolTip("3", 1000,100)
	  Sleep(3000)
	  ToolTip("2", 1000,100)
	  Sleep(3000)
	  ToolTip("1", 1000,100)
	  Sleep(3000)
	  fight();skip dialog until we can go to next node
	  nextNode()
	  ;end event specific
	  
   Until ($quest_stop==0 OR $allstop==0)
EndFunc

Func nextNode()
   $allstop = 0
   Do
	  Local $step = 0
	  Do
		 ;Check if out of energy
			if (checkEnergyIsEmpty()) Then
			   $arena_tier = 3
			   MsgBox(0,"out of energy", "my creator is away, i'll continue to arena to kill the time",2)
			   MouseClick("left", 148, 58) ;menu
			   Sleep(2000)
			   MouseClick("left", 148, 58) ;menu
			   Sleep(2000)
			   MouseClick("left", 148, 58) ;menu
			   Sleep(2000)
			   MouseClick("left", 270, 132) ;fight
			   Sleep(15000)
			   startArena()
			EndIf
		 ;End check
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
		 
		 ;check if in event info
		 if (PixelGetColor(50,100)==0x292c30 AND PixelGetColor(50,500)==0x292c30 AND PixelGetColor(900,100)==0x292c30 AND PixelGetColor(900,500)==0x292c30) Then
			if (PixelGetColor(939,61)==0x6c6e71) Then
			   ToolTip(1000,200, "Event board")
			   MouseClick("left", 939,61)
			EndIf
		 EndIf
		 
		 Send("J")
		 Sleep(200)
		 $greendot = PixelSearch(80,100, 957, 530, 0x00f800)
		 if (@error) Then
			ToolTip("1")
			$greendot = PixelSearch(80,100, 957, 530, 0x00e400)
		 EndIf
		 
		 if (@error) Then
			$pref = @error
			ToolTip("5")
			
			;check if teleport
			if (getDominantColor(PixelGetColor(445,445))=="green" AND getDominantColor(PixelGetColor(530,346))=="green") Then
			   ToolTip("3")
			   
			   setError(0);make error = false to break loop
;~ 			   dim $greendot[2];make array to break loop
			   $greendot = PixelSearch(0,0,0,0,PixelGetColor(0,0));language limitation workaround
			EndIf
		 Else
			ToolTip("4")
			if (PixelGetColor($greendot[0], $greendot[1]+25)==0 OR PixelGetColor($greendot[0]+25, $greendot[1])==0) Then
			   ToolTip("2")
			   setError(1);we dont want this found, make error = True
			Else
			   SetError(0);workaround
			EndIf
		 EndIf
	  
	  Until IsArray($greendot);not(@error)
	  Send("J")
	  
	  if (getDominantColor(PixelGetColor(445,445))=="green" AND getDominantColor(PixelGetColor(530,346))=="green") Then
		 ;Teleport
		 MouseClick("left", 445, 445)
		 Sleep(3000)
		 MouseClick("left", 835, 360)
	  Else
		 MouseMove($greendot[0], $greendot[1])
		 ToolTip(Stringformat("I will click this in 4s. (%d,%d)",$greendot[0], $greendot[1]),1000,200)
		 $file = FileOpen("questtilelog.txt", 1);write append
		 if ($file<>-1) Then
			FileWrite($file, StringFormat("(%d,%d)",$greendot[0], $greendot[1]) & @LF)
		 EndIf
		 FileClose($file)
		 Sleep(5000)
		 MouseClick("left", $greendot[0], $greendot[1])
		 Sleep(500)
		 MouseClick("left", $greendot[0], $greendot[1])
	  EndIf
	  Sleep(10000)

	  ;out of energy
	  if (PixelGetColor(255,163)==0x2b2c30 AND PixelGetColor(720,165)==0x2b2c30) Then
		 ;ToolTip("masuk2")
		 ;ToolTip(StringFormat("%X",PixelGetColor(294,336)));help llogo
		 if (getDominantColor(PixelGetColor(294,336))=="red") Then
			;ToolTip("dapet")
			$stop = 1
			   ;Sleep(7000)
			   ;MsgBox(0,"finished", "finished", 2)
			   ;MouseClick("left", 300,475);back to quest button
			   ;Sleep(15000)
			MsgBox(0,"finished", "out of energy", 2)
			
			MsgBox(0,"out of energy", "my creator is away, i'll continue to arena to kill the time",2)
			MouseClick("left", 148, 58) ;menu
			Sleep(2000)
			MouseClick("left", 148, 58) ;menu
			Sleep(2000)
			MouseClick("left", 148, 58) ;menu
			Sleep(2000)
			MouseClick("left", 270, 132) ;fight
			Sleep(15000)
			startArena()
		 EndIf
	  EndIf
	  
	  fight()
	  Sleep(4000)
	  Send("J")
   Until ($allstop==1)
EndFunc

;check energy is full
Func checkEnergyIsFull()
   if Not(PixelGetColor(499,61)==0xffe265) Then ; check the energy logo is there
	  ToolTip("cant check energy", 1000,100)
	  Return False
   EndIf
   $energycolor = PixelGetColor(597,62)
   Local $red = BitShift($energycolor , 16)
   Local $green = BitShift(BitAND($energycolor , 0x00FF00), 8)
   Local $blue = BitAND($energycolor , 0x0000FF)
   if ( (($red-$green)>45) AND ($blue<7) ) Then
	  Return True
   Else
	  Return False
   EndIf
EndFunc
;check energy is empty
Func checkEnergyIsEmpty()
   if Not(PixelGetColor(499,61)==0xffe265) Then ; check the energy logo is there
	  ToolTip("cant check energy", 1000,100)
	  Return False
   EndIf
   $energycolor = PixelGetColor(492,63)
   Local $red = BitShift($energycolor , 16)
   Local $green = BitShift(BitAND($energycolor , 0x00FF00), 8)
   Local $blue = BitAND($energycolor , 0x0000FF)
   if ( (($red-$green)>45) AND ($blue<7) ) Then
	  Return False
   Else
	  Return True
   EndIf
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


;perform check if we're stuck in a room (any current click affects nothing)
;return True if stuck, False if not
Func checkStuck()
   ; check if we're stuck in some room
   $samepixel = 0
   if (Not(PixelGetColor(100,100)==$screensave[0])) Then
	  Return False
   EndIf
   if (Not(PixelGetColor(400,100)==$screensave[1])) Then
	  Return False
   EndIf
   if (Not(PixelGetColor(700,100)==$screensave[2])) Then
	  Return False
   EndIf
   if (Not(PixelGetColor(100,500)==$screensave[3])) Then
	  Return False
   EndIf
   if (Not(PixelGetColor(498,298)==$screensave[4])) Then
	  Return False
   EndIf
   if (Not(PixelGetColor(700,500)==$screensave[5])) Then
	  Return False
   EndIf
   Return True
EndFunc

;update $screensave to current capture
Func updateCapture()
   if ($screenloading[0]==0) Then;Not yet captured
	  $screensave[0] = PixelGetColor(100,100)
	  if ($screensave[0]==0x142e3f) Then ;we don't want to save loading screen;TODO REUPDATGE THESE
		 $screensave[0] = 0
	  EndIf
	  $screensave[1] = PixelGetColor(400,100)
	  if ($screensave[1]==0x3c3c61) Then
		 $screensave[1] = 0
	  EndIf
	  $screensave[2] = PixelGetColor(700,100)
	  if ($screensave[2]==0x14385d) Then
		 $screensave[2] = 0
	  EndIf
	  $screensave[3] = PixelGetColor(100,500)
	  if ($screensave[3]==0x387293) Then
		 $screensave[3] = 0
	  EndIf
	  $screensave[4] = PixelGetColor(498,298)
	  if ($screensave[4]==0x676767) Then
		 $screensave[4] = 0
	  EndIf
	  $screensave[5] = PixelGetColor(700,500)
	  if ($screensave[5]==0x3c334c) Then
		 $screensave[5] = 0
	  EndIf
   Else
	  $screensave[0] = PixelGetColor(100,100)
	  if ($screensave[0]==$screenloading[0]) Then ;we don't want to save loading screen;
		 $screensave[0] = 0
	  EndIf
	  $screensave[1] = PixelGetColor(400,100)
	  if ($screensave[1]==$screenloading[1]) Then
		 $screensave[1] = 0
	  EndIf
	  $screensave[2] = PixelGetColor(700,100)
	  if ($screensave[2]==$screenloading[2]) Then
		 $screensave[2] = 0
	  EndIf
	  $screensave[3] = PixelGetColor(100,500)
	  if ($screensave[3]==$screenloading[3]) Then
		 $screensave[3] = 0
	  EndIf
	  $screensave[4] = PixelGetColor(498,298)
	  if ($screensave[4]==$screenloading[4]) Then
		 $screensave[4] = 0
	  EndIf
	  $screensave[5] = PixelGetColor(700,500)
	  if ($screensave[5]==$screenloading[5]) Then
		 $screensave[5] = 0
	  EndIf
   EndIf
EndFunc
;capture doesnt want loading screen, we capture loading screen manually here
Func updateCaptureLoading()
   $screenloading[0] = PixelGetColor(100,100)
   $screenloading[1] = PixelGetColor(400,100)
   $screenloading[2] = PixelGetColor(700,100)
   $screenloading[3] = PixelGetColor(100,500)
   $screenloading[4] = PixelGetColor(498,298)
   $screenloading[5] = PixelGetColor(700,500)
   ToolTip(StringFormat("%x %x %x,  %x %x %x", $screenloading[0],$screenloading[1],$screenloading[2],$screenloading[3],$screenloading[4],$screenloading[5]),1000,200)
EndFunc

;check if in home of the game, return true/false
Func checkInsideHome()
   if (getDominantColor(PixelGetColor(271,170))==getDominantColor(PixelGetColor(483,170)) AND getDominantColor(PixelGetColor(271,170))==getDominantColor(PixelGetColor(810,170)) AND getDominantColor(PixelGetColor(271,170))=="green") Then
	  ToolTip("we're home", 1000,400)
	  return True
   EndIf
   Return False
EndFunc

Func checkInsideFight()
   if (isInsideFight()) Then
	  ;MsgBox(0,"fight", "inside FIGHT!",1)
	  ToolTip("inside fight",1000,0)
	  ;Sleep(500)
	  MouseClick("left",200,200)
	  MouseClick("left",220,200)
	  $arena_continue = 0
	  fightArena()
	  return True
   Else
	  return False
   EndIf
EndFunc
;Check if currently in fight
;return 1 if true, 0 false
Func isInsideFight()
   ;check if there is pause button
   Local $leftborder = 0
   Local $rightborder = 0
   $leftborder = PixelGetColor(466,57)
   $rightborder = PixelGetColor(511,57)
   if ($leftborder==0x222222 OR $leftborder==0x212121) Then
	  if ($rightborder==0x222222 OR $rightborder==0x212121) Then
		 if ((PixelGetColor(483,57)==0x9cba9b AND PixelGetColor(493,57)==0x9cba9b) AND getDominantColor(PixelGetColor(488,57))=="green") Then
			return 1
		 EndIf
	  EndIf
   EndIf
   return 0
EndFunc


Func Duel()
   Local $count=10;Limit count here
   Do
	  Do
		 MouseClick("left", 276,97)
		 Sleep(3000)
	  Until (PixelGetColor(550,550)==0xffffff)
	  Send($duel_target, 1);name to search
	  Sleep(1000)
	  MouseClick("left", 772,102);search button
	  Sleep(5000)
	  if ($duel_target_pos==1) Then
	  ;1nd search position
		 MouseClick("left", 286,186)
		 Sleep(1000)
		 MouseClick("left", 445,156)
		 Sleep(4000)
	  ElseIf ($duel_target_pos==2) Then
	  ;2nd search position
		 MouseClick("left", 286,246)
		 Sleep(1000)
		 MouseClick("left", 445,216)
		 Sleep(4000)
	  ElseIf ($duel_target_pos==3) Then
	  ;3rd search pos 
		 MouseClick("left", 286,306)
		 Sleep(1000)
		 MouseClick("left", 445,256)
		 Sleep(4000)
	  endif
	  
	  MouseClick("left", 616,453);continue
	  Sleep(4000)
	  MouseClick("left", 103,547);start
	  fightDuel()
	  Sleep(2000)
	  $count = $count - 1
   Until ($allstop==1 OR $count==0)
EndFunc

;Fight in duel
Func fightDuel()
   $seq = 0
   $stop = 0
   $allstop = 0
   
   ;stuck in something handler
   Local $somewhereoutsidecounter = 0
   Local $stuckseq = 0
   Local $startarena = TimerInit()
   Local $arenatimersecond = 0
   Do
	  $stuckseq = $stuckseq+1
	  if (Mod($stuckseq,400)==0) Then
		 ;check if too long playing maybe something is not right
		 Local $dif = TimerDiff($startarena)
		 if ($dif > 30000) Then
			$startarena = TimerInit()
			$arenatimersecond = $dif/1000
		 EndIf
		 if ($arenatimersecond > 240) Then
			MsgBox(0, "popup", "too long minutes ", 3)
			Sleep(5000)
			MouseClick("left", 148, 58) ;menu
			Sleep(2000)
			MouseClick("left", 190, 58) ;menu double
			Sleep(2000)
			MouseClick("left", 270, 132) ;fight
			Sleep(10000)
		 EndIf
	  EndIf
	  
	  Send("0")
	  Sleep(1);
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
	  $loading = PixelGetColor(640, 540);
	  ;or chat bar has been clicked
	  if ($loading==0x161a1d) Then
		 if (PixelGetColor(136,540)==0x292c30) Then
			$stop = 1
			MsgBox(0,"chat", "this is chat window", 1)
			Sleep(1000)
			MouseClick("left", 943, 52); close
			Sleep(2000)
		 EndIf
	  EndIf
	  if (PixelGetColor(690,105)==0x161a1d AND PixelGetColor(800,105)==0x343434 AND PixelGetColor(841,105)==0x515151) Then
		 ;MsgBox(0, "done", "done", 1)
		 ToolTip("done",1000,200)
		 Sleep(2000)
		 $stop = 1
	  EndIf
   Until ($stop==1 or $allstop==1)
EndFunc
;Go to fight menu
Func gotoFightMenu()
   MouseClick("left", 190, 58) ;menu
   Sleep(1000)
   MouseClick("left", 190, 58) ;menu double
   Sleep(1000)
   MouseClick("left", 270, 132) ;fight
   Sleep(10000)
EndFunc
   
Func isInTeamAdding() 
   if (PixelGetColor(18, 130)==0x2b2c30 AND PixelGetColor(936,511)==0x2b2c30) Then ;the champion filter button
	  Return True
   ElseIf (PixelGetColor(18, 130)==0x0b0b0c AND PixelGetColor(936,511)==0x0b0b0c) Then ;the champion filter button
	  Return True
   EndIf
   Return False
EndFunc
;only check tier, not in team adding
Func isInTeamAddingTier($tier) 
   if ($tier = 3 AND PixelGetColor(108,559)==0x383838) Then
	  Return True
   EndIf
   ;TODO OTHER TIER
   Return False
EndFunc

;what todo like when in launcher
Func startOver()
   $allstop=1
   Sleep(2000)
   MouseClick("left", 175,613);android window button
   Sleep(2000)
   MouseClickDrag("left", 900,310, 900,70);remove the bluestack service
   Sleep(2000)
   MouseClick("left", 121,613);android home button
   Sleep(2000)
   Local $repeat=10
   Do
	  MouseClickDrag("left", 500,100, 500, 550);upmost
	  Sleep(1000)
	  $repeat = $repeat-1
   Until ($repeat<1)
   MouseClick("left", 200,160);mcoc game
   Sleep(30000)
   Local $ccc = 0
   Do
	  ToolTip("not yet", 1000,300)
	  Sleep(1000)
	  $ccc = $ccc+1
   Until ((PixelGetColor(276,172)==0x013000) OR $ccc>40)
   gotoFightMenu()
   Sleep(2000)
   startArena()
EndFunc