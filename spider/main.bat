@echo off  
:loop
start python main.py --config config.json
timeout /t 30
goto :loop
exit 