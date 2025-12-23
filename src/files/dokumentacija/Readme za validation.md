**kratka i praktične dokumentacija** za `validation.py`

## `validation.py`

Ovaj modul sadrži pomoćne funkcije za **validaciju fajlova i proveru njihovog integriteta** tokom nightly file pipeline-a.

Funkcija `validate_file` proverava da li fajl postoji i da li ima određenu veličinu.
Funkcija `sha256_file` računa SHA-256 checksum fajla i koristi se za proveru integriteta podataka.

Funkcija `copy_and_verify` kopira fajl u izlazni direktorijum i upoređuje checksum pre i posle kopiranja, 
čime se osigurava da tokom I/O operacija nije došlo do oštećenja podataka. U slučaju greške raises izuzetak koji worker obrađuje i beleži u metrikama.
