# AVM Vesting Streams — proiectul trei

Contract Rust pentru plăți eliberate în timp: până la 8 beneficiari, perioadă de
așteptare, plată liniară sau în tranșe, anulare opțională și returnarea părții
necuvenite. Sumele deja câștigate rămân beneficiarului după anulare.

Testele reale din standul AVM închid exact contabilitatea: 1.900 finanțate =
1.100 plătite beneficiarilor + 800 returnate. Sunt incluse eșecuri de transfer și
reluarea lor, nu doar scenarii în care totul merge bine.

Arhiva conține sursele, contractele WASM, testele, documentația și dovezile de
execuție. Cele 73 de teste native au trecut. 1.200 de cazuri verifică matematica
față de un calcul independent Python, iar 14.400 de pași verifică stările și
conservarea banilor.

Pentru reluare, urmează comenzile din README.md într-un Linux x86-64 sau WSL2.
Nu trebuie introduse chei private și nu sunt folosiți bani reali. Pentru înscriere
la bounty trebuie publicat proiectul și trimis linkul conform anunțului.
Proiect public: https://github.com/h2so4nackl-code/avm-vesting-streams
Publicarea nu înseamnă aprobarea proiectului sau acordarea recompensei.

Compatibilitatea a fost verificată cu SDK 0.2.0 și guest SDK 0.1.1, într-un stand local nou.
