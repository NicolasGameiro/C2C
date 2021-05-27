@ECHO on

REM set CannelleFolder=D:\Users\s053979\Cannelle\Cannelle_TEST_v4.07
set PyFolder=C:\Windows

set PYTHONINSTAL=%PyFolder%

set PYTHONPATH=%PYTHONINSTAL%

set pythonExe=%PYTHONINSTAL%"\py.exe" Appli.py
%pythonExe%

pause