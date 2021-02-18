<h1 class="code-line" data-line-start=0 data-line-end=1 ><a id="Ray_tracer_0"></a>Ray tracer</h1>
<p class="has-line-data" data-line-start="2" data-line-end="3">Ray tracer je program napisan v Python 3, ki omogoča risanje krogel, valjev, ravnin in stožcev v prostoru na realističen način z uporabo Blinn-Phong modela in lomnega zakona. Dodan je tudi preprost uporabniški vmesnik v Pygame-u, ki omogoča:</p>
<ul>
<li class="has-line-data" data-line-start="3" data-line-end="4">branje iz datotek formata “.json”,</li>
<li class="has-line-data" data-line-start="4" data-line-end="5">predogled postavitve v prostoru kot pogled iz smeri kamere in 3-d vrtljivo shemo,</li>
<li class="has-line-data" data-line-start="5" data-line-end="6">dodajanje novih objektov s poljubno barvo na sceno in shranjevanje v format “.json”,</li>
<li class="has-line-data" data-line-start="6" data-line-end="7">sprotno risanje končne slike na zaslonu,</li>
<li class="has-line-data" data-line-start="7" data-line-end="9">shranjevanje slike v formate oblike ‘JPEG’: ’<em>.jpg’,’</em>.jpeg’,’<em>.jpe’,’</em>.jfif’; ‘PNG’: ’<em>.png’; ‘BMP’: ’</em>.bmp’,’<em>.jdib’; ‘GIF’: ’</em>.gif’.</li>
</ul>
<p class="has-line-data" data-line-start="9" data-line-end="10">Ideja algoritma je bila narejena po korakih in kodi avtorja Romana Aflaka, ki je objavil “Ray Tracing From Scratch in Python” [Objavljeno: 26. 7. 2020. Vir:  <a href="https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9">https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9</a>] z nekaj dodatki in implementacijo kode v uporabniški vmesnik.</p>
<h3 class="code-line" data-line-start=10 data-line-end=11 ><a id="Instalacija_10"></a>Instalacija</h3>
<p class="has-line-data" data-line-start="11" data-line-end="12">Za pravilno delovanje programa je potrebno iz git-hub projekta prenesti vse Python datoteke in paziti, da so v isti mapi, kar velja za uporabo uporabniškega vmesnika. Na računalniku potrebujemo instaliran Python 3 in knjižnjice: numpy, math, json, tkinter, progress.bar in če ne uporabljamo uporabniškega vmesnika matplotlib.</p>
<h3 class="code-line" data-line-start=13 data-line-end=14 ><a id="Uporaba_raytrpyhttpsgithubcomenejcafraytracerblobmainraytrpy_13"></a>Uporaba <a href="https://github.com/enejcaf/ray-tracer/blob/main/raytr.py">raytr.py</a></h3>
<p class="has-line-data" data-line-start="14" data-line-end="15">Vhodni podatki programa so objekti, svetila, kamera in zaslon, ki so oblike seznama, v katerem je z indeksno številko predstavljen objekt. Pri zaslonu in kameri, je trenutno možna le en objekt, a se je obdržala splošna notacija. Poglejmo primer:</p>
<ul>
<li class="has-line-data" data-line-start="16" data-line-end="17">objekti:</li>
</ul>
<pre><code class="has-line-data" data-line-start="18" data-line-end="23" class="language-sh">objekti = [
    { <span class="hljs-string">'center'</span>: np.array([-<span class="hljs-number">0.2</span>, <span class="hljs-number">0</span>, -<span class="hljs-number">1</span>]), <span class="hljs-string">'radius'</span>: <span class="hljs-number">0.7</span>, <span class="hljs-string">'ambient'</span>: np.array([<span class="hljs-number">0.1</span>, <span class="hljs-number">0</span>, <span class="hljs-number">0</span>]), <span class="hljs-string">'diffuse'</span>: np.array([<span class="hljs-number">0.7</span>, <span class="hljs-number">0</span>, <span class="hljs-number">0</span>]), <span class="hljs-string">'specular'</span>: np.array([<span class="hljs-number">1</span>, <span class="hljs-number">1</span>, <span class="hljs-number">1</span>]), <span class="hljs-string">'shininess'</span>: <span class="hljs-number">100</span>, <span class="hljs-string">'reflection'</span>: <span class="hljs-number">0.5</span>, <span class="hljs-string">'n2'</span>: <span class="hljs-number">1.52</span> },
    { <span class="hljs-string">'center'</span>: np.array([<span class="hljs-number">0</span>, -<span class="hljs-number">9000</span>, <span class="hljs-number">0</span>]), <span class="hljs-string">'radius'</span>: <span class="hljs-number">9000</span> - <span class="hljs-number">0.7</span>, <span class="hljs-string">'ambient'</span>: np.array([<span class="hljs-number">0.1</span>, <span class="hljs-number">0.1</span>, <span class="hljs-number">0.1</span>]), <span class="hljs-string">'diffuse'</span>: np.array([<span class="hljs-number">0.6</span>, <span class="hljs-number">0.6</span>, <span class="hljs-number">0.6</span>]), <span class="hljs-string">'specular'</span>: np.array([<span class="hljs-number">1</span>, <span class="hljs-number">1</span>, <span class="hljs-number">1</span>]), <span class="hljs-string">'shininess'</span>: <span class="hljs-number">100</span>, <span class="hljs-string">'reflection'</span>: <span class="hljs-number">0.5</span>, <span class="hljs-string">'n2'</span>: <span class="hljs-number">1.4</span>}
]
</code></pre>
<p class="has-line-data" data-line-start="23" data-line-end="24">Opomba: Posamezen slovar objekta krogle je sestavljen iz središča: ‘center’: (x, y, z), velikosti radija: ‘radius’, parametrov Blinn-Phong modela svetlobe ‘ambient’, ‘diffuse’, ‘specular’, ‘shininess’, ‘reflection’ in n2, ki je lomni količnik materiala predmetov. Lomni količnik okolice je privzet na 1, vendar ga lahko manualno spremenimo.</p>
<ul>
<li class="has-line-data" data-line-start="24" data-line-end="25">svetloba:</li>
</ul>
<pre><code class="has-line-data" data-line-start="26" data-line-end="28" class="language-sh">svetloba = [{ <span class="hljs-string">'position'</span>: np.array([<span class="hljs-number">5</span>, <span class="hljs-number">5</span>, <span class="hljs-number">5</span>]), <span class="hljs-string">'ambient'</span>: np.array([<span class="hljs-number">1</span>, <span class="hljs-number">1</span>, <span class="hljs-number">1</span>]), <span class="hljs-string">'diffuse'</span>: np.array([<span class="hljs-number">1</span>, <span class="hljs-number">1</span>, <span class="hljs-number">1</span>]), <span class="hljs-string">'specular'</span>: np.array([<span class="hljs-number">1</span>, <span class="hljs-number">1</span>, <span class="hljs-number">1</span>]) }],
</code></pre>
<p class="has-line-data" data-line-start="28" data-line-end="29">Opomba: podobno velja tudi pri svetlobi, da imamo lego: ‘position’: (x, y, z) in tri parametre iz svetlobnega modela ‘ambient’, ‘diffuse’ in ‘specular’.</p>
<ul>
<li class="has-line-data" data-line-start="29" data-line-end="30">lega kamere:</li>
</ul>
<pre><code class="has-line-data" data-line-start="31" data-line-end="33" class="language-sh">kamera = [{<span class="hljs-string">'position'</span>: np.array([<span class="hljs-number">0</span>, <span class="hljs-number">0</span>, <span class="hljs-number">1</span>])}]
</code></pre>
<ul>
<li class="has-line-data" data-line-start="33" data-line-end="34">Velikost zaslona:</li>
</ul>
<pre><code class="has-line-data" data-line-start="35" data-line-end="37" class="language-sh">zaslon = [{<span class="hljs-string">'width'</span>: <span class="hljs-number">900</span>, <span class="hljs-string">'height'</span>: <span class="hljs-number">600</span>}]
</code></pre>
<h3 class="code-line" data-line-start=38 data-line-end=39 ><a id="Uporabniki_vmesnik_38"></a>Uporabniški vmesnik</h3>
<p class="has-line-data" data-line-start="39" data-line-end="40">Uporabniški vmesnik <a href="https://github.com/enejcaf/ray-tracer/blob/main/main.py">main.py</a> je preprost, saj vsebuje le nekaj intuitivnih gumbov. Dodatna opozorila, kot na primer, da niste izbrali datoteke, čeprav ste kliknili naloži datoteko in podobno se prikazujejo v terminalu, zato je dobro pustiti odprtega zraven. Prav tako je v terminalu prikazan prikazovalnik napredka, ki je vgrajen v <a href="https://github.com/enejcaf/ray-tracer/blob/main/raytr.py">raytr.py</a>, kar je namenjeno predvsem uporabi brez prikazovalnika slike v živo z uporabniškim vmesnikom.

</p>![Slika uporabniškega vmesnika](https://github.com/enejcaf/ray-tracer/blob/main/uporabniski_vmesnik.png "Slika uporabniskega vmesnika")

<h5 class="code-line" data-line-start=43 data-line-end=44 ><a id="1_Zaetek_uporabe_43"></a>1. Začetek uporabe:</h5>
<p class="has-line-data" data-line-start="44" data-line-end="51">1.1. Nalaganje vhodne datoteke:<br>
V glavnem oknu s klikom na gumb “Naloži” naložimo dototeko oblike “.json”. Če takšne datoteke še nimamo, lahko vzamemo katerega od primerov s strani <a href="https://github.com/enejcaf/ray-tracer">projekta</a> in jo preoblikujemo, ali pa uporabimo funkcijo<br>
print_json(objekti, svetloba, kamera, zaslon, ime) iz datoteke <a href="https://github.com/enejcaf/ray-tracer/blob/main/print_on_json.py">print_on_json.py</a>, s katero lahko zapišemo objekte v zgoraj opisanem formatu v pregledno datoteko “ime.json”. Ko je datoteka naložena vidimo na mreži naložen tloris naše sheme. Na mreži niso prikazane zelo velike žoge, ki so lahko uporabljene kot ravnine, da ne zakrijejo celotne slike.<br>
<br>
1.2. Dodajanje objektov<br>
Objekte lahko dodajamo s pritiskom na desni kumb “krogla”. Ob pritisku v pogovornem oknu izberemo barvo in na zaslonu se prikaže obarvan objekt. Hkrati se to zapiše tudi na našo delavno datoteko ‘ime.json’. Ker je na začetku žoga postavljena na naključno pozicijo z naključnim radijem (vse količine so normalizirane), lahko potem manualno ostale parametre še spreminjamo. Če se vse dogaja na isti datoteki, le-te ni potrebno ponovno nalagati.<br>
<br>
1.3. Izrisovanje slike<br>
Ko smo zadovoljni s sceno s klikom na gumb “Nariši”, program začne sproti izrisovat sliko na zaslonu v terminalu pa lahko vidimo tudi progress bar, če nas bolj pritegne opazovanje številk. Kako pogosto se posodablja slika, lahko zlahka spreminjamo v zanki, saj pri prepogostem osveževanju uporabniški vmesnik lahko postane neodziven. Za višjo kvaliteto slik je potrebno počakati nekaj časa. Ko je slika končana se prikažeta rdeča gumba “X” zapri, kar nas vrne na začetno stran programa, in gumb “Shrani”, ki nam omogoča shranjevanje slike, prek pogovornega okna, v formate oblike ‘JPEG’: ’<em>.jpg’,’</em>.jpeg’,’<em>.jpe’,’</em>.jfif’; ‘PNG’: ’<em>.png’; ‘BMP’: ’</em>.bmp’,’<em>.jdib’; ‘GIF’: ’</em>.gif’. Če po nesreči stisnemo “X” in bi vendarle radi sliko, ki smo jo na zaslonu čakali nekaj časa, bo do začetka novega izrisovanja, slika še shranjena pod imenom “trenutna.jpg”</p>
