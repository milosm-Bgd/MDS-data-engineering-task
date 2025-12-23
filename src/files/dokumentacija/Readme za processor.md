**kratka dokumentacije** za `processor.py`

## `processor.py`

Ovaj modul sadrži logiku za **obradu jednog bucket-a fajlova** u okviru nightly file pipeline-a.

Funkcija `process_one_bucket` iterira kroz fajlove u bucket-u, proverava da li je fajl validan i zatim ga kopira u 
izlazni direktorijum uz proveru integriteta (checksum). Nevalidni fajlovi se preskaču, dok se uspešno obrađeni fajlovi 
broje i taj broj se vraća kao rezultat.

Ovaj modul predstavlja **business logic sloj** pipeline-a i koristi se direktno od strane worker-a koje paralelno 
obrađuju bucket-e.
