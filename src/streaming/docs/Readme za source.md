**kratka dokumentacije** za `source.py`.



## `source.py`

Ovaj modul implementira **simulirani izvor poruka** za streaming pipeline.

Funkcija `message_source` generiše poruke tokom definisanog vremenskog intervala i emituje ih sa nasumičnim kašnjenjem koje prati eksponencijalnu distribuciju, 
čime se simulira realan, nepravilan dolazak događaja. Poruke se emituju kao generator, što omogućava efikasan rad i zauzimanje memorije i integraciju sa minibatch i worker logikom.

Modul je namenjen **testiranju i demonstraciji streaming arhitekture**, a ne produkcionom ingestovanju podataka.
