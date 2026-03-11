# Modern Flask Calculator (SmartCalc)

Ein wissenschaftlicher Web-Taschenrechner, der auf Flask basiert. Dieses Projekt ist eine Migration eines ursprünglichen `tkinter`-basierten Python-Rechners in eine moderne Webanwendung mit Clean Code und einem ansprechenden User Interface.

## Features

- **Wissenschaftliche Funktionen**: Unterstützung für `sin`, `cos`, `tan`, `log`, `ln`, `exp`, Wurzeln (`√`) und Potenzen (`^`).
- **Verlaufsmanagement**: Alle Berechnungen werden in einem Verlauf gespeichert, der jederzeit eingesehen oder gelöscht werden kann.
- **Modernes UI**: Responsives Design mit "Glassmorphism"-Effekten, optimiert für Desktop und Mobile.
- **Dark/Light Mode**: Wechselbares Theme, das über `localStorage` im Browser gespeichert wird.
- **Tastatursteuerung**: Unterstützung für direkte Eingaben über die Tastatur (Zahlen, Operatoren, Enter für Ergebnis).

## Technologien

- **Backend**: Python 3, Flask
- **Frontend**: HTML5, Vanilla CSS3 (CSS Variables, Flexbox/Grid), JavaScript (ES6, Fetch API)
- **Logik**: `math` Modul für präzise Berechnungen, `re` für Ausdrucks-Sanitizing.

## Installation & Start

1. **Repository klonen** (oder Dateien herunterladen).
2. **Abhängigkeiten installieren**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Anwendung starten**:
   ```bash
   python app.py
   ```
4. **Browser öffnen**: Navigiere zu `http://127.0.0.1:5000`.

## Projektstruktur

- `app.py`: Flask-Server mit Berechnungslogik und API-Endpoints.
- `templates/index.html`: Struktur der Web-Oberfläche.
- `static/css/style.css`: Modernes Design und Theming.
- `static/js/script.js`: Frontend-Interaktionen und API-Kommunikation.
- `requirements.txt`: Benötigte Python-Pakete.

## Sicherheitshinweis
Die Anwendung nutzt `eval()` zur Auswertung mathematischer Ausdrücke. Um Sicherheitsrisiken zu minimieren, werden alle Eingaben gegen eine strikte Whitelist erlaubter Zeichen geprüft und in einem isolierten Kontext ohne Zugriff auf Systemfunktionen ausgeführt.
