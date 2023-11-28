# Diese Datei dient nur zur Ablage unserer Prompts
# Sie können in der ./src/templates/openai_prompter.py getestet werden

self._client.chat.completions.create(
    model=model,
    messages=[
        # system: Dies definiert eine Systemnachricht, die Anweisungen oder Informationen für das Modell enthält, wie es antworten soll.
        {"role": "system", "content": """
            Den Prompt, den du von der Rolle user bekommst, enthält Titel und Text. Der Titel beschreibt den Text.
            Ich möchte aber bitte, dass du den Text kategorisierst. Ich möchte am Ende also Stichworte bekommen,
            die den Text beschreibt und anhand derer man direkt weiß, worum es im Text geht.
            Ein Sachbearbeiter soll so anhand von Kategorien, die passenden Texte schneller finden. Bitte ignoriere
            aufkommende Quellenverweise.
            """},
        # user: Nachricht des Benutzers
        {"role": "user", "content": prompt},
        # assistant Dies sind Antworten, die das Modell in früheren Dialogen generiert hat. Sie geben Kontext und zeigen,
        # wie das Modell auf vorherige Benutzeranfragen reagiert hat.
        {"role": "assistant", "content": """
            Bitte entnehme die 3 besten Kategorien, die am aussagekräftigsten und möglichst individuell 
            bzw. unterscheidbar sind. Am Ende sollten die 3 Kategorieren, die den Text am besten 
            wiederspiegeln dann so aufgelistet werden:
            1. 
            2. 
            3. 
        """},
        # {"role": "user", "content": "Where was it played?"}
    ]
)