Megismerkedni egy PaaS környezettel felhasználói szinten és segítségével létrehozni egy fényképalbum alkalmazást.

Eszközök, feltételek
A megoldásnak valamilyen publikusan elérhető PaaS környezetben (OpenShift/AppEngine/Heroku/...) kell műkködnie. 
A végleges alkalmazásváltozatnak skálázhatónak és többrétegűnek kell lennie.
Tetszőleges nyelv, tetszőleges keretrendszer használható.
GitHub-ra feltöltve a build induljon el automatikusan.

Funkcionális követelmények:
Fényképek feltöltése/törlése.
Miden fényképnek legyen neve (max. 40 karakter), és feltöltési dátuma (év-hó-nap óra:perc)
Fényképek nevének és dátumának listázása név szerint/dátum szerint rendezve.
Lista egy elemére kattintva mutassa meg a név mögötti képet.
Felhasználókezelés (regisztráció, belépés, kilépés).
Feltöltés, törlés csak bejelentkezett felhasználónak engedélyezett.
Tetszőleges további opcionális funkciók.


Segítség
Első lépésként érdemes a választott PaaS szolgáltatás lehetőségeit (támogatott nyelvek, keretrendszer, adatbázis, ...) ellenőrizni.
Pl. Regisztráljon az OpenShift szolgáltatására és indítson egy ingyenes Developer Sandbox-ot!
Próbáljon ki egy egyszerű példát (pl. Django)! Ehhez segítséget talál az előző féléves diák között (ld. lent).
Az alkalmazás viszonylag egyszerűen megvalósítható a Django keretrendszerrel
Készítse el az alkalmazást első minimál válozatát először lokális környezetben lokális adatbázissal (pl. sqlite) felhasználókezelés nélkül.
Töltse fel a GitHubra, majd onnan a választott PaaS környezetbe.
Kapcsolja össze repozitorit és a PaaS rendszert megfelelő hook-kal. 
Teszteljen és folytassa a fejlesztést.


Benyújtandó
A megoldás forrásfájljai, és egy dokumentációja GitHub-on. (linket kell megadni)
Működó alkalmazás a PaaS környezetben (be kell mutatni)
A feladatot bontsa két fő részfeladatra (pl. nincs még minden funkció kész) Ez lesz az első beadás (4. feladat) 
A végleges, külön adatbázis-szerverrel működő változat lesz az 5. feladat beadása.