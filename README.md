PULLONKAULA
=======

_Tämä on kurssin 'Tietokantasovellus' -harjoitustyö._

Olen aikaisemmin tehnyt ohjelmistotekniikan kurssilla [tuotannonohjausjärjestelmän](https://github.com/Skorp7/ot-harjoitustyo) Javalla ja SQLitellä. Nyt aion tehdä saman tapaisen sovelluksen, mutta eri painotuksilla ja kokonaan alusta alkaen. Toteutan siis kokonaan uuden sovelluksen ja rakennan myös tietokantapuolen eri tavalla. Kielenä tulee olemaan Python (minulle uusi kieli) ja tietokantana PostgreSQL.

Aikaisemmassa sovelluksessa pääpaino oli siinä, että näkee helposti kuka työntekijä on tehnyt minkäkin työvaiheen ja jos jokin tilaus on hukassa, niin koodilla voi etsiä kuka tilausta on käsitellyt viimeksi. Sovellus näytti myös päiväkohtaisia työmääriä.

Tässä uudessa sovelluksessa olisi tarkoitus päästä seuraamaan sitä, kuinka kauan mikäkin työvaihe kestää ja lisätä tilauksille mahdollisuus jäädä jonottamaan työn alle pääsyä. Näin työnjohtaja näkisi helposti missä kohtaa tuotantoa on pullonkauloja ja miksi jotkut tietyt tilaukset aina myöhästyvät.
Esimerkiksi jos tilaus seisoo jonossa kauan ennen kuin se uloskirjataan, niin tiedetään että laskutus on hidasta ja siihen tarvittaisiin tehostamistoimia. Tuotantotilana pidän edellisen sovelluksen tavoin hammaslaboratorion, mutta pyrin rakentamaan sovelluksen niin että se olisi helposti muokattavissa koodia vähän muuttamalla eri tuotannon käyttöön.

Käyttäjäryhmät
--------
Sovellukseen tulee kaksi käyttäjäryhmää:
* työnjohto 
* työntekijät 

Työnjohto näkee kaikkien tilausten kestot kussakin työvaiheessa ja työntekijät näkevät omien työvaiheidensa kestot. Esimerkiksi laskuttaja näkee kuinka kauan häneltä kuluu keskimäärin laskutukseen per tietynlainen tilaus.

Käyttöliittymä
--------
* Kirjautumismahdollisuus
* Eri tyyppisten tilausten haku
  * näyttää esim. aikajanana kuinka pitkä aika on mennyt missäkin työvaiheessa keskimäärin
* Tietyn tilauksen haku koodilla
  * näyttää esim. aikajanana kuinka pitkä aika on mennyt missäkin työvaiheessa ja ilmaisee jollain tapaa jos aika on yli keskiarvon
* Keskimääräiset toimitusajat tilastona eri tyyppisille tilauksille
* Mahdollisuuksien mukaan myös muita toimintoja ja tilastoja työnjohtoa helpottamaan




