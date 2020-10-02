# TUOTANNONSEURANTA

_Tämä on kurssin 'Tietokantasovellus' -harjoitustyö._

[Sovelluskehityksen tämän hetkinen tilanne](#sovelluskehityksen-tämän-hetkinen-tilanne)


Sovellus on tarkoitettu hammaslaboratoroion tuotannon seurantaan. Sen avulla saa yleiskäsityksen siitä mitä tuotantotiloissa tapahtuu ja sen olisi tarkoitus olla apuväline työnjohtajille tuotannon tehostamisessa. Tuotantotiloissa tilaukset liikkuvat usean eri työntekijän välillä ja tulee helposti sekaannuksia, kuka teki millekin tilaukselle viimeksi mitäkin. Välillä tilauksia voi unohtua eikä ne tavoita pyydettyä toimitusaikaa. Sovellus pyrkii ratkaisemaan näitä tuotannon ongelmia.

Sovelluksen avulla tulee saamaan selville muun muassa:
* Missä vaiheessa tuotantoketjua tietty tilaus on menossa
* Onko tietty tilaus jämähtänyt jonoon odottamaan jotakin tiettyä työvaihetta
* Onko jossain työvaiheessa yleisesti pitkät jonot (tarvitaanko tehostamista tai lisää työvoimaa)
* Mitkä tilaukset pitäisi olla valmiina TÄNÄÄN ja mikä niiden sen hetkinen status on
* Kuka työntekijä on tehnyt mitäkin työvaiheita

### Käyttäjäryhmät

Sovellukseen tulee kolme käyttäjäryhmää:
* ei oikeuksia
  * pystyy kirjautumaan sisään muttei pääse eteenpäin tuotanto-välilehdelle tai muualle
 
* peruskäyttäjä 
  * voi lisätä tilauksia, asiakkaita, tilaustyyppejä, työvaiheita, toimipaikkoja
  * voi etsiä tilauksia asiakaskohtaisesti, tilauskohtaisesti, toimipaikkakohtaisesti

* työnjohto 
  * samat toiminnot kuin peruskäyttäjällä mutta lisäksi:
  * voi muuttaa toisten käyttäjien oikeuksia (peruskäyttäjä, työnjohtaja, ei oikeuksia)
  * näkee tilastoja tuotannosta, esim. työvaiheiden kestoja, tilausmääriä, asiakaskohtaisia tilausmääriä, toimipaikkakohtaisia tilausmääriä
 
Oikeudet voidaan poistaa jos työntekijä esimerkiksi vaihtaa työpaikkaa tai tapahtuu jotain miksi häntä ei voi päästää tietokantaan käsiksi, esim. salasanavuoto. Kirjautumisoikeus pysyy siksi että tiedetään käyttäjän olevan olemassa ja oikeudet voi työnjohtajan halutessa palauttaa.

### Käyttöliittymä

* Kirjautumisnäkymä
  * Rekisteröityminen

* Tuotanto-ikkuna
  * Aukeaa TÄNÄÄN-ikkunaan josta näkee päivän aikana valmiiksi saatavat tilaukset
  * Työmääriä voi tarkastella hakemalla niitä erilaisilla parametreillä (tilauksen tyyppi, asiakas, toimipaikka, tilausta käsitellyt työntekijä)
  * Tilauksen tilaa voi seurata hakemalla esim. tilauksen id:llä
    * näyttää esim. aikajanana kuinka pitkä aika on mennyt missäkin työvaiheessa ja ilmaisee jollain tapaa jos aika on yli keskiarvon
  * Työvaiheen lisääminen
  * Tilauksen lisääminen
    * Asiakkaan lisääminen
    * Tilaustyypin (tuotteen) lisääminen
    * Toimipaikan lisääminen
* Hallinta-ikkuna (vain työnjohtajille)
  * Käyttäjien statuksen vaihto
  * Keskimääräiset jonotusajat eri työvaiheisiin
  * Keskimääräiset toimitusajat tilastona eri tyyppisille tilauksille

* Tilauksella on status, se voi olla 'työn alla' tai 'lähetetty'. 
* Tilauksen työvaiheilla on myös statukset, status voi olla 'jonossa' tai 'käsittelyssä/käsitelty'.
* Mahdollisuuksien mukaan myös muita toimintoja ja tilastoja työnjohtoa helpottamaan


### Tiedon pysyväistallennus

Sovelluksen tietokantana toimii PostgreSQL -tietokanta. Tietokantatauluja 6kpl ja ne on jaettu oheisen kaavion mukaisesti. Lisäksi on yksi taulu johon on tallennettu Suomen kuntien nimet. Tietokannan jaottelusta saa parhaiten kuvan tutustumalla [sql-skeemaan](schema.sql), mutta selvyyden vuoksi otetaan muutama huomio jaottelun taustasyistä; asiakaskunta on hammaslääkärit ja he saattavat työskennellä usealla eri vastaanotolla, sen takia toimipisteet on omassa taulussaan. Lisäksi yhteen tilaukseen liittyy yleensä yksi tilaustyyppi, jotka ovat useimmiten samoja tiettyjä. Tilaustyypin lisäämiseen on kuitenkin jätetty vapaat tekstikentät koska myös hyvin erikoisia tilauksia saattaa tulla.

<img src="/documentation/tietokantakaavio.jpg" height="300" title="Tietokantakaaavio"> 

Tietokannassa asiakkaiden ja käyttäjien kohdalla on sarake 'visible', jolla ne voi piilottaa poistotilanteessa, jottei yhteydet katkea tehtyihin tilauksiin. Tämä on kuitenkin vielä kehityksen alla, että jääkö tämä ominaisuus vai onko siitä vain enemmän haittaa kuin hyötyä.



### Sovelluskehityksen tämän hetkinen tilanne


Tällä hetkellä sovellus tukee seuraavia toimintoja:
* Kirjautuminen
* Käyttäjien statuksen vaihto
* Tilastot eniten työvaiheita tehneistä käyttäjistä ja jonotusajoista
* Tilausten lisääminen
* Tilaustyyppien (tuotteiden) lisääminen
* Asiakkaiden lisääminen
* Toimipaikkojen lisääminen
* Tilausten etsiminen tilaus-id:llä
* Tilausten etsiminen joihin sisäänkirjautunut käyttäjä liittyy käsittelijänä
* TÄNÄÄN-ikkunassa näkyy tänään toimitettavat tilaukset ja niiden sen hetkinen tila

Ulkoasu ja lomakkeiden toiminnat on testattu tietokoneella tavallisella selaimella (Chrome, Firefox), joka on myös ajateltu käyttötapa. Esimerkiksi lomakkeiden virheentarkistus ja virheilmoitukset ei vielä toimi tekstiselaimella eikä pudotusvalikoiden valinnan aiheuttama heräte.

Sovellusta pääsee kokeilemaan osoitteessa: https://tsoha-tuotannonseuranta.herokuapp.com
Jos luot itsellesi uuden tunnuksen kokeilua varten, sillä tulee olemaan peruskäyttäjän oikeudet. Voit myös kokeilla adminin oikeuksia tunnuksella 'admin' ja salasanalla 'pass'.



-------------------------------------------------------
_Olen aikaisemmin tehnyt ohjelmistotekniikan kurssilla [tuotannonohjausjärjestelmän](https://github.com/Skorp7/ot-harjoitustyo) Javalla ja SQLitellä. Tämä sovellus perustuu siis samaan ideaan, mutta eri painotuksilla ja ohjelmoin sen kokonaan alusta alkaen. Kielenä on Python (minulle uusi kieli) ja tietokantana PostgreSQL._
