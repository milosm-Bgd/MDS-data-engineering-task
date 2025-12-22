# Data Engineering zadatak – Streaming i obrada fajlova

Ovaj projekat modeluje **dva nezavisna data processing pipeline-a**:

1. **Streaming pipeline (obrada poruka u realnom vremenu)**
2. **Noćni pipeline za obradu fajlova**

Cilj projekta je da demonstrira:
- rad sa konkurentnim sistemima (threading, queue)
- vremensko grupisanje podataka (minibatches)
- efikasnu obradu velikog broja malih fajlova
- testabilan i proširiv dizajn

---

## 1. Streaming pipeline

### Opis

- Izvor podataka emituje poruke prema **Poisson distribuciji**
  (~10 poruka u minuti).
- Prva pristigla poruka pokreće kreiranje minibatch-a.
- Minibatch sadrži sve poruke koje pristignu u narednih **5 minuta**.
- Kada se minibatch formira, šalje se u **worker pool (10 thread-ova)**.
- Kreiranje novih minibatch-eva ne zavisi od završetka prethodnih.

### Tehnička rešenja

- `Queue` se koristi za komunikaciju između producer-a i worker-a
- Worker-i rade paralelno
- Implementirana je **retry logika sa exponential backoff-om**
- Implementirano je **graciozno gašenje worker-a** pomoću `threading.Event`

---

## 2. Noćni pipeline za obradu fajlova

### Opis

- Drugi proces prikuplja ~100 fajlova tokom noći (simulirano).
- Veličine fajlova prate **eksponencijalnu distribuciju**.
- Obrada malih fajlova pojedinačno je neefikasna.
- Fajlovi se pakuju u **bucket-e veličine do 10MB**.
- Svaki bucket se šalje u worker pool na paralelnu obradu.

### Bucketing strategije

Implementirane su sledeće strategije:
- **First Fit (FF)**
- **First Fit Decreasing (FFD)**
- **Best Fit Decreasing (BFD)**

Strategija se može lako zameniti bez izmene ostatka sistema.

---

## Struktura projekta


src/
streaming/ # live message ingestion
files/ # nightly file ingestion
common/ # shared utilities
main.py # orchestration entry point

tests/
test_streaming.py
test_retry.py
test_bucketing.py
test_bucket_worker.py



---

## Testovi i mock-ovi

Testovi su napisani koristeći **pytest** i mock-ovanje eksternih zavisnosti.

Mock-ovani su:

- izvori poruka
- veličine fajlova
- obrada fajlova (filesystem)
- processing funkcije

Cilj testova je da se proveri:

- ispravnost logike
- paralelno izvršavanje
- retry mehanizmi
- ispravno gašenje worker-a

### Pokretanje testova
PYTHONPATH=src pytest

### Pokretanje noćnog pipeline-a za fajlove:
python src/main.py

Nacin dizajna:

Fokus na čitljiv i održiv kod
Izbegavanje preteranog apstraktovanja
Jasna separacija odgovornosti
Kod lako testabilan
Notebook je korišćen za inicijalnu istrazivanje, a zatim je kod strukturiran kao Python projekat.