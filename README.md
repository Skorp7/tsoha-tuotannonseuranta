# TUOTANNONSEURANTA

Sovellus on tarkoitettu hammaslaboratoroion tuotannon seurantaan. Tuotantotiloissa tuotetta valmistaessa tilaukset liikkuvat usean eri työntekijän välillä ja tulee helposti sekaannuksia, kuka teki millekin tilaukselle viimeksi mitäkin. Välillä tilauksia voi unohtua eikä ne tavoita pyydettyä toimitusaikaa. Sovellus pyrkii ratkaisemaan näitä tuotannon ongelmia.

Uusi tilaus saa luontivaiheessa ID:n joka merkitään työn mukana kulkevaan paperilähetteeseen.
Tämän ID:n perusteella tilaukseen liittyviä työvaiheita voi merkitä ylös tai selvittää tilauksen sen hetkisen tilan.

Sovelluksen avulla näkee mm.
* Mitkä tilaukset pitäisi olla valmiina TÄNÄÄN ja mikä niiden sen hetkinen status on (lähetetty/työn alla)
* Missä vaiheessa tuotantoketjua tietty tilaus on menossa
* Kuka työntekijä on tehnyt mitäkin työvaiheita
* Onko tietty tilaus jämähtänyt jonoon odottamaan jotakin tiettyä työvaihetta
* Onko jossain työvaiheessa yleisesti pitkät jonot (tarvitaanko tehostamista tai lisää työvoimaa)

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

Tietokannan jaottelusta saa parhaiten kuvan tutustumalla [sql-skeemaan](schema.sql), mutta selvyyden vuoksi otetaan muutama huomio jaottelun taustasyistä; asiakaskunta on hammaslääkärit ja he saattavat työskennellä usealla eri vastaanotolla, sen takia toimipisteet on omassa taulussaan. Lisäksi yhteen tilaukseen liittyy yleensä yksi tilaustyyppi, jotka ovat useimmiten samoja tiettyjä. Tilaustyypin lisäämiseen on kuitenkin jätetty vapaat tekstikentät koska myös hyvin erikoisia tilauksia saattaa toisinaan tulla. Sama koskee työvaiheita. Jotkin työvaiheet toistuvat usein mutta joka päivä tulee myös uniikkeja työvaiheita. Työvaiheen lisäyksessä ehdotetaan kymmentä eniten käytettyä työvaihetta.

<img src="/documentation/tietokantakaavio.jpg" height="200" title="Tietokantakaaavio"> 

### Sovelluksen testaaminen

Kokeile sovellusta tunnuksella **admin** ja salasanallas **pass** niin pääset käsiksi kaikkiin toimintoihin! 

Sovelluksen osoite: https://tsoha-tuotannonseuranta.herokuapp.com 

Voit myös kokeeksi luoda uuden käyttäjän jolle tulee luodessa peruskäyttäjän oikeudet. Ulkoasu ja lomakkeiden toiminnat on testattu toimivaksi tietokoneella tavallisella selaimella (Chrome, Firefox), joka on myös ajateltu käyttötapa.

