Zadanie będące częścią kursu https://sklep.securitum.pl/wstep-do-inzynierii-wstecznej-i-asemblera

Napisz program w czystym asemblerze (patrz przykład hello-pure-asm), który:

1. Za pomocą syscalla mmap zaalokuje 4096 bajtów pamięci.

HINT: Zobacz jak wywołuje się funkcję mmap w języku C, żeby to zrobić. W
wywołaniach pojawia się trochę stałych – skorzystaj z programu rgrep żeby je
odnaleźć w katalogu /usr/include.

2. Do tej pamięci (której adres będzie zwrócony w rejestrze RAX) zapisz kolejne 64-bitowe (QWORD) wartości (składnia poniżej: adres szesnastkowo: wartość):
```
RAX+0: 0x7365597b41786548
RAX+8: 0x696854746f474921
RAX+0x10: 0x6c6c616373795373
RAX+0x18: 0x4c216b726f576f54
RAX+0x20: 0x656c654373277465
RAX+0x28: 0x7d21216574617262
```
HINT: pamiętaj o QWORD PTR; pamiętaj o możliwych kodowaniach MOV – może nie być odpowiedniego, żeby załatwić każdy zapis jedną instrukcją, ale nadal da się ten problem rozwiązać sekwencją kilku instrukcji.

3. Wywołaj syscall write, tak żeby do deskryptora plików (fd) od standardowego wyjścia (1) wysłał 48 bajtów zaczynając od początku regionu pamięci zwróconego przez mmap (tj. de facto chcemy wypisać to co wrzuciliśmy do pamięci).

4. Wywołaj syscall exit z parametrem 0.

To ćwiczenie polega na przyzwyczajeniu się do korzystania z syscalli, tablicy syscalli, oraz
wyszukiwania dziwnych stałych w /usr/include (co trzeba robić zaskakująco regularnie).
