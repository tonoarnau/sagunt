#!/usr/bin/env python3
"""
Genera la landing en tres idiomes a partir de _build/template.html (valencià):

    index.html      → valencià (idioma per defecte)
    es/index.html   → castellano
    en/index.html   → English

Ús:  python3 _build/build.py
Per a canviar un text: edita'l al template (valencià) i a la taula TR de baix.
"""
import re
from pathlib import Path

# ⚠️ Canvia-ho per l'adreça real quan publiques a GitHub Pages (acaba en /)
BASE_URL = "https://tonoarnau.github.io/sagunt/"

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = (ROOT / "_build" / "template.html").read_text(encoding="utf-8")

LANGS = {
    #       dir   html  og_locale  label   nom natiu     títol h1
    "ca": ("",    "ca", "ca_ES",   "VAL",  "Valencià",   "Sagunt"),
    "es": ("es/", "es", "es_ES",   "ES",   "Castellano", "Sagunto"),
    "en": ("en/", "en", "en_GB",   "EN",   "English",    "Saguntum"),
}

# (valencià, castellano, English) — els textos més llargs s'apliquen primer
TR = [
    # <head>
    ("Sagunt, 219 aC · Anníbal — Cròniques de foc",
     "Sagunto, 219 a. C. · Aníbal — Crónicas de fuego",
     "Saguntum, 219 BC · Hannibal — Chronicles of Fire"),
    ("Curts cinematogràfics sobre Anníbal i la Segona Guerra Púnica. Capítol I: Sagunt, el setge que va encendre una guerra.",
     "Cortometrajes cinematográficos sobre Aníbal y la Segunda Guerra Púnica. Capítulo I: Sagunto, el asedio que encendió una guerra.",
     "Cinematic short films about Hannibal and the Second Punic War. Chapter I: Saguntum, the siege that ignited a war."),
    ("Sagunt, 219 aC — El setge que va encendre una guerra",
     "Sagunto, 219 a. C. — El asedio que encendió una guerra",
     "Saguntum, 219 BC — The siege that ignited a war"),
    ("Curts cinematogràfics sobre Anníbal i la Segona Guerra Púnica.",
     "Cortometrajes cinematográficos sobre Aníbal y la Segunda Guerra Púnica.",
     "Cinematic short films about Hannibal and the Second Punic War."),
    ("Anníbal, amb capa roja i armadura d'escates, davant del camp de Sagunt en flames",
     "Aníbal, con capa roja y armadura de escamas, ante el campo de Sagunto en llamas",
     "Hannibal, in a red cloak and scale armour, before the burning fields of Saguntum"),
    # Navegació
    ('aria-label="Principal"', 'aria-label="Principal"', 'aria-label="Main"'),
    (">Els curts<", ">Los cortos<", ">The films<"),
    (">Fotogrames<", ">Fotogramas<", ">Stills<"),
    (">El setge<", ">El asedio<", ">The siege<"),
    (">Cronologia<", ">Cronología<", ">Timeline<"),
    (">Estrena<", ">Estreno<", ">Premiere<"),
    ("Tràiler", "Tráiler", "Trailer"),
    ("CRÒNIQUES DE FOC", "CRÓNICAS DE FUEGO", "CHRONICLES OF FIRE"),
    # Hero
    ("El setge que va encendre una guerra", "El asedio que encendió una guerra", "The siege that ignited a war"),
    ("Una ciutat ibera aliada de Roma. Un general cartaginès d'uns vint-i-huit anys. Vuit mesos de setge que canviarien el destí del Mediterrani.",
     "Una ciudad íbera aliada de Roma. Un general cartaginés de unos veintiocho años. Ocho meses de asedio que cambiarían el destino del Mediterráneo.",
     "An Iberian city allied with Rome. A Carthaginian general of about twenty-eight. Eight months of siege that would change the fate of the Mediterranean."),
    ("Veure el curt", "Ver el corto", "Watch the film"),
    ("Tots els capítols", "Todos los capítulos", "All chapters"),
    ("VAL · SUBT. ES/EN", "V.O. VALENCIANO · SUBT. ES/EN", "VALENCIAN · ES/EN SUBS"),
    ("Baixar als curts", "Bajar a los cortos", "Scroll to the films"),
    # Cinta
    ("Els Alps", "Los Alpes", "The Alps"),
    ("Trasimè", "Trasimeno", "Trasimene"),
    (">Cannes<", ">Cannas<", ">Cannae<"),
    # Els curts
    ("LA SÈRIE · 4 CAPÍTOLS", "LA SERIE · 4 CAPÍTULOS", "THE SERIES · 4 CHAPTERS"),
    ("Curts cinematogràfics", "Cortometrajes cinematográficos", "Cinematic short films"),
    ("Cada capítol, un moment decisiu de la Segona Guerra Púnica, rodat com una peça de cinema breu.",
     "Cada capítulo, un momento decisivo de la Segunda Guerra Púnica, rodado como una pieza de cine breve.",
     "Each chapter, a defining moment of the Second Punic War, shot as a short piece of cinema."),
    ("Reproduir Capítol I, Sagunt", "Reproducir capítulo I, Sagunto", "Play chapter I, Saguntum"),
    ("Reproduir capítol II, Els Alps", "Reproducir capítulo II, Los Alpes", "Play chapter II, The Alps"),
    ("Reproduir capítol III, Cannes", "Reproducir capítulo III, Cannas", "Play chapter III, Cannae"),
    ("Reproduir capítol IV, Zama", "Reproducir capítulo IV, Zama", "Play chapter IV, Zama"),
    ("[VÍDEO 16:9 · PLACEHOLDER]", "[VÍDEO 16:9 · PLACEHOLDER]", "[VIDEO 16:9 · PLACEHOLDER]"),
    ("ESTRENA · [DATA]", "ESTRENO · [FECHA]", "PREMIERE · [DATE]"),
    ("Anníbal assetja la ciutat ibera mentre Roma envia ambaixadors i no exèrcits. Quan Sagunt cau, ja no hi ha volta enrere.",
     "Aníbal asedia la ciudad íbera mientras Roma envía embajadores y no ejércitos. Cuando Sagunto cae, ya no hay vuelta atrás.",
     "Hannibal besieges the Iberian city while Rome sends envoys, not armies. When Saguntum falls, there is no turning back."),
    ("DIRECCIÓ", "DIRECCIÓN", "DIRECTOR"),
    ("[NOM]", "[NOMBRE]", "[NAME]"),
    (">IDIOMA<", ">IDIOMA<", ">LANGUAGE<"),
    ("<b>Valencià</b>", "<b>Valenciano</b>", "<b>Valencian</b>"),
    ("PRÒXIMAMENT", "PRÓXIMAMENTE", "COMING SOON"),
    ("Elefants, neu i un exèrcit sencer creuant l'impossible cap a Itàlia.",
     "Elefantes, nieve y un ejército entero cruzando lo imposible hacia Italia.",
     "Elephants, snow and an entire army crossing the impossible into Italy."),
    ("L'encerclament perfecte i la pitjor derrota de la història de Roma.",
     "El cerco perfecto y la peor derrota de la historia de Roma.",
     "The perfect encirclement and the worst defeat in Rome’s history."),
    ("Anys després, a l'Àfrica, Escipió espera Anníbal per a l'últim acte.",
     "Años después, en África, Escipión espera a Aníbal para el último acto.",
     "Years later, in Africa, Scipio awaits Hannibal for the final act."),
    # Fotogrames
    ("FOTOGRAMES · CAPÍTOL I", "FOTOGRAMAS · CAPÍTULO I", "STILLS · CHAPTER I"),
    ("Dins del setge", "Dentro del asedio", "Inside the siege"),
    ("Cinc moments del curt. Toca una imatge per a veure-la a pantalla completa.",
     "Cinco momentos del corto. Toca una imagen para verla a pantalla completa.",
     "Five moments from the film. Tap an image to view it full screen."),
    ("Ampliar fotograma", "Ampliar fotograma", "Enlarge still"),
    ("Les torres de setge", "Las torres de asedio", "The siege towers"),
    ("La muralla cedeix", "La muralla cede", "The wall gives way"),
    ("L'assalt", "El asalto", "The assault"),
    ("El consell", "El consejo", "The council"),
    ("L'ordre", "La orden", "The order"),
    ("'FOTOGRAMA ", "'FOTOGRAMA ", "'STILL "),
    # Context històric
    ("CONTEXT HISTÒRIC", "CONTEXTO HISTÓRICO", "HISTORICAL CONTEXT"),
    ("Sagunt no era la guerra.", "Sagunto no era la guerra.", "Saguntum was not the war."),
    ("Era l'espurna.", "Era la chispa.", "It was the spark."),
    ("La seua caiguda va donar a Roma el motiu per declarar la Segona Guerra Púnica.",
     "Su caída dio a Roma el motivo para declarar la Segunda Guerra Púnica.",
     "Its fall gave Rome the reason to declare the Second Punic War."),
    ("Ampliar el mapa d'Hispània el 219 aC", "Ampliar el mapa de Hispania en el 219 a. C.", "Enlarge the map of Hispania in 219 BC"),
    ("Sagunt quedava al sud de l'Ebre, dins la zona d'influència cartaginesa, però era aliada de Roma. Atacar-la era desafiar Roma.",
     "Sagunto quedaba al sur del Ebro, dentro de la zona de influencia cartaginesa, pero era aliada de Roma. Atacarla era desafiar a Roma.",
     "Saguntum lay south of the Ebro, inside the Carthaginian sphere of influence, yet it was allied with Rome. To attack it was to defy Rome."),
    ("MESOS DE SETGE", "MESES DE ASEDIO", "MONTHS OF SIEGE"),
    ("La ciutat va resistir des de la primavera fins a finals del 219 aC sense rebre ajuda de Roma.",
     "La ciudad resistió desde la primavera hasta finales del 219 a. C. sin recibir ayuda de Roma.",
     "The city held out from spring until late 219 BC without any help from Rome."),
    ("ANYS D'ANNÍBAL", "AÑOS TENÍA ANÍBAL", "HANNIBAL’S AGE"),
    ("Nascut cap al 247 aC, feia només dos anys que comandava l'exèrcit cartaginès a Hispània quan va plantar el setge.",
     "Nacido hacia el 247 a. C., llevaba solo dos años al mando del ejército cartaginés en Hispania cuando inició el asedio.",
     "Born around 247 BC, he had commanded the Carthaginian army in Hispania for only two years when he laid siege."),
    ("ANYS DE GUERRA", "AÑOS DE GUERRA", "YEARS OF WAR"),
    ("De Sagunt a Zama: el conflicte que va decidir qui dominaria el Mediterrani occidental.",
     "De Sagunto a Zama: el conflicto que decidió quién dominaría el Mediterráneo occidental.",
     "From Saguntum to Zama: the conflict that decided who would rule the western Mediterranean."),
    # Cronologia
    ("Cronologia de la saga", "Cronología de la saga", "Timeline of the saga"),
    ("Setge de Sagunt", "Asedio de Sagunto", "Siege of Saguntum"),
    ("Travessa dels Alps", "Travesía de los Alpes", "Crossing the Alps"),
    ("Batalla de Cannes", "Batalla de Cannas", "Battle of Cannae"),
    ("Batalla de Zama", "Batalla de Zama", "Battle of Zama"),
    # Avisos
    ("Que no et pille el foc desprevingut.", "Que el fuego no te pille desprevenido.", "Don’t let the fire catch you off guard."),
    ("T'avisem quan s'estrene cada capítol. Cap correu més.",
     "Te avisamos cuando se estrene cada capítulo. Ningún correo más.",
     "We’ll let you know when each chapter premieres. Nothing else."),
    ("Correu electrònic", "Correo electrónico", "Email address"),
    ("el-teu@correu.cat", "tu@correo.es", "you@email.com"),
    ("Avisa'm", "Avísame", "Notify me"),
    ("Fet. Et direm quan caiga Sagunt.", "Hecho. Te avisaremos cuando caiga Sagunto.", "Done. We’ll tell you when Saguntum falls."),
    # Peu i diàlegs
    ('aria-label="Xarxes"', 'aria-label="Redes"', 'aria-label="Social"'),
    ("[CONTACTE]", "[CONTACTO]", "[CONTACT]"),
    ("[PRODUCTORA]", "[PRODUCTORA]", "[PRODUCTION COMPANY]"),
    ('aria-label="Tancar"', 'aria-label="Cerrar"', 'aria-label="Close"'),
    ("[INSERIR VÍDEO]", "[INSERTAR VÍDEO]", "[INSERT VIDEO]"),
    ("Placeholder del reproductor 16:9", "Placeholder del reproductor 16:9", "16:9 player placeholder"),
    ("Fotograma anterior", "Fotograma anterior", "Previous still"),
    ("Fotograma següent", "Fotograma siguiente", "Next still"),
]

# Substitucions genèriques (s'apliquen després de la taula)
GENERIC = {
    "es": [(r"\[TÍTOL DEL CAPÍTOL ([IV]+)\]", r"[TÍTULO DEL CAPÍTULO \1]"),
           (r"(\d{3}) aC", r"\1 a. C."), (r"CAPÍTOL", "CAPÍTULO"), (r"DURADA", "DURACIÓN"),
           (r"ELS ALPS", "LOS ALPES"), (r"CANNES", "CANNAS"), (r"SAGUNT(?!O|UM)", "SAGUNTO"),
           (r"Sagunt(?!o|um)", "Sagunto"), (r"ANNÍBAL", "ANÍBAL"), (r"Anníbal", "Aníbal"), (r"Hispània", "Hispania")],
    "en": [(r"\[TÍTOL DEL CAPÍTOL ([IV]+)\]", r"[CHAPTER \1 TITLE]"),
           (r"(\d{3}) aC", r"\1 BC"), (r"CAPÍTOL", "CHAPTER"), (r"DURADA", "RUNTIME"),
           (r"ELS ALPS", "THE ALPS"), (r"CANNES", "CANNAE"), (r"SAGUNT(?!O|UM)", "SAGUNTUM"),
           (r"Sagunt(?!o|um)", "Saguntum"), (r"ANNÍBAL", "HANNIBAL"), (r"Anníbal", "Hannibal"), (r"Hispània", "Hispania")],
}

# Suggeriment d'idioma (una sola vegada, no redirigeix: millor per a SEO i per a l'usuari)
TIP = {
    "ca": ("Aquesta pàgina també està en valencià", "Valencià"),
    "es": ("Esta página también está en castellano", "Castellano"),
    "en": ("This page is also available in English", "English"),
}


def rel(frm, to):
    """Enllaç relatiu entre versions (funciona en qualsevol subcarpeta de GitHub Pages)."""
    up = "../" if LANGS[frm][0] else ""
    return (up + LANGS[to][0]) or "./"


def h1(word):
    spans = "".join(
        f'<span class="letter" aria-hidden="true" style="animation-delay:{0.55 + i * 0.04:.2f}s">{c}</span>'
        for i, c in enumerate(word))
    return f'<h1 aria-label="{word}" style="--chars:{len(word)}">{spans}</h1>'


def build(lang):
    d, html_lang, locale, _, _, word = LANGS[lang]
    s = TEMPLATE
    if lang != "ca":
        col = 1 if lang == "es" else 2
        for row in sorted(TR, key=lambda r: -len(r[0])):
            s = s.replace(row[0], row[col])
        for pat, rep in GENERIC[lang]:
            s = re.sub(pat, rep, s)
        s = re.sub(r'(?<![\w/.])img/', '../img/', s)  # rutes a les imatges des de la subcarpeta
    s = s.replace('<html lang="ca">', f'<html lang="{html_lang}">', 1)

    head = [f'<meta property="og:locale" content="{locale}">']
    head += [f'<meta property="og:locale:alternate" content="{LANGS[o][2]}">' for o in LANGS if o != lang]
    head += [f'<link rel="alternate" hreflang="{LANGS[o][1]}" href="{BASE_URL}{LANGS[o][0]}">' for o in LANGS]
    head.append(f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}">')
    s = s.replace("<!--I18N_HEAD-->", "\n".join(head), 1)

    current = ' aria-current="page"'
    links = "".join(
        f'<a href="{rel(lang, o)}" hreflang="{LANGS[o][1]}" lang="{LANGS[o][1]}" data-lang="{o}" '
        f'aria-label="{LANGS[o][4]}"{current if o == lang else ""}>{LANGS[o][3]}</a>'
        for o in LANGS)
    s = s.replace("<!--I18N_SWITCH-->", f'      <nav class="lang" aria-label="Idioma · Language">{links}</nav>', 1)
    s = s.replace("<!--I18N_H1-->", h1(word), 1)

    tips = {o: {"msg": TIP[o][0], "cta": TIP[o][1], "href": rel(lang, o)} for o in LANGS if o != lang}
    script = f"""/* Idioma: recorda l'elecció i suggereix (sense redirigir) la versió del navegador */
(() => {{
  const PAGE = '{lang}', TIPS = {tips!r};
  const get = () => {{ try {{ return localStorage.getItem('lang'); }} catch (e) {{ return null; }} }};
  const set = (v) => {{ try {{ localStorage.setItem('lang', v); }} catch (e) {{}} }};
  document.querySelectorAll('.lang a').forEach(a => a.addEventListener('click', () => set(a.dataset.lang)));
  if (get()) return;
  const pref = (navigator.languages || [navigator.language || '']).map(l => l.toLowerCase().slice(0, 2));
  const want = pref.find(l => l === 'ca' || l === 'es' || l === 'en') || 'en';
  if (want === PAGE || !TIPS[want]) return;
  const t = TIPS[want];
  const el = document.createElement('div');
  el.className = 'langtip glass'; el.setAttribute('role', 'status'); el.lang = want;
  el.innerHTML = `<span></span><a></a><button type="button" aria-label="×"><svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 3 L13 13 M13 3 L3 13" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></button>`;
  el.querySelector('span').textContent = t.msg;
  const a = el.querySelector('a'); a.textContent = t.cta; a.href = t.href; a.hreflang = want;
  a.addEventListener('click', () => set(want));
  el.querySelector('button').addEventListener('click', () => {{ set(PAGE); el.remove(); }});
  setTimeout(() => document.body.appendChild(el), 2500);
}})();
"""
    s = s.replace("<!--I18N_SCRIPT-->", script, 1)

    # comprovació: no han de quedar marcadors ni restes òbvies en valencià
    assert "<!--I18N_" not in s
    if lang != "ca":
        visible = re.sub(r"/\*.*?\*/|//[^\n]*|s-setge|#setge|#curts|id=\"setge\"|id=\"curts\"|class=\"setge|\.setge\{", "", s, flags=re.S)
        leftovers = [w for w in ("setge", "Sagunt ", "curts", "capítol", "Anníbal", "Avisa'm", "Tancar") if w in visible]
        assert not leftovers, (lang, leftovers)
    out = ROOT / d / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(s, encoding="utf-8")
    print(f"✓ {lang} → {out.relative_to(ROOT)}")


if __name__ == "__main__":
    for l in LANGS:
        build(l)
