@echo off  
:loop
start python main.py --config config.json
timeout /t 3600
goto :loop
exit 