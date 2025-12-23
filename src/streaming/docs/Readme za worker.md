**kratka dokumentacija** za `worker.py` (streaming varijanta).


## `worker.py`

Ovaj modul definiše **worker funkciju** za paralelnu obradu minibatch-eva u streaming pipeline-u.

Funkcija `worker` u petlji preuzima batch-eve iz thread-safe reda (`Queue`) i poziva prosleđenu funkciju za obradu nad svakim batch-om.
Rezultati obrade i greške se evidentiraju kroz metrike, dok se `stop_event` koristi za kontrolisano i uredno zaustavljanje worker niti.

Modul implementira klasični **producer–consumer obrazac** i omogućava skalabilnu obradu streaming podataka.
