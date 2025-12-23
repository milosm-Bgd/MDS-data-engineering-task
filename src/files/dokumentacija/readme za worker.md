**kratka dokumentacije** za `worker.py`


## `worker.py`

Ovaj modul definiše **worker funkciju** za paralelnu obradu bucket-a u nightly file pipeline-u.

Funkcija `bucket_worker` u petlji čita bucket-e iz reda (`Queue`) i za svaki bucket poziva prosleđenu funkciju za obradu.
Uspešna i neuspešna obrada se evidentiraju kroz metrike, dok se `stop_event` koristi za kontrolisano zaustavljanje worker-a.

Ovaj modul implementira klasični **producer–consumer obrazac** i omogućava skaliranje obrade fajlova korišćenjem multi-thredinga.
