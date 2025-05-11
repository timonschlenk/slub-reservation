# Sportkurse Bot

## Plan
Einen Bot mit Pyhton und der Bibliothek Selenium schreiben, der einen mithilfe einer Exceldatei automatisch SLUB Räume reserviert

## Installation
Folge den Schritten aus dem Tutorial: [Python Selenium Tutorial - Automate Websites and Create Bots](https://www.youtube.com/watch?v=NB8OceGZGjA) oder Befolge folgende Schritte:

1. Installiere eine aktuelle Version von Python
2. Installiere Selenium, Schedule und Openpyxl, gebe dafür ins Terminal ein:
```terminal
pip install selenium
pip install openpyxl
pip install schedule
```
3. Installiere eine aktuelle Version von Google Chrome oder Firefox und den dazugehörigen Driver ([Chrome](https://sites.google.com/chromium.org/driver/), [Firefox](https://github.com/mozilla/geckodriver))
4. Kopiere die Executable des Drivers in den root Ordner des Projekts und benenne sie ``` chromedriver.exe ```
5. Füge eine ``` config.json ``` Datei in den Root Ordner hinzu in welcher sich Passwort und Username befinden mit folgender Formatierung:
```json
{
   "username": "username",
   "password": "password"
}
```