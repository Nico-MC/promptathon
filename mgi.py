import os
import requests
import datetime
import json

from dotenv import load_dotenv
load_dotenv()

"""
Dieses Skript lädt eine Liste aller MGI-bekannten GOÄ-Ziffern und den dazugehörigen Informationen und speichert diese in einer json Datei
Möglicher Zifferinhalt:
* Ziffer
* Kommentare mit Scope GENERAL (MGI-Kommentare)
* Unverträglichkeiten
* Zusatznummern
* Bedingungen
* Originärnummern (Ursprungsnummern, wenn Ziffer eine Analogziffer ist)
* Querverweise - sind Verweise auf andere Ziffern oder Paragraphen/Präambeln der Gebührenordnung

Bestandteile können in Funktion `get_complete_go_nr` ein-/auskommentiert werden

BENUTZUNG

* Environment Variablen setzen
    * MGI_CLI_STAGE mit "dev" sonst wird default local angewandt
    * MGI_CLI_USER
    * MGI_CLI_PASS
* Skript ausführen
* Nach Abschluss ist Ergebnis als `ziffern.json` abgespeichert

Beispielbefehl unter Linux

```bash
export MGI_CLI_STAGE=local
export MGI_CLI_USER=moderator-user@red6-es.de
export MGI_CLI_PASS=password
python3 mgi.py
```

"""

stage = os.getenv("MGI_CLI_STAGE")

auth_url = "https://dev.account.martin-gebuehren.info/auth" if stage == "dev" else "http://localhost:8083/auth"
base_url = "https://dev.app.martin-gebuehren.info/api" if stage == "dev" else "http://localhost:8080/api"

username = os.getenv("MGI_CLI_USER")
password = os.getenv("MGI_CLI_PASS")

auth_header = dict()
token = ""


def log(msg: str):
    print(f"{datetime.datetime.now()} - {msg}")


def refresh_auth():
    """Holt den access_token vom Keycloak und speichert ihn in token Variable"""
    login_url = auth_url + "/realms/martin/protocol/openid-connect/token"
    form_data = dict(grant_type="password",client_id="martinClient",username=username,password=password)
    res: requests.Response = requests.post(login_url, data=form_data)
    
    if not res.ok or "access_token" not in res.json():
        raise IOError("Login failed", res.json())

    token = res.json()["access_token"]
    global auth_header
    auth_header = dict(Authorization="Bearer " + token)


def get_go_nrs():
    """Lädt die Liste aller MGI-bekannten GOÄ-Ziffern"""
    res = requests.get(base_url + "/ziffern/attrib/zifferNr", headers=auth_header)
    return res.json()


def get_ziffer_by_go_nr(go_nr: str):
    """Lädt den Ziffer Inhalt"""
    res = requests.get(base_url + "/ziffern/zifferNr/" + go_nr, headers=auth_header)
    body = res.json()
    ziffer = body["data"]

    # Nicht benötigte Properties können gelöscht werden
    # del ziffer["tarife"]

    return ziffer


def get_mgi_comments_by_go_nr(go_nr: str):
    """Lädt die Kommentare zu einer Ziffer und filtert alle nicht-MGI-Kommentare raus"""
    res = requests.get(base_url + "/kommentare/zifferNr/" + go_nr, headers=auth_header)
    try:
        comments: list[any] = res.json()
        mgi_comments = [x for x in comments if x["scope"]=="GENERAL"]
        return mgi_comments
    except Exception:
        log(f"Fehler beim Laden der Kommentare für GOÄ Nummer {go_nr}")
        log(f"{res.status_code} {res.reason}")
        return []


def get_unvertraeglichkeiten_by_go_nr(go_nr: str):
    res = requests.get(base_url + "/hinweise/unvertraeglichkeiten/zifferNr/" + go_nr, headers=auth_header)
    return res.json()


def get_bedingungen_by_go_nr(go_nr: str):
    res = requests.get(base_url + "/hinweise/bedingungen/zifferNr/" + go_nr, headers=auth_header)
    return res.json()


def get_zusatznummern_by_go_nr(go_nr: str):
    res = requests.get(base_url + "/hinweise/zusatznummern/zifferNr/" + go_nr, headers=auth_header)
    return res.json()


def get_originaernummern_by_go_nr(go_nr: str):
    res = requests.get(base_url + "/hinweise/originaer/zifferNr/" + go_nr, headers=auth_header)
    return res.json()


def get_querverweise_by_go_nr(go_nr: str):
    res = requests.get(base_url + "/hinweise/querverweise/zifferNr/" + go_nr, headers=auth_header)
    return res.json()


def get_complete_go_nr(go_nr: str):
    """
    Bei Bedarf benötigte Bestandteile ein-/auskommentieren
    """
    ziffer = get_ziffer_by_go_nr(go_nr)
    ziffer["kommentare"] = get_mgi_comments_by_go_nr(go_nr)
    # ziffer["unvertraeglichkeiten"] = get_unvertraeglichkeiten_by_go_nr(go_nr)
    # ziffer["zusatznummern"] = get_zusatznummern_by_go_nr(go_nr)
    # ziffer["bedingungen"] = get_bedingungen_by_go_nr(go_nr)
    # ziffer["originaernummern"] = get_originaernummern_by_go_nr(go_nr)
    # ziffer["querverweise"] = get_querverweise_by_go_nr(go_nr)

    return ziffer


def get_go_nrs_with_content():
    # Liste der Ziffern, die geladen und gespeichert werden sollen
    # Kann auch mit beliebigen Ziffern befüllt werden
    # go_nrs = ["G"]
    go_nrs = get_go_nrs()
    complete_ziffern = []

    log(f"Lade {len(go_nrs)} Ziffern...")
    n = 0
    for go_nr in go_nrs:
        complete_ziffern.append(get_complete_go_nr(go_nr))

        n += 1
        if n % 200 == 0:
            log(f"{n} Ziffern verarbeitet")
            # Token muss regelmäßig refresht werden
            refresh_auth()

    return complete_ziffern


def write_ziffern_to_json(ziffern):
    with open("ziffern.json", "w") as file:
        file.write(json.dumps(ziffern, ensure_ascii=False, indent=2))        


def main():
    log(f'Stage: {"local" if stage != "dev" else "dev"}')

    refresh_auth()
    log(f"Login als {username} erfolgreich")
    
    ziffern = get_go_nrs_with_content()
    write_ziffern_to_json(ziffern)

if __name__ == "__main__":
    main()
