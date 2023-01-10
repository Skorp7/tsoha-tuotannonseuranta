# TUOTANNONSEURANTA

Tämä sovellus on tietojenkäsittelytieteen aineopintojen harjoitustyö, tietokantasovellus. Tehtävänanto oli hyvin vapaa, kunhan relaatiotietokantaa käytetään monipuolisesti ja taulujen väliset suhteet ovat monimutkaisia. Python Flaskia ja PostgreSQL:ää tuli käyttää.

### Käyttötarkoitus

Sovellus on tarkoitettu hammaslaboratoroion tuotannon seurantaan. Hammaslaboratorio valmistaa yksilöllisiä suuhun asennettavia kojeita ja hampaita, asiakkaita ovat hammaslääkärit. Tuotantotiloissa tuotetta valmistaessa tilaukset liikkuvat usean eri työntekijän välillä ja tulee helposti sekaannuksia, kuka teki millekin tilaukselle viimeksi mitäkin. Välillä tilauksia voi unohtua eikä ne tavoita pyydettyä toimitusaikaa. Sovellus pyrkii ratkaisemaan näitä tuotannon ongelmia.

Sovelluksen avulla näkee mm.
* Mitkä tilaukset pitäisi olla valmiina TÄNÄÄN ja mikä niiden sen hetkinen status on (lähetetty/työn alla)
* Missä vaiheessa tuotantoketjua tietty tilaus on menossa
* Kuka työntekijä on tehnyt mitäkin työvaiheita
* Onko tietty tilaus jämähtänyt jonoon odottamaan jotakin tiettyä työvaihetta
* Onko jossain työvaiheessa yleisesti pitkät jonot (tarvitaanko tehostamista tai lisää työvoimaa)

Tilauksen kulku tuotannossa:
* Uusi tilaus saa luontivaiheessa ID:n joka merkitään työn mukana kulkevaan paperilähetteeseen.
* Kun työntekijä ottaa tilauksia (yleensä useita kerralla) omalle pöydälleen, hän merkitsee ID:n perusteella niille työvaiheen jonka aikoo suorittaa (esim. 'maalaus'). Työvaiheen statukseksi merkitään *Jonossa* tai *Työn alla* riippuen siitä aloittaako työntekijä kyseisen tilauksen käsittelyn heti vai jääkö se pöydälle jonoon.
   * Kun jonossa oleva tilaus pääsee työn alle, työntekijä merkkaa uuden työvaiheen ja klikkaa valinnan "Työn alla".
* Tilauksen viimeisen työvaiheen kohdalla työntekijä merkkaa valinnan "kirjaa tilaus samalla ulos", jolloin tilauksen tilaksi vaihtuu *lähetetty*, ja muutkin työntekijät näkevät että tämä tilaus on nyt valmis.


### Käyttäjäryhmät

Sovelluksessa on kolme käyttäjäryhmää: 'ei oikeuksia', 'peruskäyttäjä' ja 'työnjohtaja'.

* Peruskäyttäjä 
  * voi lisätä tilauksia, asiakkaita, tilaustyyppejä, työvaiheita, toimipaikkoja
  * voi etsiä tilauksia asiakas-, tilaus-, tuote- tai toimipaikkakohtaisesti
  * näkee kaikki tekemänsä työvaiheet listana

* Työnjohtaja voi tavallisten toimintojen lisäksi:
   * hakea tilausten työvaiheet käyttäjäkohtaisesti (seurata työntekijöiden toimintaa)
   * hakea kaikki mahdolliset tilaukset kerralla nähtäväksi
   * näkee tilastoja mm. työmääristä ja jonotusajoista
   * voi muuttaa käyttäjien oikeuksia
 
Oikeudet voidaan poistaa jos työntekijä esimerkiksi vaihtaa työpaikkaa tai tapahtuu jotain miksi häntä ei voi päästää tietokantaan käsiksi, esim. salasanavuoto. Kirjautumisoikeus kuitenkin säilyy siksi että tiedetään käyttäjän olevan olemassa ja oikeudet voi työnjohtajan halutessa palauttaa. Tällainen käyttäjä ei kuitenkaan pääse eteenpäin etusivulta.



### Tiedon pysyväistallennus

Tietokannan jaottelusta saa parhaiten kuvan tutustumalla [sql-skeemaan](schema.sql), ohessa myös kaaviokuva, mutta selvyyden vuoksi otetaan muutama huomio jaottelun taustasyistä; asiakaskunta on hammaslääkärit ja he saattavat työskennellä usealla eri vastaanotolla, sen takia toimipisteet on omassa taulussaan. Lisäksi yhteen tilaukseen liittyy yleensä yksi tilaustyyppi, jotka ovat useimmiten samoja tiettyjä. Tilaustyypin lisäämiseen on kuitenkin jätetty vapaat tekstikentät koska myös hyvin erikoisia tilauksia saattaa toisinaan tulla. Sama koskee työvaiheita. Jotkin työvaiheet toistuvat usein mutta joka päivä tulee myös uniikkeja työvaiheita. Työvaiheen lisäyksessä ehdotetaan kymmentä eniten käytettyä työvaihetta.

<img src="/documentation/tietokantakaavio.jpg" height="200" title="Tietokantakaaavio"> 

### Sovelluksen testaaminen

Kysy admin-tunnukset niin pääset käsiksi kaikkiin toimintoihin! 

[https://tsoha-tuotannonseuranta.fly.dev](https://tsoha-tuotannonseuranta.fly.dev)

Voit myös kokeeksi luoda uuden käyttäjän mutta sillä ei ole oikeuksia ennen kuin työnjohtaja lisää ne. Tyhjennä selaimen välimuisti ja historia jotta sovellus saa käyttöönsä uusimman css-tiedoston ja muotoilut näkyvät oikein. Ulkoasu ja lomakkeiden toiminnat on testattu toimivaksi tietokoneella tavallisella selaimella (Chrome, Firefox), joka on myös ajateltu käyttötapa. 

