# �� Zeta Proposer v1.0.1

## ✨ Features

- **KI-gestützte Konzeptgenerierung** mit OpenAI GPT-4o (Standard)
- **Word-Dokument-Export** mit professioneller Formatierung
- **JSON-Spezifikationsgenerierung** für Datenaustausch
- **Benutzerfreundliche GUI** für einfache Bedienung
- **OpenAI & Ollama Support** für Flexibilität
- **Automatische Diagramm-Erstellung** mit Graphviz
- **Template-Unterstützung** für verschiedene Dokumenttypen
- **Manuelle Projektnamen-Eingabe** für bessere Kontrolle
- **Konfigurierbare Wortanzahl-Grenzen** aus JSON

## 📥 Installation

1. **ZIP herunterladen** (unten klicken)
2. **Entpacken** in einen Ordner
3. **Zeta_Proposer.exe** starten
4. **Einstellungen** konfigurieren (OpenAI API Key)

## 🔧 Konfiguration

### OpenAI (Empfohlen - Beste Qualität)

1. Starten Sie `Zeta_Proposer.exe`
2. Klicken Sie auf "Einstellungen"
3. Wählen Sie "OpenAI" als Provider (Standard: GPT-4o)
4. Geben Sie Ihren API Key ein: `sk-your-openai-api-key-here`
5. Klicken Sie auf "Speichern"

### Ollama (Lokal - Datenschutz)

1. Installieren Sie Ollama von [https://ollama.ai](https://ollama.ai)
2. Starten Sie den Ollama-Service: `ollama serve`
3. Laden Sie ein Modell: `ollama pull llama3`
4. In der GUI: Wählen Sie "Ollama" als Provider (Standard: llama3)

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

## 🎯 Verwendung

1. **Projektname eingeben**: Aussagekräftigen Namen eingeben
2. **Beschreibung schreiben**: Detaillierte Projektbeschreibung
3. **Generate Technical Concept**: KI generiert Word-Dokument
4. **Generate from Specification**: KI generiert JSON-Datei
5. **Word-Dokument öffnet sich**: Sofort einsatzbereit

## 🆕 Neue Features in v1.0.1

- **JSON-Spezifikationsgenerierung**: Neue Schaltfläche "Generate from Specification"
- **Konfigurierbare JSON-Ausgabe**: Einstellbare JSON-Ausgabeordner
- **Verbesserte Fehlerbehandlung**: Robustere Fehlerbehandlung für Dateioperationen
- **Bugfixes**: Behebung von Indentierungsfehlern und Variablen-Scope-Problemen

## 🐛 Bekannte Probleme

- **Graphviz nicht gefunden**: Installieren Sie Graphviz von https://graphviz.org/download/
- **OpenAI API Key nicht gefunden**: Überprüfen Sie die Einstellungen
- **Word-Dokument kann nicht erstellt werden**: Überprüfen Sie Schreibrechte im `output/` Ordner
- **JSON-Datei kann nicht erstellt werden**: Überprüfen Sie Schreibrechte im `output/json/` Ordner

## 📞 Support

- **Log-Dateien**: `output/logs/` für Fehlerdiagnose
- **GitHub Issues**: Für Bug-Reports und Feature-Requests
- **README.md**: Detaillierte Anleitung im ZIP

## 🔄 Updates

- **Neue Versionen**: Über GitHub Releases
- **Changelog**: Siehe Release Notes
- **Breaking Changes**: Werden deutlich gekennzeichnet

---

**Entwickelt mit ❤️ für effiziente technische Dokumentation**

📦 **Download**: [Zeta_Proposer_v1.0.1.zip](link)
