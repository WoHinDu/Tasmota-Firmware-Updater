# Tasmota Firmware Updater
Script um alle eure Sonoff Geräte mit Tasmota Firmware auf einmal zu aktualisieren.

![screenshot](final.JPG)

# Vor- und Nachteile
- Funktioniert ohne Internet
- klein und schlank
- kann nur Updaten; nicht mehr
- Python benötigt

# Voraussetzungen
- Python 3
- selbstcompilierte Firmwares (normal + minimal) mit WIFI_RETRY, euren Wlan-Daten und dem Webserver aktiviert

# Anleitung
- Abhängigkeiten installieren: "pip install requests"
- settings.json öffnen und eure Zugangsdaten für jedes Gerät eingeben
- In den selben Ordner kopiert ihr eure Firmwares und benennt diese nach "firmware.bin" und "firmware-minimal.bin" um
- Datei "upgrade.py" ausführen und den Anweisungen folgen