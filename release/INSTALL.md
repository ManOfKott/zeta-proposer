# 🚀 Zeta Proposer - Schnellstart

## Installation (2 Minuten)

### 1. Download & Entpacken

- Laden Sie `Zeta_Proposer.exe` herunter
- Erstellen Sie einen neuen Ordner für das Programm
- Kopieren Sie alle Dateien in diesen Ordner

### 2. KI-Provider konfigurieren

#### Option A: OpenAI (Empfohlen - Beste Qualität)

1. Starten Sie `Zeta_Proposer.exe`
2. Klicken Sie auf "Einstellungen"
3. Wählen Sie "OpenAI" als Provider
4. Geben Sie Ihren API Key ein: `sk-your-openai-api-key-here`
5. Klicken Sie auf "Speichern"

#### Option B: Ollama (Lokal - Geringere Qualität)

1. Installieren Sie Ollama von [https://ollama.ai](https://ollama.ai)
2. Starten Sie den Ollama-Service: `ollama serve`
3. Laden Sie ein Modell: `ollama pull llama3`
4. In der GUI: Wählen Sie "Ollama" als Provider
5. Klicken Sie auf "Speichern"

**Hinweis**: Ollama bietet Datenschutz durch lokale Ausführung, aber die Ergebnisse sind qualitativ schlechter als OpenAI.

### 3. Graphviz installieren (optional, für Diagramme)

- Download: https://graphviz.org/download/
- Installation mit Standardeinstellungen
- `dot` muss im System-PATH verfügbar sein

### 4. Programm starten

- Doppelklick auf `Zeta_Proposer.exe`
- Keine weitere Installation erforderlich!

## 📁 Ordnerstruktur

```
Zeta_Proposer/
├── Zeta_Proposer.exe          # Hauptprogramm
├── .env                       # OpenAI API Key (selbst erstellen)
├── README.md                  # Detaillierte Anleitung
├── section_descriptions.json  # Sektionen-Konfiguration
├── logging_config.json        # Logging-Einstellungen
├── config.json               # Automatisch erstellt (GUI-Einstellungen)
└── templates/                # Word-Templates
    └── Scriptum_Zeta_Project_Proposal_Template.docx
```

## ⚡ Erste Schritte

1. **Projektname eingeben**: Geben Sie einen aussagekräftigen Namen ein
2. **Beschreibung**: Beschreiben Sie Ihr Projekt detailliert
3. **Provider wählen**:
   - **OpenAI GPT-4**: Beste Qualität (empfohlen)
   - **Ollama**: Lokal, Datenschutz, aber geringere Qualität
4. **Generieren**: Klicken Sie auf "Generate Concept"

## 📤 Ausgabe

Generierte Dateien finden Sie im `output/` Ordner:

- Word-Dokumente: `output/docx/`
- Diagramme: `output/diagrams/`
- Logs: `output/logs/`

## 🆘 Hilfe

- Lesen Sie `README.md` für detaillierte Anleitung
- Log-Dateien in `output/logs/` für Fehlerdiagnose
- GitHub Issues für Support

---

**Viel Erfolg mit Zeta Proposer! 🎉**
