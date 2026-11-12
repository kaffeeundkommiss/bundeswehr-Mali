# Erzeugt den Umriss Malis (Logo, Favicon) und die Übersichtskarte aus Natural Earth (gemeinfrei).
# Eingabe: ne_50m_admin_0_countries.geojson (Logo) und ne_10m_admin_0_countries.geojson (Karte,
#   gleicher Maßstab 1:10 Mio. wie die Karten der Afghanistan- und Kosovo-Seite)
#   https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson
#   https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_admin_0_countries.geojson
# Aufruf: python3 werkzeuge/umriss.py PFAD/ne_50m.geojson PFAD/ne_10m.geojson
# Die Karte nutzt die Klassen der Afghanistan-/Kosovo-Karten (kartesvg, nachbar, landname, ort de/haupt).
import json, math, sys
d = json.load(open(sys.argv[1]))
geo = {f['properties']['ADMIN']: f['geometry'] for f in d['features']}
geo10 = {f['properties']['ADMIN']: f['geometry'] for f in json.load(open(sys.argv[2]))['features']}

def rings(g):
    if g['type'] == 'Polygon': return [g['coordinates'][0]]
    return [p[0] for p in g['coordinates']]

def dp(pts, eps):
    if len(pts) < 3: return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1; n = math.hypot(dx, dy) or 1e-9
    i, m = 0, 0
    for k in range(1, len(pts) - 1):
        x, y = pts[k]; t = abs(dy * x - dx * y + x2 * y1 - y2 * x1) / n
        if t > m: i, m = k, t
    if m > eps: return dp(pts[:i + 1], eps)[:-1] + dp(pts[i:], eps)
    return [pts[0], pts[-1]]

K = math.cos(math.radians(17))  # mittlere Breite Malis

def pfad(g, f, eps):
    out = []
    for r in rings(g):
        pts = [f(lon, lat) for lon, lat in r][:-1]  # Ring öffnen
        j = max(range(len(pts)), key=lambda k: math.hypot(pts[k][0]-pts[0][0], pts[k][1]-pts[0][1]))
        pts = dp(pts[:j + 1], eps)[:-1] + dp(pts[j:] + [pts[0]], eps)[:-1]
        if len(pts) < 4: continue
        out.append('M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + 'Z')
    return ' '.join(out)

# 1) Logo 64 x 64
mali = rings(geo['Mali'])[0]
xs = [lon * K for lon, _ in mali]; ys = [-lat for _, lat in mali]
w, h = max(xs) - min(xs), max(ys) - min(ys); s = 56 / max(w, h)
ox = (64 - w * s) / 2 - min(xs) * s; oy = (64 - h * s) / 2 - min(ys) * s
logo = pfad(geo['Mali'], lambda lon, lat: (lon * K * s + ox, -lat * s + oy), 0.35)
open('werkzeuge/umriss-logo.txt', 'w').write(logo + '\n')

# 2) Karte: Ausschnitt 13° W bis 6° O, 9° N bis 26° N
W, E, S_, N = -13.5, 5.5, 9.0, 26.0
B = 600; sk = B / ((E - W) * K)
H = (N - S_) * sk
f = lambda lon, lat: ((lon - W) * K * sk, (N - lat) * sk)
nachbarn = [('Algeria', 'Algerien'), ('Niger', 'Niger'), ('Burkina Faso', 'Burkina Faso'), ('Ivory Coast', 'Elfenbeinküste'),
            ('Guinea', 'Guinea'), ('Senegal', 'Senegal'), ('Mauritania', 'Mauretanien')]
teile = []
for n, de in nachbarn:
    teile.append(f'<path class="nachbar" d="{pfad(geo10[n], f, 0.6)}"><title>{de}</title></path>')
teile.append(f'<path class="mali" d="{pfad(geo10["Mali"], f, 0.4)}"><title>Mali</title></path>')
for name, lon, lat in [('Algerien', 1.5, 24.5), ('Mauretanien', -10.5, 20.5), ('Niger', 4.2, 17.8), ('Burkina Faso', -1.5, 12.0), ('Guinea', -11.0, 10.4), ('Senegal', -12.6, 14.6), ('Elfenbeinküste', -6.2, 9.6), ('Mali', -4.0, 18.0)]:
    x, y = f(lon, lat)
    teile.append(f'<text class="{"landname kos" if name=="Mali" else "landname"}" x="{x:.1f}" y="{y:.1f}">{name}</text>')
# Ortssymbole wie Afghanistan/Kosovo: haupt = Hauptstadt, de = Standort der Bundeswehr. Lage ungefähr (Grad, gerundet)
orte = [
    ('Bamako', -8.0, 12.65, 'haupt', 'end', -10, 4),
    ('Koulikoro', -7.56, 12.86, 'de', 'start', 10, -6),
    ('Gao', -0.04, 16.27, 'de', 'start', 10, 4),
]
for name, lon, lat, art, anker, dx, dy in orte:
    x, y = f(lon, lat)
    teile.append(f'<g class="ort {art}"><circle cx="{x:.1f}" cy="{y:.1f}" r="5"/><text x="{x+dx:.1f}" y="{y+dy:.1f}" text-anchor="{anker}">{name}</text></g>')
svg = (f'<svg class="kartesvg malikarte" viewBox="0 0 {B} {H:.0f}" role="img" aria-labelledby="karte-titel">'
       f'<title id="karte-titel">Karte Malis mit Nachbarstaaten und den Orten Bamako, Koulikoro und Gao</title>' + ''.join(teile) + '</svg>')
open('werkzeuge/karte.svg.txt', 'w').write(svg + '\n')
print(len(logo), len(svg))
