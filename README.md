# AB-Tech — förslag på ny statisk hemsida

Det här är ett förslag på en ny sajt som kan ersätta [ab-tech.se](https://www.ab-tech.se/), som idag ligger hos Mozello för cirka 900 kr/år. Innehåll, språk (engelska) och uttryck följer den nuvarande sajten, men layouten är renare, modernare och anpassad för mobil.

**Det här är bara ett förslag.** Inget är publicerat. Mozello, domänen, DNS och konton är orörda. Formuläret är förberett men har ingen riktig nyckel än.

När sajten väl ligger hos till exempel GitHub Pages, Cloudflare Pages eller Netlify blir själva hostingen gratis. Kvar att betala är i praktiken bara .se-domänen, typ 100–200 kr per år beroende på registrar.

Mejl på **bladelius.com** (bland annat ab-tech@bladelius.com) påverkas inte av flytten. Den adressen ligger inte hos Mozello.

## Sidor

Samma sidor som idag, med samma webbadresser:

| Sida | Fil |
| --- | --- |
| Startsida | `index.html` |
| Products | `products/index.html` |
| STILL | `still/index.html` |
| REN | `ren/index.html` |
| KLAR | `klar/index.html` |
| FRID | `frid/index.html` |
| TAMP | `tamp/index.html` |
| About Us | `about-us/index.html` |
| News | `news/index.html` |
| Contact | `contact/index.html` |
| Sister brands (Bladelius och Norse Audio) | `bladelius/index.html` |
| Reviews | `reviews/index.html` |

Gemensam formgivning ligger i `css/style.css`. Lite JavaScript för mobilmenyn, bildgalleriet och kontaktformuläret ligger i `js/main.js`. Logotyp, produktbilder, nyhetsbilder och recensionsbilder ligger i `images/`.

Startsidan har samma stora foto som idag. Under bilden ligger ett rullande urval av senaste nyheter och recensioner, ett stillsamt bildspel med produkter (länk till Products) och en kort hänvisning till Instagram och Facebook. Själva produktlistan ligger på Products-sidan. Längst ned på Products, och på sidan Sister brands (`bladelius/`), finns Bladelius och Norse Audio. På Products-sidan är TAMP klickbar, vilket den inte var på Mozello-sajten. Alla 33 nyheter visas direkt, utan Mozellos “Load more”.

## Hur du redigerar texter och bilder

Du kan öppna respektive HTML-fil i en vanlig textredigerare och ändra rubriker, brödtext och specifikationslistor. Strukturen är densamma på produktsidorna: vänster kolumn är texten, höger kolumn är bilden och specifikationen, längst ner ligger eventuellt galleri.

Byter du ut en bild: lägg den nya filen i samma mapp med samma filnamn (till exempel `images/products/still.jpg`), eller lägg en ny fil där och uppdatera `src` i HTML:en. Helst JPEG eller WebP, max cirka 2000 pixlar bred, så att sidan fortsätter ladda snabbt.

Vill du lägga till en nyhet: kopiera ett befintligt `<article class="news-item">` i `news/index.html` och ändra rubrik, datum, text och bild.

Menyn och sidfoten är inskrivna på varje sida. Ändrar du en länk i menyn behöver samma ändring göras på alla sidor. Alternativt kan du köra `python3 build.py` efter att ha uppdaterat mallen i den filen (det skriver om HTML-filerna).

Typsnittet är **Lato** (samma som idag). Färgerna är svart bakgrund `#000000` / `#0c0c0c`, ljus text `#e6e6e6` och `#d8d8d8`.

## Kontaktformuläret

Formuläret på Contact skickar till **ab-tech@bladelius.com**, precis som idag, men via [Web3Forms](https://web3forms.com) (gratis för den här volymen). I `contact/index.html` finns en tydligt markerad platshållare:

```html
<input type="hidden" name="access_key" value="YOUR_WEB3FORMS_ACCESS_KEY">
```

Byt ut `YOUR_WEB3FORMS_ACCESS_KEY` mot en riktig nyckel innan sajten går live. Skapa nyckeln på web3forms.com och ange ab-tech@bladelius.com som mottagare. Tills dess visar formuläret ett felmeddelande i stället för att skicka något.

Vill du hellre använda [Formspree](https://formspree.io): ändra formulärets `action` till `https://formspree.io/f/DIN_FORM_ID` och ta bort fältet `access_key`.

Lägg inte en riktig nyckel i ett publikt git-repo om du kan undvika det. De flesta hostar låter dig sätta värdet vid publicering.

## Så tittar du på förslaget lokalt

I den här mappen:

```bash
python3 -m http.server 8080
```

Öppna sedan http://localhost:8080 i webbläsaren.

## När ni vill gå live (inget av detta är gjort nu)

Gör det i den här ordningen, så att ab-tech.se aldrig ligger nere.

### 1. Välj gratis hosting

Alla tre här nedan funkar för den här sajten (ren HTML/CSS, lite JS):

- **Cloudflare Pages** — smidigt om ni ändå ska ha DNS eller domänen hos Cloudflare.
- **Netlify** — enkelt att dra in mappen och få HTTPS.
- **GitHub Pages** — lägg filerna i ett repo och slå på Pages. Filen `.nojekyll` finns redan så att GitHub inte kör Jekyll på mappen.

Skapa ett konto, ladda upp innehållet i den här mappen och kontrollera att sidan ser rätt ut på den tillfälliga adressen ni får (typ `något.pages.dev`).

### 2. Koppla formulärnyckeln

Skapa nyckeln som beskrivs ovan, klistra in den (eller sätt den vid deploy) och skicka ett testmeddelande. Kolla att det kommer fram till ab-tech@bladelius.com.

### 3. Flytta .se-domänen från Mozello

Domänen ab-tech.se ligger idag hos Mozello. För att ta över den:

1. Be Mozello om en **auth-kod / överföringskod** (EPP) för ab-tech.se. Det görs i deras kontrollpanel eller via support.
2. Välj en registrar, till exempel **Loopia** eller **Cloudflare Registrar**, och starta en domänflytt med koden. En .se-flytt tar oftast ett par dagar.
3. När domänen är flyttad pekar ni DNS mot den nya hosten enligt deras instruktioner (vanligtvis ett CNAME för `www` och antingen ett CNAME/ALIAS eller A-poster för roten `ab-tech.se`). Aktivera HTTPS (det sköts automatiskt hos Pages/Netlify/Cloudflare).
4. Se till att både `ab-tech.se` och `www.ab-tech.se` fungerar, och att den ena omdirigerar till den andra.

Rör inte Mozello-DNS förrän den nya sajten är uppladdad och testad på den tillfälliga adressen.

### robots.txt och sitemap (vid publicering)

Filen `sitemap.xml` ligger redan i roten, med absoluta adresser på https://ab-tech.se/. `robots.txt` blockerar fortfarande sökmotorer med `Disallow: /` så länge sajten bara är en förhandsvisning. Sitemap-raden finns redan:

```
Sitemap: https://ab-tech.se/sitemap.xml
```

När sajten går live, ändra `robots.txt` till:

```
User-agent: *
Allow: /

Sitemap: https://ab-tech.se/sitemap.xml
```

Lägg därefter till sajten i Google Search Console och skicka in `https://ab-tech.se/sitemap.xml`.

### 4. Säg upp Mozello först när den nya sajten är live

När https://ab-tech.se (och www) visar den nya sajten, formuläret fungerar och ni har klickat igenom sidorna: säg upp Mozello-abonnemanget så att ni inte betalar dubbelt. Säg inte upp det tidigare, för då kan både den gamla sajten och domänen påverkas.

### 5. Mejl

Mejl på bladelius.com, inklusive ab-tech@bladelius.com, påverkas inte. Den här flytten gäller bara webbplatsen och domänen ab-tech.se.

## Skärmbilder

Jämförelser mellan nuvarande sajt och förslaget ligger i `screens/`.

## Vad som inte följde med

- Mozellos “Load more” på News (alla 33 inlägg ligger nu på samma sida).
- Egna permanenta adresser för varje nyhetsinlägg (`/news/params/post/...`). Innehållet finns på `/news/`.
- Google Analytics.
- Eventuell cookie-ruta från Mozello.
- Språkväxlaren i Mozello-mallen; sajten är enbart på engelska, precis som innehållet idag.
