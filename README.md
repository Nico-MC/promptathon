### Requirements:
- Follow these instructions: https://medium.com/@dipan.saha/managing-git-repositories-with-vscode-setting-up-a-virtual-environment-62980b9e8106#:~:text=Open%20a%20powershell%20terminal%20within,virtual%20environment%20to%20your%20workspace.

<mark>Ausführung von Skripts in Windows erlauben: set-executionpolicy remotesigned</mark>

### TL;DR
```
python -m venv .venv
.venv\Scripts\activate.ps1
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```

<mark>Caution: Shift + Control + P --> Click 'Python: Select Interpreter' --> select .venv</mark>


test new repository