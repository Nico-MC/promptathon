# Martin AI

Martin AI is the repository for all the code to improve Martin-Gebühren-Info and its content with artificial intelligence.

## Classification Promptathon

### Aktuelle TODOs
- Alle Kommentare einer goä ziffer anhand der Präfixe kategorisieren

### Requirements:
- Follow these instructions: https://medium.com/@dipan.saha/managing-git-repositories-with-vscode-setting-up-a-virtual-environment-62980b9e8106#:~:text=Open%20a%20powershell%20terminal%20within,virtual%20environment%20to%20your%20workspace.

<mark>CAUTION ⚠️: Bei Kodierungsfehler folgende Schritte machen:</mark>
- JSON in Notepad++ öffnen
- Unten rechts auf Kodierung (z.B. ANSI) rechtsklicken und Convert to UTF-8
- abspeichern
</br></br>

<mark>CAUTION ⚠️: Bei Skriptfehler in Windows folgenden Schritt durchführen (Ausführung von Skripts in Windows erlauben):</mark>
- JSON in Notepad++ öffnen

### TL;DR
```
python -m venv .venv
.venv\Scripts\activate.ps1
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```

<mark>(Optional) Shift + Control + P --> Click 'Python: Select Interpreter' --> select .venv</mark>


### Chat Completions Parameter
Erstellung der Anfrage:

response = self._client.chat.completions.create(...): Dieser Teil des Codes sendet eine Anfrage an das Sprachmodell. self._client.chat.completions.create ruft die Funktion auf, die die Komplettierungen (oder Antworten) vom Modell generiert.
Modellparameter:

model=model: Hier geben Sie an, welches Modell verwendet werden soll. model ist eine Variable, die den Namen des Modells enthält, z.B. text-davinci-003 oder ein ähnliches Modell.
Nachrichten und Rollen:

messages=[...]: Dies ist eine Liste von Nachrichten, die Teil des Dialogs sind. Jede Nachricht hat eine Rolle und einen Inhalt.
- "role": "system": Dies definiert eine Systemnachricht, die Anweisungen oder Informationen für das Modell enthält, wie es antworten soll. Zum Beispiel: "content": "You are a helpful assistant." teilt dem Modell mit, dass es in der Rolle eines hilfreichen Assistenten antworten soll.
- "role": "user": Dies sind Nachrichten, die vom Benutzer stammen, wie Fragen oder Kommentare. Zum Beispiel: "content": "Who won the world series in 2020?".
- "role": "assistant": Dies sind Antworten, die das Modell in früheren Dialogen generiert hat. Sie geben Kontext und zeigen, wie das Modell auf vorherige Benutzeranfragen reagiert hat.
Erhalt der Antwort:

Nach dem Senden der Anfrage liefert das Modell eine Antwort basierend auf den bereitgestellten Nachrichten und Rollen.
In der Webanwendung, wenn Sie mit dem Modell interagieren, wird dieser Prozess im Hintergrund ausgeführt. Sie geben Ihre Nachricht ein, und die Anwendung sendet diese Nachricht zusammen mit dem Kontext (frühere Nachrichten im Dialog) an das Modell, um eine Antwort zu erhalten. Die Rollen in der API-Anfrage helfen dem Modell zu verstehen, wer spricht und in welchem Kontext, um eine relevante und kohärente Antwort zu generieren.