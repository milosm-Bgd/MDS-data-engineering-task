**kratke dokumentacija** za `minibatch.py`

## `minibatch.py`

Ovaj modul implementira **vremensko grupisanje poruka u minibatch-eve** za streaming pipeline.

Funkcija `minibatch_collector` prikuplja poruke iz generatora (`message_source`) i grupiše ih u liste na osnovu definisanog vremenskog prozora (`window_sec`).
Kada prozor istekne, formirani minibatch se prosleđuje u izlazni red (`Queue`) na dalju paralelnu obradu.

Ovakav pristup je tipičan u streaming sistemima jer omogućava **kontrolu kašnjenja i efikasniju obradu** u odnosu na rad sa pojedinačnim porukama.

