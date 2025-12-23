**kratka dokumentacija** za `generator.py`
---

## `generator.py`

Ovaj modul služi za **generisanje fake/testnih fajlova** koji se koriste za simulaciju nightly file pipeline-a.

Funkcija `create_fake_files` kreira zadati broj binarnih fajlova sa **nasumičnom veličinom**, upisuje ih u lokalni direktorijum 
i vraća njihove putanje. Fajlovi se koriste kao ulaz za testiranje bucketing logike i paralelne obrade.

Modul je namenjen **lokalnom testiranju i demonstraciji pipeline-a**, a ne produkcionoj upotrebi.
