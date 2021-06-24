# Pigeon Invadors

Projekat Pigeon Invadors je rađen kao projekat za predmet Distribuirani računarski sistemi u elektroenergetici, u okviru tima od 3. 

## O projektu

Projekat Pigeon Invaders predstavlja igricu napravljenu po uzoru na arkadnu igru Space Invaders. 
Za razliku od Space Invaders-a, u igrici Pigeon Invaders je omogućen rad sa 2 igrača. Pri startovanju aplikacije, oba igrača se nalaze u uglovima okvira za dozvoljeno kretanje. Korisnici pokreću svoje avatare horizontalno na strelice levo i desno, odnosno na tastere A i D. Umesto alien-a, neprijatelji igrača su pigeon-i, postavljeni u formaciji 3x10, koji se kreću po zadatoj šemi od jedne do druge ivice dozvoljene oblasti ekrana aplikacije. Oni napadaju igrače ispaljivanjem projektila nasumično i nezavisno jedni od drugih. Kao u originalu, da bi igrač prešao na sledeći nivo, neophodno je da pogodi svakog neprijatelja projektilima koje izbacuje na strelicu na gore tj. taster W. Novim nivom se povećava brzina kojom projektil leti ka igraču i šansa da će neprijatelj ispaliti projektil, dok se životi igrača ponovo inicijalizuju na 3. Kada projektili pigeon-a pogode igrača, broj njegovih života se smanjuje. Takođe, dodata je još jedna uloga u projektu, velika ptica koja se pojavljuje iznad ostalih pigeon-a i vraća 1 život igraču koji je pogodi. Igrica se završava u slučaju da oba igrača izgube sve živote i tada se za pobednika proglašava igrač koji je najduže ostao u igrici ili ako su se neprijatelji spustili do kraja ekrana i tako pobedili igrača.

Realizacija projekta Pigeon Invaders je izvršena korišćenjem Python jezika, multiprocessing biblioteke i PyQt5 okvira.

Zahtev izrade programa je napisan u fajlu **T3 - Space Invaders.pdf**

Detaljniji opis o samom projektu dostupan je u okviru fajla **Dokumentacija.pdf**


 
