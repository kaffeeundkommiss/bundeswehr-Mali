# Setzt Logo-Umriss und Karte in index.html ein. Vorher: python3 werkzeuge/umriss.py <geojson>
# Aufruf im Repo-Ordner: python3 werkzeuge/seite_bauen.py
s = open('vorlage/index.vorlage.html').read()
logo = open('werkzeuge/umriss-logo.txt').read().strip()
karte = open('werkzeuge/karte.svg.txt').read().strip()
s = s.replace('@@LOGO@@', logo).replace('@@KARTE@@', karte)
open('index.html', 'w').write(s)
fav = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#CBB18C"/>'
       f'<path d="{logo}" fill="#4C5233" stroke="#4C5233" stroke-width="1.5" stroke-linejoin="round"/></svg>\n')
open('favicon.svg', 'w').write(fav)
print('index.html, favicon.svg geschrieben')
