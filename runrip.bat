@echo on
echo %CD%
start python "%CD%\processRip.py" "-profile" "A"
TIMEOUT 10
start python "%CD%\processRip.py" "-profile" "B"
TIMEOUT 10
start python "%CD%\processRip.py" "-profile" "C"
TIMEOUT 10
start python "%CD%\processRip.py" "-profile" "D"
TIMEOUT 10
start python "%CD%\processRip.py" "-profile" "E"
TIMEOUT 10
start python "%CD%\processRip.py" "-profile" "F"
TIMEOUT 10
REM start python "%CD%\rip.py" "-profile" "G"
REM TIMEOUT 10
pause