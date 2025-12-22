
**main.py** docs

#### main.py – Orkestracija Data Engineering Pipeline-ova

Ovaj fajl predstavlja **ulaznu tačku (entry point)** projekta i ima ulogu **orkestratora** koji pokreće i koordinira dva nezavisna pipeline-a:

1. **Streaming pipeline** – obrada poruka u realnom vremenu korišćenjem minibatch pristupa
2. **File (batch) pipeline** – obrada fajlova u noćnom / batch režimu

Cilj dizajna je da demonstrira tipične **data engineering obrasce**: 
    - producer–consumer model, 
    - rad sa redovima (Queue), 
    - multithreading, 
    - metrike, 
    - graceful shutdown i 
    - modularnost.

---

## Pregled uvoza /importa

```python
from queue import Queue
import threading
```

* `Queue` – thread-safe red iz standardne biblioteke
* `threading` – omogućava paralelno izvršavanje worker niti

Ovo su osnovni gradivni blokovi za **producer–consumer arhitekturu**.

---

### Streaming pipeline importi

```python
from common.config import MINIBATCH_WINDOW_SECONDS
from streaming.source import message_source
from streaming.minibatch import minibatch_collector
from streaming.retry import retry_with_backoff
from streaming.worker import worker
from streaming.processing import process_batch
```

Moduli koji čine **streaming podsistem**:

* `message_source` – simulira real-time izvor poruka
* `minibatch_collector` – grupiše poruke u vremenske minibatch-e
* `worker` – generički worker koji obrađuje batch-e iz reda
* `process_batch` – konkretna logika obrade jednog batch-a
* `retry_with_backoff` – mehanizam za retry (korišćen u worker-u)

---

### File pipeline importi

```python
from files.generator import create_fake_files
from files.bucketing import bfd_buckets
from files.processor import process_one_bucket
from files.worker import bucket_worker
from common.metrics import init_file_metrics
```

Ovi moduli implementiraju **batch / file pipeline**:

* `create_fake_files` – generiše lažne fajlove za simulaciju
* `bfd_buckets` – grupiše fajlove u bucket-e po veličini
* `bucket_worker` – worker za obradu bucket-a
* `process_one_bucket` – logika obrade jednog bucket-a
* `init_file_metrics` – inicijalizacija metrika

---

## Funkcija: `run_message_pipeline()`

Ova funkcija pokreće **streaming pipeline**.

### Kreiranje queue-a /reda i osnovnih objekata

```python
work_queue = Queue(maxsize=50)
```

* Thread-safe red sa ograničenjem veličine
* Obezbeđuje **backpressure** ako producer proizvodi brže nego što worker-i obrađuju

---

### Metrike i signal za zaustavljanje

```python
metrics = {
    "batches_ok": 0,
    "batches_failed": 0,
    "messages_processed": 0,
}
stop_event = threading.Event()
```

* `metrics` – deljeni dictionary za praćenje uspešnosti
* `stop_event` – signal kojim se worker-i obaveštavaju da treba da se zaustave

Ovo je standardan obrazac za **graceful shutdown** u multithreading okruženju.

---

### Pokretanje worker niti

```python
for i in range(10):
    threading.Thread(
        target=worker,
        args=(i + 1, work_queue, metrics, stop_event, process_batch),
        daemon=True,
    ).start()
```

* Pokreće se 10 paralelnih worker-a
* Svaki worker:

  * čita batch-e iz reda
  * obrađuje ih pomoću `process_batch`
  * ažurira metrike

`daemon=True` znači da se niti automatski gase kada se glavni proces završi.

---

### Proizvodnja minibatch-eva

```python
minibatch_collector(
    message_source(duration_sec=300),
    window_sec=5,
    out_queue=work_queue,
)
```

* `message_source` emituje poruke tokom 5 minuta
* `minibatch_collector`:

  * skuplja poruke u vremenske prozore od 5 sekundi
  * formira minibatch-e
  * ubacuje ih u `work_queue`

Ovo simulira realan **streaming ingestion + windowing** scenario.

---

### Čekanje završetka obrade i gašenje

```python
work_queue.join()
stop_event.set()
time.sleep(1)
print("STREAMING METRICS:", metrics)
```

* `queue.join()` blokira dok svi batch-evi ne budu obrađeni
* `stop_event.set()` signalizira worker-ima da izađu iz petlje
* Na kraju se ispisuju metrike

---


## Funkcija: `run_file_pipeline()`

Ova funkcija implementira **batch / nightly file pipeline**.

### Generisanje fajlova i bucketing

```python
files = create_fake_files(100)
buckets = bfd_buckets(files, 10 * 1024 * 1024)
```

* Generiše se 100 fake fajlova
* Fajlovi se grupišu u bucket-e maksimalne veličine 10 MB

Ovo simulira tipičan **ETL file ingestion** scenario.

---

### Punjenje reda

```python
queue = Queue(maxsize=50)
for b in buckets:
    queue.put(b)
```

* Svi bucket-i se stavljaju u red pre početka obrade
* Red služi kao izvor posla za worker-e

---

### Worker-i i obrada

```python
metrics = init_file_metrics()
stop_event = threading.Event()

for i in range(10):
    threading.Thread(
        target=bucket_worker,
        args=(i + 1, queue, metrics, stop_event, process_one_bucket),
        daemon=True
    ).start()
```

* Pokreće se 10 worker-a
* Svaki worker obrađuje jedan bucket odjednom
* Metrike se centralno ažuriraju

---

### Završetak pipeline-a

```python
queue.join()
stop_event.set()
print("NIGHTLY FILES METRICS:", metrics)
```

* Čeka se da svi bucket-i budu obrađeni
* Signalizira se zaustavljanje worker-a
* Ispisuju se rezultati

---

## CLI interfejs (`__main__` blok)

```python
parser.add_argument(
    "--pipeline",
    choices=["files", "streaming", "all"],
    default="files",
)
```

Omogućava pokretanje pipeline-a iz cmd-a:

* `files` –  za file pipeline
* `streaming` – za streaming pipeline
* `all` – oba pipeline-a istovremeno

---

### Paralelno pokretanje oba pipeline-a

```python
t = threading.Thread(target=run_message_pipeline)
t.start()

run_file_pipeline()
t.join()
```

* Streaming pipeline se pokreće u posebnoj niti
* File pipeline se izvršava u glavnoj niti
* Na kraju se čeka završetak oba

Ovo demonstrira **koegzistenciju real-time i batch sistema**, što je čest slučaj u realnim data platformama.

---

## Zaključak

`main.py` predstavlja centralni orkestracioni layer koji:

* jasno razdvaja streaming i batch logiku
* koristi standardne concurrency obrasce
* omogućava testiranje, proširenje i demonstraciju znanja iz oblasti data engineering-a

Ovaj fajl je posebno pogodan za **code review**, jer pokazuje razumevanje:

* multithreading-a
* producer–consumer arhitekture
* metrika i graceful shutdown-a
