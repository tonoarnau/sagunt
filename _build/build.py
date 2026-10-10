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
    ("Anníbal · Cròniques de foc — Sagunt, els Alps i Cannes, història recreada amb IA",
     "Aníbal · Crónicas de fuego — Sagunto, los Alpes y Cannas, documental histórico con IA",
     "Hannibal · Chronicles of Fire — Saguntum, the Alps and Cannae, AI history documentary"),
    ("Sèrie documental sobre Anníbal recreada amb IA i basada en Polibi i Titus Livi. Mira el setge de Sagunt (219 aC), la travessa dels Alps amb elefants (218 aC) i la batalla de Cannes (216 aC).",
     "Serie documental sobre Aníbal recreada con IA y basada en Polibio y Tito Livio. Mira el asedio de Sagunto (219 a. C.), el cruce de los Alpes con elefantes (218 a. C.) y la batalla de Cannas (216 a. C.).",
     "AI-recreated documentary series about Hannibal, based on Polybius and Livy. Watch the siege of Saguntum (219 BC), the crossing of the Alps with elephants (218 BC) and the Battle of Cannae (216 BC)."),
    ("Anníbal · Cròniques de foc — La Segona Guerra Púnica, recreada amb IA",
     "Aníbal · Crónicas de fuego — La Segunda Guerra Púnica, recreada con IA",
     "Hannibal · Chronicles of Fire — The Second Punic War, recreated with AI"),
    ("Sèrie documental basada en les fonts antigues. Capítol I: Sagunt. Capítol II: Els Alps. Capítol III: Cannes.",
     "Serie documental basada en las fuentes antiguas. Capítulo I: Sagunto. Capítulo II: Los Alpes. Capítulo III: Cannas.",
     "A documentary series based on the ancient sources. Chapter I: Saguntum. Chapter II: The Alps. Chapter III: Cannae."),
    ('content="Anníbal · Cròniques de foc"', 'content="Aníbal · Crónicas de fuego"', 'content="Hannibal · Chronicles of Fire"'),
    ("Anníbal, amb capa roja i armadura d'escates, davant del camp de Sagunt en flames",
     "Aníbal, con capa roja y armadura de escamas, ante el campo de Sagunto en llamas",
     "Hannibal, in a red cloak and scale armour, before the burning fields of Saguntum"),
    # El projecte
    ("EL PROJECTE", "EL PROYECTO", "THE PROJECT"),
    ("Història documentada, recreada amb IA", "Historia documentada, recreada con IA", "Documented history, recreated with AI"),
    ("Anníbal · Cròniques de foc és una sèrie documental sobre la Segona Guerra Púnica. Cada fet que s'hi conta ix de les fonts antigues; quan les fonts dubten o no coincideixen, la veu ho diu.",
     "Aníbal · Crónicas de fuego es una serie documental sobre la Segunda Guerra Púnica. Cada hecho que se cuenta sale de las fuentes antiguas; cuando las fuentes dudan o no coinciden, la voz lo dice.",
     "Hannibal · Chronicles of Fire is a documentary series about the Second Punic War. Every fact it tells comes from the ancient sources; when the sources are unsure or disagree, the narrator says so."),
    ("FONTS PRIMÀRIES", "FUENTES PRIMARIAS", "PRIMARY SOURCES"),
    ("Polibi i Titus Livi, contrastats frase a frase, amb la cita de cada xifra i de cada episodi dubtós.",
     "Polibio y Tito Livio, contrastados frase a frase, con la cita de cada cifra y de cada episodio dudoso.",
     "Polybius and Livy, checked line by line, with a citation for every figure and every disputed episode."),
    ("RECREACIÓ AMB IA", "RECREACIÓN CON IA", "RECREATED WITH AI"),
    ("Cada pla és una imatge generada amb IA a partir de les fonts i animada com una peça de cinema, amb música orquestral pròpia.",
     "Cada plano es una imagen generada con IA a partir de las fuentes y animada como una pieza de cine, con música orquestal propia.",
     "Every shot is an AI-generated image built from the sources and animated like a piece of cinema, with an original orchestral score."),
    (">IDIOMES<", ">IDIOMAS<", ">LANGUAGES<"),
    ("Narrat en valencià, amb subtítols en castellà i anglés a YouTube.",
     "Narrado en valenciano, con subtítulos en castellano e inglés en YouTube.",
     "Narrated in Valencian, with Spanish and English subtitles on YouTube."),
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
    ("Una ciutat ibera aliada de Roma. Un general cartaginès d'uns vint-i-huit anys. Huit mesos de setge que canviarien el destí del Mediterrani.",
     "Una ciudad íbera aliada de Roma. Un general cartaginés de unos veintiocho años. Ocho meses de asedio que cambiarían el destino del Mediterráneo.",
     "An Iberian city allied with Rome. A Carthaginian general of about twenty-eight. Eight months of siege that would change the fate of the Mediterranean."),
    ("Veure el curt", "Ver el corto", "Watch the film"),
    # Carrusel de l'hero
    ("La columna d'Anníbal puja en fila per un vessant nevat dels Alps, a contrallum, sobre un mar de núvols",
     "La columna de Aníbal sube en fila por una ladera nevada de los Alpes, a contraluz, sobre un mar de nubes",
     "Hannibal's column climbs in single file up a snowy slope of the Alps, against the light, above a sea of clouds"),
    ("Pausar el carrusel", "Pausar el carrusel", "Pause the slideshow"),
    ("Reprendre el carrusel", "Reanudar el carrusel", "Resume the slideshow"),
    ("Capítol I, Sagunt", "Capítulo I, Sagunto", "Chapter I, Saguntum"),
    ("Capítol II, Els Alps", "Capítulo II, Los Alpes", "Chapter II, The Alps"),
    ("Capítol III, Cannes", "Capítulo III, Cannas", "Chapter III, Cannae"),
    ("Anníbal, d'esquena i amb capa granat, contempla la plana de Cannes al capvespre, sembrada d'escuts",
     "Aníbal, de espaldas y con capa granate, contempla la llanura de Cannas al atardecer, sembrada de escudos",
     "Hannibal, seen from behind in a crimson cloak, looks out over the plain of Cannae at sunset, strewn with shields"),
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
    ("ESTRENA · 4 OCT. 2026", "ESTRENO · 4 OCT. 2026", "PREMIERE · 4 OCT 2026"),
    ("ESTRENA · 16 OCT. 2026 · 5:04", "ESTRENO · 16 OCT. 2026 · 5:04", "PREMIERE · 16 OCT 2026 · 5:04"),
    ("Anníbal i la batalla de Cannes", "Aníbal y la batalla de Cannas", "Hannibal and the Battle of Cannae"),
    ("Roma posa en camp huit legions, «una cosa que no s'havia fet mai», segons Polibi. Al vespre, l'exèrcit romà ja no existix.",
     "Roma pone en campaña ocho legiones, «algo que nunca se había hecho», según Polibio. Al anochecer, el ejército romano ya no existe.",
     "Rome puts eight legions in the field, \"a thing which had never been done before\", according to Polybius. By nightfall, the Roman army no longer exists."),
    ("Anníbal assetja la ciutat ibera mentre Roma envia ambaixadors i no exèrcits. Quan Sagunt cau, ja no hi ha volta enrere.",
     "Aníbal asedia la ciudad íbera mientras Roma envía embajadores y no ejércitos. Cuando Sagunto cae, ya no hay vuelta atrás.",
     "Hannibal besieges the Iberian city while Rome sends envoys, not armies. When Saguntum falls, there is no turning back."),
    ("DIRECCIÓ", "DIRECCIÓN", "DIRECTOR"),
    (">IDIOMA<", ">IDIOMA<", ">LANGUAGE<"),
    ("<b>Valencià</b>", "<b>Valenciano</b>", "<b>Valencian</b>"),
    ("JA DISPONIBLE", "YA DISPONIBLE", "OUT NOW"),
    ("PRÒXIMAMENT", "PRÓXIMAMENTE", "COMING SOON"),
    (" · VEURE<", " · VER<", " · WATCH<"),
    ("Més de quaranta-sis mil homes i els seus elefants deixen arrere el Roine. Quinze dies després, a la plana del Po, n'arriben com a molt vint-i-sis mil.",
     "Más de cuarenta y seis mil hombres y sus elefantes dejan atrás el Ródano. Quince días después, a la llanura del Po llegan, como mucho, veintiséis mil.",
     "More than forty-six thousand men and their elephants leave the Rhône behind. Fifteen days later, at most twenty-six thousand reach the plain of the Po."),
    ("Anníbal creua els Alps", "Aníbal cruza los Alpes", "Hannibal Crosses the Alps"),
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
    # Peu i diàlegs
    ('aria-label="Xarxes"', 'aria-label="Redes"', 'aria-label="Social"'),
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


def h1(word, tag="h1"):
    spans = "".join(
        f'<span class="letter" aria-hidden="true" style="animation-delay:{0.55 + i * 0.04:.2f}s">{"&nbsp;" if c == " " else c}</span>'
        for i, c in enumerate(word))
    cls = "" if tag == "h1" else ' class="htitle"'  # la segona diapositiva: mateix aspecte, però un sol <h1> a la pàgina
    return f'<{tag}{cls} aria-label="{word}" style="--chars:{len(word)}">{spans}</{tag}>'


# títol gran de la segona diapositiva del carrusel
ALPS = {"ca": "Els Alps", "es": "Los Alpes", "en": "The Alps"}
CANNES = {"ca": "Cannes", "es": "Cannas", "en": "Cannae"}


# Dades estructurades (schema.org): productora, sèrie i un VideoObject per capítol publicat
CANAL = "https://www.youtube.com/@historiasdeltiopipa"
SERIE = {"ca": "Anníbal · Cròniques de foc", "es": "Aníbal · Crónicas de fuego", "en": "Hannibal · Chronicles of Fire"}
DESC_SERIE = {
    "ca": "Sèrie documental sobre Anníbal i la Segona Guerra Púnica, recreada amb IA a partir de Polibi i Titus Livi. Narrada en valencià.",
    "es": "Serie documental sobre Aníbal y la Segunda Guerra Púnica, recreada con IA a partir de Polibio y Tito Livio. Narrada en valenciano, con subtítulos en castellano.",
    "en": "Documentary series about Hannibal and the Second Punic War, recreated with AI from Polybius and Livy. Narrated in Valencian, with English subtitles."}
VIDEOS = [  # id de YouTube, durada ISO, data de publicació, títol i descripció per idioma
    ("1vzNUB1k7_s", "PT4M39S", "2026-10-04T06:43:04-07:00", 1,
     {"ca": ("Anníbal assetja Sagunt (219 aC)", "Capítol I. Anníbal assetja la ciutat ibera de Sagunt, aliada de Roma, mentre Roma envia ambaixadors i no exèrcits. Quan Sagunt cau, comença la Segona Guerra Púnica."),
      "es": ("Aníbal asedia Sagunto (219 a. C.)", "Capítulo I. Aníbal asedia la ciudad íbera de Sagunto, aliada de Roma, mientras Roma envía embajadores y no ejércitos. Cuando Sagunto cae, empieza la Segunda Guerra Púnica."),
      "en": ("Hannibal besieges Saguntum (219 BC)", "Chapter I. Hannibal besieges the Iberian city of Saguntum, an ally of Rome, while Rome sends envoys, not armies. When Saguntum falls, the Second Punic War begins.")}),
    ("qEE7YH02s3s", "PT6M36S", "2026-10-04T06:43:29-07:00", 2,
     {"ca": ("Anníbal creua els Alps (218 aC)", "Capítol II. Més de quaranta-sis mil homes i els seus elefants deixen arrere el Roine. Quinze dies després, a la plana del Po, n'arriben com a molt vint-i-sis mil."),
      "es": ("Aníbal cruza los Alpes (218 a. C.)", "Capítulo II. Más de cuarenta y seis mil hombres y sus elefantes dejan atrás el Ródano. Quince días después, a la llanura del Po llegan, como mucho, veintiséis mil."),
      "en": ("Hannibal crosses the Alps (218 BC)", "Chapter II. More than forty-six thousand men and their elephants leave the Rhône behind. Fifteen days later, at most twenty-six thousand reach the plain of the Po.")}),
    ("EZ8KpRyL_sM", "PT5M4S", "2026-10-16", 3,
     {"ca": ("Anníbal i la batalla de Cannes (216 aC)", "Capítol III. A la plana de Cannes, Roma posa en camp huit legions, «una cosa que no s'havia fet mai», segons Polibi. Davant, uns cinquanta mil homes d'Anníbal. Al vespre, l'exèrcit romà ja no existix."),
      "es": ("Aníbal y la batalla de Cannas (216 a. C.)", "Capítulo III. En la llanura de Cannas, Roma pone en campaña ocho legiones, «algo que nunca se había hecho», según Polibio. Enfrente, unos cincuenta mil hombres de Aníbal. Al anochecer, el ejército romano ya no existe."),
      "en": ("Hannibal and the Battle of Cannae (216 BC)", "Chapter III. On the plain of Cannae, Rome puts eight legions in the field, \"a thing which had never been done before\", according to Polybius. Facing them, some fifty thousand of Hannibal's men. By nightfall, the Roman army no longer exists.")}),
]


def ld(lang, url):
    import json
    org = {"@type": "Organization", "@id": BASE_URL + "#productora", "name": "Historias del tío Pipa", "url": CANAL,
           "logo": BASE_URL + "img/og.jpg",
           "sameAs": [CANAL, "https://www.instagram.com/historiasdeltiopipa"]}
    serie = {"@type": "CreativeWorkSeries", "@id": BASE_URL + "#serie", "name": SERIE[lang], "description": DESC_SERIE[lang],
             "url": url, "inLanguage": "ca", "genre": ["Documental", "Història"] if lang != "en" else ["Documentary", "History"],
             # La guerra va com a Thing i no com a Event: Google valida qualsevol Event com un esdeveniment
             # amb entrades (startDate, location, offers...) i Search Console ho marcava com a error.
             "about": [{"@type": "Person", "name": {"ca": "Anníbal", "es": "Aníbal", "en": "Hannibal"}[lang],
                        "sameAs": "https://en.wikipedia.org/wiki/Hannibal"},
                       {"@type": "Thing", "name": {"ca": "Segona Guerra Púnica", "es": "Segunda Guerra Púnica", "en": "Second Punic War"}[lang],
                        "sameAs": "https://en.wikipedia.org/wiki/Second_Punic_War"}],
             "creator": {"@id": BASE_URL + "#productora"}, "image": BASE_URL + "img/og.jpg"}
    videos = []
    for vid, dur, data, n, txt in VIDEOS:
        nom, desc = txt[lang]
        videos.append({"@type": "VideoObject", "@id": f"{BASE_URL}#capitol-{n}", "name": f"{nom} · {SERIE[lang]}", "description": desc,
                       "thumbnailUrl": [f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg"], "uploadDate": data, "duration": dur,
                       "contentUrl": f"https://www.youtube.com/watch?v={vid}", "embedUrl": f"https://www.youtube.com/embed/{vid}",
                       "inLanguage": "ca", "isPartOf": {"@id": BASE_URL + "#serie"}, "publisher": {"@id": BASE_URL + "#productora"},
                       "position": n})
    pagina = {"@type": "WebPage", "@id": url, "url": url, "name": SERIE[lang], "description": DESC_SERIE[lang], "inLanguage": LANGS[lang][1],
              "isPartOf": {"@type": "WebSite", "@id": BASE_URL + "#web", "url": BASE_URL, "name": SERIE[lang]},
              "about": {"@id": BASE_URL + "#serie"}, "primaryImageOfPage": BASE_URL + "img/og.jpg",
              "video": [{"@id": v["@id"]} for v in videos]}
    data = {"@context": "https://schema.org", "@graph": [pagina, org, serie] + videos}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "</script>"


def sitemap():
    """Una URL per idioma, amb hreflang, data de l'última modificació (la del build) i els vídeos publicats en extensió de
    vídeo de Google (miniatura, títol, descripció, reproductor, durada i data) en l'idioma de cada pàgina."""
    import datetime, html, re as _re
    avui = datetime.date.today().isoformat()
    alts = "".join(f'<xhtml:link rel="alternate" hreflang="{LANGS[o][1]}" href="{BASE_URL}{LANGS[o][0]}"/>' for o in LANGS)
    alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{BASE_URL}"/>'

    def segons(iso):
        m = _re.match(r"PT(?:(\d+)M)?(?:(\d+)S)?", iso)
        return int(m.group(1) or 0) * 60 + int(m.group(2) or 0)

    def videos(lang):
        out = ""
        for vid, dur, data, n, txt in VIDEOS:
            nom, desc = (html.escape(x) for x in txt[lang])
            out += (f"<video:video><video:thumbnail_loc>https://i.ytimg.com/vi/{vid}/maxresdefault.jpg</video:thumbnail_loc>"
                    f"<video:title>{nom}</video:title><video:description>{desc}</video:description>"
                    f"<video:player_loc>https://www.youtube.com/embed/{vid}</video:player_loc>"
                    f"<video:duration>{segons(dur)}</video:duration><video:publication_date>{data}</video:publication_date>"
                    f"<video:family_friendly>yes</video:family_friendly></video:video>")
        return out

    urls = "".join(f"<url><loc>{BASE_URL}{LANGS[l][0]}</loc><lastmod>{avui}</lastmod>{alts}{videos(l)}</url>" for l in LANGS)
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                                      'xmlns:xhtml="http://www.w3.org/1999/xhtml" '
                                      f'xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">{urls}</urlset>\n', encoding="utf-8")
    print("✓ sitemap.xml")


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
    head += [f'<link rel="canonical" href="{BASE_URL}{d}">', f'<meta property="og:url" content="{BASE_URL}{d}">']
    s = s.replace("<!--I18N_HEAD-->", "\n".join(head), 1)
    s = s.replace("<!--I18N_LD-->", ld(lang, BASE_URL + d), 1)

    current = ' aria-current="page"'
    links = "".join(
        f'<a href="{rel(lang, o)}" hreflang="{LANGS[o][1]}" lang="{LANGS[o][1]}" data-lang="{o}" '
        f'aria-label="{LANGS[o][4]}"{current if o == lang else ""}>{LANGS[o][3]}</a>'
        for o in LANGS)
    s = s.replace("<!--I18N_SWITCH-->", f'      <nav class="lang" aria-label="Idioma · Language">{links}</nav>', 1)
    s = s.replace("<!--I18N_H1-->", h1(word), 1)
    s = s.replace("<!--I18N_H1_ALPS-->", h1(ALPS[lang], "p"), 1)
    s = s.replace("<!--I18N_H1_C3-->", h1(CANNES[lang], "p"), 1)

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
        leftovers = [w for w in ("setge", "Sagunt ", "curts", "capítol", "Anníbal", "Tancar") if w in visible]
        assert not leftovers, (lang, leftovers)
    out = ROOT / d / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(s, encoding="utf-8")
    print(f"✓ {lang} → {out.relative_to(ROOT)}")


if __name__ == "__main__":
    for l in LANGS:
        build(l)
    sitemap()
