## `bucketing.py`

Ovaj modul implementira logiku za **grupisanje fajlova u bucket-e** na osnovu njihove veličine, sa ciljem da ukupna veličina fajlova u jednom bucket-u ne pređe zadati limit.

Koriste se klasični **bin-packing heuristički algoritmi** koji su česti u batch i data engineering sistemima.

### Glavne funkcije

* `file_size_bytes(path)`
  Vraća veličinu fajla u bajtovima.

* `first_fit_buckets(paths, target_bytes)`
  Implementira *First-Fit* algoritam – svaki fajl se smešta u prvi bucket u koji može da stane, ili se kreira novi bucket.

* `ffd_buckets(paths, target_bytes)`
  *First-Fit Decreasing* varijanta – fajlovi se prvo sortiraju po veličini, dajući bolju popunjenost bucket-a.

* `bfd_buckets(paths, target_bytes)`
  *Best-Fit Decreasing* varijanta – fajl se smešta u bucket gde ostaje najmanje slobodnog prostora.
  Ova funkcija se koristi u nightly file pipeline-u jer daje najefikasniju raspodelu.

### Kontekst upotrebe

Bucket predstavlja **jedinicu paralelne obrade** u nightly pipeline-u.
Cilj je ravnomerno opterećenje worker-a i efikasno korišćenje resursa.
