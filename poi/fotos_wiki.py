"""Descarga la imagen principal (Wikipedia/Commons) y las coordenadas de cada lugar, con licencia y autor."""
import json, urllib.request, urllib.parse, os, re, html
UA = {'User-Agent': 'MaratonElcheAlicanteVideo/1.0 (https://github.com/RAFA-gif2003/homologacion_maraton) python-urllib'}
def get(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
LUGARES = json.load(open('poi/lugares.json'))
os.makedirs('mapas/poi', exist_ok=True); out = []
for L in LUGARES:
  r = dict(L)
  try:
      for title in L['wiki']:
          lang, t = title.split(':', 1)
          q = get(f'https://{lang}.wikipedia.org/w/api.php?' + urllib.parse.urlencode(dict(action='query', format='json', redirects=1,
                  titles=t, prop='pageimages|coordinates|pageprops', piprop='original|name')))
          pg = next(iter(q['query']['pages'].values()))
          if 'missing' in pg: continue
          r['pagina'] = f'{lang}:{pg["title"]}'
          if pg.get('coordinates'): r['lat_wiki'], r['lon_wiki'] = pg['coordinates'][0]['lat'], pg['coordinates'][0]['lon']
          if pg.get('pageimage') and not r.get('archivo'): r['archivo'] = pg['pageimage']
          if r.get('archivo'): break
      if r.get('archivo'):
          q = get('https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(dict(action='query', format='json',
                  titles='File:' + r['archivo'], prop='imageinfo', iiprop='url|extmetadata|size', iiurlwidth=1280)))
          pg = next(iter(q['query']['pages'].values())); ii = (pg.get('imageinfo') or [{}])[0]; md = ii.get('extmetadata', {})
          clean = lambda v: html.unescape(re.sub('<[^>]+>', '', (md.get(v) or {}).get('value', ''))).strip()
          r.update(autor=clean('Artist'), licencia=clean('LicenseShortName'), url_lic=clean('LicenseUrl'), url_pag=ii.get('descriptionurl'))
          src = ii.get('thumburl') or ii.get('url')
          if src:
              fn = f"mapas/poi/{L['id']}.jpg"
              open(fn, 'wb').write(urllib.request.urlopen(urllib.request.Request(src, headers=UA), timeout=120).read())
              r['foto'] = fn
      print(L['id'], r.get('pagina'), r.get('archivo'), r.get('licencia'), r.get('lat_wiki'), r.get('lon_wiki'))
  except Exception as ex:
    r["error"] = repr(ex); print("ERROR", L["id"], repr(ex))
  out.append(r)
json.dump(out, open('mapas/poi/lugares_wiki.json', 'w'), ensure_ascii=False, indent=1)
