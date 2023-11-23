from dotenv import load_dotenv
import os
from src.helpers.json_loader import load_json, sort_json
from src.templates.openai_prompter import OpenAIPrompter
from src.helpers.console_colors import ConsoleColors

# load environment variables (.env)
load_dotenv()

# load json file
json_file = os.getenv('JSON_FILE')
encoding = os.getenv('ENCODING')
comments = sort_json(load_json(json_file, encoding), json_file)

def print_comment_example():
    print("----- Beispielausgabe für einen Kommentar -----")
    goae_number = "1" #please only give string; can contain letters too.
    comment_number = 0
    # example how to call a specific comment (see end str)
    print(f"GOÄ-Ziffer: {goae_number}\nKommentar-Nr: {comment_number+1}/{len(comments[goae_number])} \
          \n\nKommentar: {comments[goae_number][comment_number]}\n\n")


# print_comment_example()


# connect with open ai api
prompter = OpenAIPrompter()


comment = comments["1"][0]
title = comment["title"]
text = comment["text"]

comment = "Gebe mir zu folgendem Kommentar beschreibende Keywords bzw. Kategorien, die am wichtigsten sind. \
Sie sollen 1 Wort lang sein. Anhand diese Kategorien sollte der Kommentar eindeutig zuweisbar sein und man \
sollte als Sachbearbeiter verstehen, worum es geht.\n\nTitel des Kommentars: \n" + comment["title"] + "\n\n \
Text des Kommentars: \n" + comment["text"]

comment = """Eine Definition der GOÄ lautet wie folgt: Die Gebührenordnung für Ärzte (GOÄ) regelt die Abrechnung privatärztlicher Leistungen, also medizinische Leistungen außerhalb der gesetzlichen Krankenversicherung. Die GOÄ enthält 5.545 Positionen, die in der Regel durch Nummern gekennzeichnet sind. Sie ist das zentrale Instrument zur Abrechnung von Leistungen, die nicht von den gesetzlichen Krankenkassen übernommen werden.
Zu vielen der Positionen, die mit Ziffern gekennzeichnet sind gibt es Kommentare, die genauer darauf eingehen, wie eine einzelne Ziffer in bestimmten Fällen zu interpretieren ist.
Jedem Kommentar sollen passende Kategorien zugewiesen werden, um die Arbeit von Sachbearbeitern auf der Suche nach den zu einem Anwendungsfall passenden Kommentaren zu erleichtern.


In diesem Fall soll es um die Ziffer Nummer 50 gehen, die den folgenden Titel:


"Besuch, einschließlich Beratung und symptombezogene Untersuchung"


Und folgende Allgemeine Hinweise enthält:


"- Nicht bei stationärer Behandlung
- Abrechnung bei Behandlung auf Intensivstation anstelle der Nr. 435 nicht zulässig.
- Nicht abrechnungsfähig für Krankenhaus- und Belegärzte für Besuche im Krankenhaus
- Nicht für Anästhesisten für Aufsuchen anderer Praxis zur Durchführung von Anästhesien
- Bei ambulanten Operationen (weil regelmäßiger Tätigkeitsort)
- Von den erlaubten (ob erlaubt, siehe unten !) Zuschlägen (ggf. E, F, G, H, J bzw. K2) ist
- Immer nur einer möglich."


Der erste Kommentar zu dieser Nummer 50 trägt die Überschrift:


"Nr. 50 nicht analog für "ambulante Visite""


und lautet wie folgt:


"Es ist nicht nachvollziehbar, was sich hinter dem Begriff "ambulante Visite" dargestellten Leistung verbirgt. Denkbar erscheint, dass die Gebühr für das Aufsuchen des Patienten im Aufwachraum nach erfolgter ambulanter Operation berechnet wird. Hierfür stehen aber in der GOÄ Untersuchungs -und Beratungsgebühren, beziehungsweise der Zuschlag nach der GOÄ-Nr. 448 oder 449 zur Verfügung. Die entsprechenden Bestimmungen sind zu beachten. Somit fehlt es an einer durch Analogie ausfüllungsbedürftigen Lücke in der Gebührenordnung. Die Nr. 50 analog für eine "ambulante Visite" kann daher nicht abgerechnet werden"


Diesem Kommentar können die folgenden Kategorien zugewiesen werden:


1. ambulante Visite
2."""

print(f"{ConsoleColors.OKCYAN}{comment}{ConsoleColors.ENDC}")

result = prompter.create_completion(comment, 200, 1)
print(f"{ConsoleColors.OKGREEN}{result}{ConsoleColors.ENDC}\n")


