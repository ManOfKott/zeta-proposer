# Zeta Proposer - Section Configuration Guide

## 📋 Übersicht

Die `section_descriptions.json` Datei konfiguriert, wie jede Sektion des technischen Konzeptdokuments generiert wird. Du kannst Wortanzahlen, Diagramm-Anforderungen und Inhaltsrichtlinien für jede Sektion individuell anpassen.

## 🏗️ Struktur

### Grundlegende Sektionsstruktur

```json
{
  "section_key": {
    "title": "Anzeigetitel der Sektion",
    "description": "Detaillierte Beschreibung für die AI-Generierung",
    "content_requirements": ["Liste der Themen, die abgedeckt werden sollen"],
    "word_count": {
      "target": 250,
      "min": 150,
      "max": 325
    },
    "diagram": {
      "enabled": true,
      "type": "architecture",
      "description": "Was das Diagramm visualisieren soll",
      "requirements": ["Spezifische Anforderungen für das Diagramm"]
    }
  }
}
```

## ⚙️ Konfigurationsoptionen

### 1. Wortanzahl (word_count)

**Zweck**: Kontrolliert die Länge jeder Sektion

```json
"word_count": {
  "target": 250,    // Ideale Wortanzahl
  "min": 150,       // Minimale akzeptable Wortanzahl
  "max": 325        // Maximale akzeptable Wortanzahl (mit Toleranz)
}
```

**Vorgeschlagene Werte**:

- **Kurz**: `{"target": 150, "min": 100, "max": 200}`
- **Mittel**: `{"target": 250, "min": 150, "max": 325}`
- **Lang**: `{"target": 400, "min": 300, "max": 520}`

### 2. Diagramm-Konfiguration (diagram)

**Zweck**: Steuert, ob und wie Diagramme generiert werden

```json
"diagram": {
  "enabled": true,                    // Diagramm aktivieren/deaktivieren
  "type": "architecture",             // Diagramm-Typ
  "description": "Was visualisiert werden soll",
  "requirements": [                   // Spezifische Anforderungen
    "Anforderung 1",
    "Anforderung 2"
  ]
}
```

**Verfügbare Diagramm-Typen**:

- `context` - Systemgrenzen und Stakeholder
- `architecture` - Technische Komponenten und Beziehungen
- `integration` - Externe Schnittstellen und APIs
- `pipeline` - CI/CD Workflow-Stufen
- `testing` - Testing-Pyramide und Coverage
- `infrastructure` - Deployment und Infrastruktur
- `ux_ui` - User Journey und Interface-Flow

## 📝 Anpassung der Sektionen

### Beispiel: Neue Sektion hinzufügen

```json
{
  "custom_section": {
    "title": "Meine benutzerdefinierte Sektion",
    "description": "Beschreibe hier, was die AI generieren soll. Sei spezifisch und detailliert.",
    "content_requirements": [
      "Thema 1 - Was soll abgedeckt werden?",
      "Thema 2 - Welche Aspekte sind wichtig?",
      "Thema 3 - Welche Details brauchst du?"
    ],
    "word_count": {
      "target": 200,
      "min": 120,
      "max": 260
    },
    "diagram": {
      "enabled": true,
      "type": "context",
      "description": "Visualisiere die wichtigsten Komponenten und Beziehungen",
      "requirements": [
        "Zeige die Hauptkomponenten",
        "Markiere wichtige Beziehungen",
        "Verwende unterschiedliche Farben für verschiedene Ebenen"
      ]
    }
  }
}
```

### Beispiel: Bestehende Sektion anpassen

```json
{
  "system_scope": {
    "title": "System Scope and Boundaries",
    "description": "Deine angepasste Beschreibung hier...",
    "content_requirements": ["Deine angepassten Anforderungen hier..."],
    "word_count": {
      "target": 300, // Längere Sektion
      "min": 200,
      "max": 390
    },
    "diagram": {
      "enabled": false, // Diagramm deaktivieren
      "type": "context",
      "description": "Angepasste Diagramm-Beschreibung",
      "requirements": ["Deine angepassten Diagramm-Anforderungen"]
    }
  }
}
```

## 🎯 Best Practices

### 1. Beschreibungen schreiben

**Gut**:

```json
"description": "Beschreibe die Architektur des Systems, einschließlich der gewählten Technologien, Komponenten-Struktur und Kommunikationsmuster. Erkläre, warum diese Entscheidungen getroffen wurden und wie sie die Geschäftsanforderungen unterstützen."
```

**Schlecht**:

```json
"description": "Beschreibe die Architektur."
```

### 2. Content Requirements

**Gut**:

```json
"content_requirements": [
  "Architecture Overview - Welches Architekturmuster verwendest du?",
  "Technology Stack Selection - Warum diese spezifischen Technologien?",
  "Component Architecture - Wie sind Komponenten organisiert?"
]
```

**Schlecht**:

```json
"content_requirements": [
  "Architecture Overview",
  "Technology Stack",
  "Components"
]
```

### 3. Diagramm-Anforderungen

**Gut**:

```json
"requirements": [
  "Zeige alle Hauptsystemkomponenten (Frontend, Backend, Datenbank)",
  "Markiere Beziehungen zwischen Komponenten mit beschrifteten Pfeilen",
  "Verwende unterschiedliche Farben für verschiedene Technologie-Ebenen"
]
```

**Schlecht**:

```json
"requirements": [
  "Zeige Komponenten",
  "Zeige Beziehungen"
]
```

## 🔧 Erweiterte Konfiguration

### Diagramm-Typen im Detail

#### Context Diagram

```json
"diagram": {
  "type": "context",
  "description": "Visualisiere Systemgrenzen und Stakeholder",
  "requirements": [
    "Zeige Systemgrenzen klar mit einem Boundary-Box",
    "Inkludiere alle wichtigen Stakeholder (Benutzer, Admins, externe Systeme)",
    "Zeige externe Systeme und Abhängigkeiten",
    "Markiere die Hauptsystemkomponenten"
  ]
}
```

#### Architecture Diagram

```json
"diagram": {
  "type": "architecture",
  "description": "Zeige technische Komponenten und Beziehungen",
  "requirements": [
    "Zeige alle Hauptsystemkomponenten (Frontend, Backend, Datenbank, etc.)",
    "Markiere Beziehungen zwischen Komponenten mit beschrifteten Pfeilen",
    "Inkludiere Technologie-Stack-Informationen in Komponenten-Labels",
    "Zeige Datenfluss und Kommunikationsmuster",
    "Markiere Sicherheitsgrenzen und Authentifizierungsschichten"
  ]
}
```

## 🚀 Schnellstart

1. **Kopiere die Standard-Konfiguration**:

   ```bash
   cp section_descriptions.json section_descriptions_backup.json
   ```

2. **Bearbeite die JSON-Datei**:

   - Ändere Wortanzahlen nach deinen Bedürfnissen
   - Aktiviere/Deaktiviere Diagramme mit `"enabled": true/false`
   - Passe Beschreibungen und Anforderungen an

3. **Teste die Konfiguration**:
   - Starte die Zeta Proposer App
   - Generiere ein technisches Konzept
   - Überprüfe die Ergebnisse

## ❓ Häufige Fragen

**Q: Kann ich neue Sektionen hinzufügen?**
A: Ja! Füge einfach neue Einträge zur JSON-Datei hinzu. Die App erkennt automatisch neue Sektionen.

**Q: Wie aktiviere ich Diagramme für alle Sektionen?**
A: Setze `"enabled": true` in der `diagram`-Konfiguration jeder Sektion.

**Q: Kann ich die Reihenfolge der Sektionen ändern?**
A: Die Reihenfolge wird durch die JSON-Struktur bestimmt. Bearbeite die Datei entsprechend.

**Q: Was passiert, wenn ich die JSON-Datei lösche?**
A: Die App fällt auf die Standard-Konfiguration zurück.

## 📞 Support

Bei Fragen oder Problemen:

1. Überprüfe die JSON-Syntax mit einem JSON-Validator
2. Schau dir die Logs in `output/logs/` an
3. Teste mit kleinen Änderungen zuerst

---

**Version**: 1.0  
**Letzte Aktualisierung**: 2025-07-10
