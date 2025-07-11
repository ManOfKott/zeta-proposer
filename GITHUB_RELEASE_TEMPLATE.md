# 🚀 Zeta Proposer v1.0

## ✨ Features

- **KI-gestützte Konzeptgenerierung** mit OpenAI GPT-4o (Standard)
- **Word-Dokument-Export** mit professioneller Formatierung
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
├── diagrams/               # PNG-Diagramme
│   └── section_name.png
└── logs/                   # Log-Dateien
    └── zeta_log_YYYYMMDD_HHMMSS.log
```

## 🎯 Verwendung

1. **Projektname eingeben**: Aussagekräftigen Namen eingeben
2. **Beschreibung schreiben**: Detaillierte Projektbeschreibung
3. **Generate Concept klicken**: KI generiert automatisch
4. **Word-Dokument öffnet sich**: Sofort einsatzbereit

## 🐛 Bekannte Probleme

- **Graphviz nicht gefunden**: Installieren Sie Graphviz von https://graphviz.org/download/
- **OpenAI API Key nicht gefunden**: Überprüfen Sie die Einstellungen
- **Word-Dokument kann nicht erstellt werden**: Überprüfen Sie Schreibrechte im `output/` Ordner

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

📦 **Download**: [Zeta_Proposer_v1.0.zip](link)
