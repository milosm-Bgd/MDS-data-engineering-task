### bucketing.py – Grupisanje fajlova u bucket-e (Nightly File Pipeline)

Ovaj modul implementira **algoritme za grupisanje fajlova u bucket-e** na osnovu njihove veličine, sa ciljem da se fajlovi efikasno rasporede 
u ograničene jedinice za obradu (npr. maksimalna veličina po batch-u).

Ovakav pristup je tipičan u **nightly / batch data pipeline-ovima**, gde se fajlovi pakuju pre slanja na paralelnu obradu ili distribuciju.

---

### Uvoz zavisnosti

```python
from .validation import os
```

* Modul koristi `os` za rad sa fajl sistemom
* `os` se re-eksportuje iz `validation` modula kako bi se centralizovale osnovne zavisnosti

Napomena: U produkcionom kodu bi se `import os` obično radio direktno, ali ovakav pristup pojednostavljuje mockovanje i testiranje.

---

## Funkcija: `file_size_bytes`

```python
def file_size_bytes(path):
    return os.path.getsize(path)
```

### Opis

* Vraća veličinu fajla u bajtovima za dati `path`
* Predstavlja pomoćnu (utility) funkciju

### Zašto je izdvojena?

* Povećava čitljivost algoritama za bucketing
* Omogućava lakšu zamenu implementacije (npr. remote storage)

---

## Algoritam: First-Fit

### Funkcija: `first_fit_buckets`

```python
def first_fit_buckets(paths, target_bytes):
```

#### Ulazni parametri

* `paths` – lista putanja do fajlova
* `target_bytes` – maksimalna dozvoljena veličina jednog bucket-a

#### Logika rada

* Iterira kroz fajlove redom
* Svaki fajl pokušava da smesti u **prvi bucket** u koji može stati
* Ako ne može ni u jedan postojeći bucket → kreira se novi

```python
for bucket in buckets:
    if sum(file_size_bytes(p) for p in bucket) + file_size_bytes(path) <= target_bytes:
```

#### Karakteristike

* Jednostavan i brz algoritam
* Nije optimalan u pogledu popunjenosti bucket-a

---

## Algoritam: First-Fit Decreasing (FFD)

### Funkcija: `ffd_buckets`

```python
def ffd_buckets(paths, target_bytes):
    return first_fit_buckets(sorted(paths, key=file_size_bytes, reverse=True), target_bytes)
```

### Opis

* Poboljšana verzija First-Fit algoritma
* Pre raspoređivanja:

  * fajlovi se sortiraju po veličini (opadajući niz)

### Prednosti

* Značajno bolja popunjenost bucket-a
* Jednostavna implementacija (reuse postojećeg koda)

---

## Algoritam: Best-Fit Decreasing (BFD)

### Funkcija: `bfd_buckets`

```python
def bfd_buckets(paths, target_bytes):
```
Ovo je **najsofisticiraniji algoritam u modulu** i on se koristi u `main.py`.

---

### Korak 1: Sortiranje fajlova

```python
sorted_paths = sorted(paths, key=file_size_bytes, reverse=True)
```

* Veći fajlovi se raspoređuju prvi
* Smanjuje se rizik da veliki fajl ostane sam u bucket-u

---

### Korak 2: Pronalaženje "najboljeg" bucket-a

```python
best_idx, best_remaining = None, None
```

Za svaki fajl:

* prolazi se kroz sve postojeće bucket-e
* traži se onaj gde će **preostali prostor biti minimalan**

```python
remaining = target_bytes - (current + size_p)
```

---

### Korak 3: Dodavanje fajla

* Ako nijedan bucket ne može da primi fajl → kreira se novi
* U suprotnom → fajl se dodaje u najbolji postojeći bucket

```python
if best_idx is None:
    buckets.append([path])
else:
    buckets[best_idx].append(path)
```

---

## Zašto je BFD izabran u pipeline-u?

* Smanjuje broj bucket-a
* Ravnomerno opterećuje worker-e
* Simulira realne probleme pakovanja 

U kontekstu **nightly file pipeline-a**:

* bucket = jedinica paralelne obrade
* cilj = maksimalna iskorišćenost resursa

---

## Povezanost sa ostatkom sistema

* `bfd_buckets` se koristi u `main.py`
* Rezultat (lista bucket-a) se prosleđuje worker-ima putem `Queue`

---

## Zaključak
`bucketing.py` demonstrira:

* razumevanje bin-packing problema
* izbor algoritma u odnosu na realna ograničenja
* jasno odvajanje odgovornosti
