@echo off

where choco
if errorlevel 1 (
  @powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((new-object net.webclient).DownloadString('https://chocolatey.org/install.ps1'))"
  SET PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin
)

choco install python3 --confirm
choco install make    --confirm

make
