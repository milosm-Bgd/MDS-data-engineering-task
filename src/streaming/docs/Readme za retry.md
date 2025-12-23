**kratka dokumentacije** za `retry.py`



## `retry.py`

Ovaj modul implementira jednostavan **retry mehanizam sa eksponencijalnim backoff-om**.

Funkcija `retry_with_backoff` izvršava prosleđenu funkciju i u slučaju greške pokušava ponovo, uz postepeno povećavanje vremena čekanja između pokušaja.
Ako se greška ponovi više puta od dozvoljenog broja retry-a, izuzetak se prosleđuje dalje.

Modul se koristi u streaming pipeline-u kako bi sistem bio **otporniji na prolazne greške** bez komplikovanja glavne logike obrade.
