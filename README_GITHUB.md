# Zeta Proposer - Technical Concept Generator

Ein KI-gestützter Generator für technische Konzeptdokumente mit automatischer Diagramm-Erstellung und JSON-Spezifikationsgenerierung.

## 🚀 Download & Installation

### Für Endbenutzer (Einfachste Methode)

1. **Download**: Laden Sie die neueste `Zeta_Proposer.exe` aus dem [Releases](https://github.com/your-repo/releases) Bereich herunter
2. **Ausführen**: Doppelklicken Sie auf `Zeta_Proposer.exe` - keine Installation erforderlich!
3. **Konfiguration**: Erstellen Sie eine `.env` Datei im gleichen Ordner (siehe Konfiguration unten)

### Für Entwickler

```bash
git clone https://github.com/your-repo/zeta-proposer.git
cd zeta-proposer
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## 📋 Voraussetzungen

- **Windows 10/11** (für die EXE-Version)
- **OpenAI API Key** (für KI-Generierung)
- **Graphviz** (für Diagramm-Erstellung)

## ⚙️ Konfiguration

### 1. OpenAI API Key einrichten

Erstellen Sie eine `.env` Datei im gleichen Ordner wie die EXE:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 2. Graphviz installieren (für Diagramme)

1. Laden Sie Graphviz von [https://graphviz.org/download/](https://graphviz.org/download/) herunter
2. Installieren Sie es mit den Standardeinstellungen
3. Stellen Sie sicher, dass `dot` im System-PATH verfügbar ist

## 🎯 Verwendung

### Schritt 1: Projektname eingeben

- Geben Sie einen aussagekräftigen Projektnamen ein

### Schritt 2: Projektbeschreibung

- Beschreiben Sie Ihr Projekt detailliert
- Je mehr Details, desto bessere Ergebnisse

### Schritt 3: KI-Provider wählen

- **OpenAI GPT-4**: Beste Qualität (empfohlen)
- **OpenAI GPT-3.5**: Schneller, günstiger

### Schritt 4: Generierung starten

- **Word-Dokument**: Klicken Sie auf "Generate Technical Concept"
- **JSON-Spezifikation**: Klicken Sie auf "Generate from Specification"
- Das System erstellt automatisch:
  - Technische Konzeptdokumente
  - Diagramme (falls aktiviert)
  - Word-Dokumente mit allen Sektionen
  - JSON-Dateien für Datenaustausch

## 📁 Ausgabe

Generierte Dateien werden im `output/` Ordner gespeichert:

```
output/
├── docx/                    # Word-Dokumente
│   └── Projektname_YYYY-MM-DD.docx
├── json/                    # JSON-Spezifikationsdateien
│   └── Projektname_YYYY-MM-DD.json
├── diagrams/               # PNG-Diagramme
│   └── section_name.png
└── logs/                   # Log-Dateien
    └── zeta_log_YYYYMMDD_HHMMSS.log
```

## 🔧 Sektionen-Konfiguration

Die Sektionen können in `section_descriptions.json` angepasst werden:

```json
{
  "system_scope": {
    "description": "Beschreibung der Sektion...",
    "word_count": {
      "target": 70,
      "min": 30,
      "max": 100
    },
    "diagram": {
      "enabled": false
    }
  }
}
```

## 🎨 Features

- ✅ **KI-gestützte Inhaltsgenerierung**
- ✅ **Automatische Diagramm-Erstellung**
- ✅ **Word-Dokument-Export**
- ✅ **JSON-Spezifikationsgenerierung**
- ✅ **Template-Unterstützung**
- ✅ **Manuelle Projektnamen-Eingabe**
- ✅ **Konfigurierbare Wortanzahl-Grenzen**
- ✅ **Logging und Debugging**
- ✅ **Benutzerfreundliche GUI**

## 🐛 Troubleshooting

### Problem: "OpenAI API Key nicht gefunden"

**Lösung**: Erstellen Sie eine `.env` Datei mit Ihrem API Key

### Problem: "Graphviz nicht gefunden"

**Lösung**: Installieren Sie Graphviz und fügen Sie es zum PATH hinzu

### Problem: "Word-Dokument kann nicht erstellt werden"

**Lösung**: Stellen Sie sicher, dass der `output/` Ordner beschreibbar ist

### Problem: "JSON-Datei kann nicht erstellt werden"

**Lösung**: Stellen Sie sicher, dass der `output/json/` Ordner beschreibbar ist

### Problem: "Keine Internetverbindung"

**Lösung**: Überprüfen Sie Ihre Internetverbindung für OpenAI API

## 📞 Support

Bei Problemen oder Fragen:

1. Überprüfen Sie die Log-Dateien in `output/logs/`
2. Erstellen Sie ein Issue auf GitHub
3. Kontaktieren Sie den Entwickler

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz.

---

**Entwickelt mit ❤️ für effiziente technische Dokumentation**
