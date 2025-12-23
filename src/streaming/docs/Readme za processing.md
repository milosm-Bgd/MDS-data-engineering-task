**kratka dokumentacije** za `processing.py`.


## `processing.py`

processing modul sadrži **simulaciju obrade jednog minibatch-a poruka** u streaming pipeline-u.

Funkcija `process_batch` uvodi kratko kašnjenje kako bi simulirala stvarnu obradu i nasumično izaziva grešku sa određenom verovatnoćom, 
što omogućava testiranje retry i error-handling logike u worker-ima. U slučaju uspeha, funkcija vraća broj obrađenih poruka u batch-u.

Modul je namenjen **demonstraciji ponašanja sistema pod opterećenjem i greškama** u kontekstu obrade zadatog tehničkog DE zadatka.
