# Zeta Proposer - Technical Concept Generator

Ein intelligentes Tool zur automatischen Generierung technischer Konzepte aus Software-Projektbeschreibungen.

## Features

- **KI-gestützte Analyse**: Unterstützt sowohl OpenAI GPT als auch Ollama für die Konzeptgenerierung
- **Intelligente Diagrammerstellung**: Automatische Erstellung von Architektur- und Systemdiagrammen mit Microsoft Visio
- **Professionelle Word-Dokumente**: Generierung strukturierter technischer Konzepte im .docx-Format
- **JSON-Spezifikationsgenerierung**: Erstellung von JSON-Dateien aus Projektspezifikationen für einfache Datenaustausch
- **Benutzerfreundliche GUI**: Einfache Bedienung über eine intuitive grafische Oberfläche
- **Flexible Eingabe**: Texteingabe über GUI oder zukünftig auch über TXT-Dateien

## Installation

### Voraussetzungen

- Python 3.8 oder höher
- Microsoft Visio (für Diagrammerstellung)
- Windows-Betriebssystem (für Visio-Integration)

### Setup

1. **Repository klonen oder herunterladen**

2. **Virtuelles Environment aktivieren**

   ```bash
   # Windows PowerShell
   .\venv\Scripts\Activate.ps1

   # Windows Command Prompt
   .\venv\Scripts\activate.bat
   ```

3. **Abhängigkeiten installieren**

   ```bash
   pip install -r requirements.txt
   ```

4. **Konfiguration einrichten**

   - Kopiere `env_example.txt` zu `.env`
   - Trage deine API-Keys ein:

     ```
     # Für OpenAI
     OPENAI_API_KEY=dein_openai_api_key

     # Für Ollama (optional)
     OLLAMA_URL=http://localhost:11434
     OLLAMA_MODEL=llama3.2
     ```

## Verwendung

### GUI starten

```bash
python main.py
```

### Workflow

1. **KI-Provider auswählen**: Wähle zwischen OpenAI und Ollama
2. **Konfiguration**: Klicke auf "Configure" um API-Keys einzustellen
3. **Projektbeschreibung eingeben**: Beschreibe dein Software-Projekt
4. **Konzept generieren**: Klicke auf "Generate Technical Concept" für Word-Dokumente
5. **JSON generieren**: Klicke auf "Generate from Specification" für JSON-Dateien
6. **Ergebnis**: Die Dokumente werden im `output/`-Ordner gespeichert

### Beispiel-Projektbeschreibung

```
E-Commerce-Plattform für lokale Händler

Wir entwickeln eine Online-Plattform, die lokalen Händlern ermöglicht, ihre Produkte online zu verkaufen.
Die Plattform soll folgende Features haben:
- Benutzerregistrierung und -verwaltung
- Produktkatalog mit Kategorien
- Warenkorb und Checkout-System
- Zahlungsabwicklung (PayPal, Kreditkarte)
- Bestellverfolgung
- Admin-Dashboard für Händler
- Mobile-responsive Design

Die Zielgruppe sind kleine bis mittlere lokale Geschäfte, die bisher noch nicht online vertreten sind.
```

## Projektstruktur

```
zeta proposer/
├── src/
│   ├── __init__.py
│   ├── gui.py              # Haupt-GUI-Anwendung
│   ├── ai_service.py       # KI-Service-Manager
│   ├── word_generator.py   # Word-Dokument-Generator
│   └── visio_diagram.py    # Visio-Diagramm-Generator
├── output/                 # Generierte Dokumente
│   ├── docx/              # Word-Dokumente
│   ├── json/              # JSON-Spezifikationsdateien
│   └── logs/              # Log-Dateien
├── venv/                   # Virtuelles Environment
├── requirements.txt        # Python-Abhängigkeiten
├── main.py                 # Haupt-Einstiegspunkt
├── env_example.txt         # Beispiel-Konfiguration
└── README.md              # Diese Datei
```

## Technische Details

### KI-Integration

- **OpenAI**: Verwendet die OpenAI API für hochwertige Konzeptgenerierung
- **Ollama**: Lokale KI-Modelle über Ollama-API für Datenschutz

### Diagrammerstellung

- **Microsoft Visio**: Automatische Erstellung von:
  - Systemarchitektur-Diagrammen
  - Datenfluss-Diagrammen
  - Komponenten-Interaktions-Diagrammen
- **Export**: PNG-Format für Word-Integration

### Word-Dokumente

- **Struktur**: Professionelle Gliederung mit Inhaltsverzeichnis
- **Inhalte**: Alle wichtigen technischen Aspekte
- **Diagramme**: Automatische Einbettung der generierten Visualisierungen

## Zukünftige Features

- [ ] TXT-Datei-Automatisierung für Batch-Verarbeitung
- [ ] Erweiterte Diagrammtypen
- [ ] Export in weitere Formate (PDF, HTML)
- [ ] Template-System für verschiedene Projekttypen
- [ ] Integration weiterer KI-Provider

## Troubleshooting

### Visio-Fehler

- Stelle sicher, dass Microsoft Visio installiert ist
- Überprüfe, ob Visio über COM-Automation erreichbar ist
- **Hinweis**: Das Programm funktioniert auch ohne Visio - Diagramme werden dann übersprungen

### API-Fehler

- Überprüfe deine API-Keys in der `.env`-Datei
- Stelle sicher, dass die Internetverbindung funktioniert (für OpenAI)
- Für OpenAI: Überprüfe dein API-Limit und Guthaben

### Ollama-Verbindung

- Starte den Ollama-Service: `ollama serve`
- Überprüfe die URL in der Konfiguration
- Stelle sicher, dass das gewählte Modell installiert ist: `ollama list`

### Allgemeine Probleme

- **Import-Fehler**: Führe `pip install -r requirements.txt` aus
- **GUI startet nicht**: Überprüfe Python-Version (3.8+ erforderlich)
- **Word-Dokument wird nicht erstellt**: Überprüfe Schreibrechte im `output/`-Ordner

## Lizenz

Dieses Projekt ist für private und kommerzielle Nutzung freigegeben.

## Support

Bei Fragen oder Problemen erstelle ein Issue im Repository oder kontaktiere den Entwickler.
