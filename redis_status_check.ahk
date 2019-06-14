;#InstallKeybdHook
#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
;#Warn  ; Recommended for catching common errors.
#Persistent
#SingleInstance force

#IfTimeout 10 ; Set the timeout to 10 ms.

SetTimer, check_redis_hb, 5000

check_redis_hb:
; MsgBox % ComObjCreate("WScript.Shell").Exec("cmd.exe /q /c dir").StdOut.ReadAll()
; MsgBox % ComObjCreate("WScript.Shell").Exec("C:\Python\Redis-x64-3.2.100\redis-cli.exe -r 3 ping").StdOut.ReadAll()

FileDelete, c:\Python\check_redis_hb.txt
Run, %ComSpec% /c C:\Python\Redis-x64-3.2.100\redis-cli.exe ping>c:\Python\check_redis_hb.txt, , ,outputPid
;msgbox %outputPid%
sleep, 1000
FileGetSize, OutputVar, c:\Python\check_redis_hb.txt
if OutputVar > 0
{
  SplashTextOn, 400, 300, Clipboard, Redis Server Seems OK
  sleep, 500
  SplashTextOff
  WinGetTitle, Title, ahk_pid %outputPid%
  ;msgbox %Title%
  if InStr(Title, "cmd.exe")
    winkill, ahk_pid %outputPid%
}
else
{
    ;msgbox %outputPid%
    WinGetTitle, Title, ahk_pid %outputPid%
    ;msgbox %Title%
    if InStr(Title, "cmd.exe")
      winkill, ahk_pid %outputPid%
    run C:\Python\Redis-x64-3.2.100\redis-server.exe
}
return

F1:
return
