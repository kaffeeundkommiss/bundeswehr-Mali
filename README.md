# bundeswehr-Mali

Statische Seite zum Einsatz der Bundeswehr in Mali 2013–2023 (MINUSMA und EUTM Mali): Kennzahlen, Karte, Zeitleiste, besondere Ereignisse, Ende des Einsatzes. Jede Angabe verweist auf ihre Quellen; Angaben mit nur einer Quelle oder nur amtlichen Quellen sind gekennzeichnet.

Seite: https://kaffeeundkommiss.github.io/bundeswehr-Mali/

- `index.html`: Überblick (wird aus `vorlage/index.vorlage.html` erzeugt, nicht direkt bearbeiten)
- `karte.html`: Karte und Standorte (wird aus `vorlage/karte.vorlage.html` erzeugt, nicht direkt bearbeiten)
- `vorlage/*.vorlage.html`: Text der Seiten mit Platzhaltern `@@LOGO@@` und `@@KARTE@@`
- `werkzeuge/umriss.py`: erzeugt Logo-Umriss und Karte aus Natural Earth (gemeinfrei)
- `werkzeuge/seite_bauen.py`: setzt Logo und Karte ein, schreibt `index.html`, `karte.html` und `favicon.svg`
- `seite.js`, `style.css`, `basis.css`, `tarn.svg`, `kk-tasse.svg`: aus dem Afghanistan-Repo übernommen (Design B, Bereich Sicherheitspolitik)
- `QUELLEN.md`: Belegmatrix mit offenen Punkten

Neu bauen nach Textänderungen: `python3 werkzeuge/seite_bauen.py`
Karte/Logo neu erzeugen: Natural-Earth-Datei `ne_50m_admin_0_countries.geojson` laden, dann `python3 werkzeuge/umriss.py <datei>` und `python3 werkzeuge/seite_bauen.py`.
