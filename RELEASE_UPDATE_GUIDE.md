# 🔄 Release Update Guide

## Schneller Update (Empfohlen)

### 1. Batch-Script (Einfach)

```bash
update_release.bat
```

### 2. PowerShell-Script (Erweitert)

```powershell
# Standard Update
.\update_release.ps1

# Mit benutzerdefinierter Version
.\update_release.ps1 -Version "1.2"

# Nur Dateien kopieren (ohne Build)
.\update_release.ps1 -SkipBuild
```

## Manueller Update-Prozess

### 1. Code testen

```bash
# Änderungen testen
python main.py
```

### 2. Neue EXE erstellen

```bash
# Virtuelle Umgebung aktivieren
venv\Scripts\activate

# PyInstaller ausführen
pyinstaller zeta_proposer.spec
```

### 3. Release aktualisieren

```bash
# Neue EXE kopieren
copy dist\Zeta_Proposer.exe release\

# Templates-Ordner kopieren
xcopy templates release\templates /E /I /Y

# Konfigurationsdateien aktualisieren (falls geändert)
copy section_descriptions.json release\
copy logging_config.json release\
```

### 4. ZIP erstellen

```powershell
# Neue Version erstellen
powershell Compress-Archive -Path release\* -DestinationPath Zeta_Proposer_v1.1.zip -Force
```

## Was wird aktualisiert?

### ✅ **Automatisch aktualisiert:**

- `Zeta_Proposer.exe` - Hauptprogramm
- `section_descriptions.json` - Sektionen-Konfiguration
- `logging_config.json` - Logging-Einstellungen
- `README.md` - Dokumentation
- `INSTALL.md` - Installationsanleitung
- `templates/` - Word-Templates (wird automatisch kopiert)
- `output/` - Ausgabe-Ordnerstruktur (docx, json, logs)

### ⚠️ **Manuell prüfen:**

- `zeta_proposer.spec` - PyInstaller-Konfiguration
- `requirements.txt` - Abhängigkeiten
- README-Dateien - Falls neue Features hinzugefügt wurden

### 📝 **Nicht in Release enthalten:**

- `config.json` - Wird automatisch beim ersten Start erstellt (von Scripts ausgeschlossen)
- `release/` - Release-Ordner wird von Git ignoriert

## Git-Konfiguration

### .gitignore Einstellungen

Der `release/` Ordner wird automatisch von Git ignoriert:

```gitignore
# Generated releases
release/
Zeta_Proposer_v*.zip
```

### Release-Ordner aus Tracking entfernen

Falls der `release/` Ordner bereits getrackt wird:

```bash
# Release-Ordner aus Git-Tracking entfernen
git rm -r --cached release/
git commit -m "Remove release folder from tracking"
```

## Versionierung

### Version-Nummern:

- **v1.0** - Erste Version
- **v1.0.1** - JSON-Generierung und Bugfixes
- **v1.1** - Bugfixes, kleine Verbesserungen
- **v1.2** - Neue Features
- **v2.0** - Große Änderungen

### GitHub Release:

1. **ZIP hochladen** zu GitHub Releases
2. **Changelog** hinzufügen
3. **Version taggen** (v1.0.1, v1.1, v1.2, etc.)

## Troubleshooting

### Problem: Build schlägt fehl

```bash
# Abhängigkeiten aktualisieren
venv\Scripts\activate
pip install -r requirements.txt
```

### Problem: EXE zu groß

```bash
# PyInstaller-Optimierung
pyinstaller zeta_proposer.spec --strip --upx-dir=upx
```

### Problem: Fehlende Dateien

```bash
# Alle Dateien prüfen
dir release\
dir dist\
```

### Problem: Release-Ordner wird getrackt

```bash
# Überprüfen ob release/ in .gitignore steht
git check-ignore release/

# Falls nicht ignoriert, aus Tracking entfernen
git rm -r --cached release/
git commit -m "Remove release folder from tracking"
```

## Checkliste vor Release

- [ ] Code getestet
- [ ] EXE funktioniert
- [ ] Konfigurationsdateien aktuell
- [ ] README-Dateien aktuell
- [ ] ZIP-Archiv erstellt
- [ ] Version dokumentiert
- [ ] Release-Ordner wird von Git ignoriert

---

**Tipp**: Verwende die Scripts für konsistente Updates! 🚀
