Zadanie będące częścią kursu https://sklep.securitum.pl/wstep-do-inzynierii-wstecznej-i-asemblera

Funkcja strlen z języka C otrzymuje adres w pamięci, gdzie znajduje się jakiś tekst. Na końcu tego tekstu jest bajt zerowy, tj. bajt o wartości 0. Funkcja ta liczy ile bajtów ma tekst do pojawienia się pierwszego bajtu zerowego, po czym zwraca tę wartość (tj. de facto zwraca długość tekstu w kodowaniu ASCIIZ, i.e. ASCII Zero-terminated).

Zaimplementuj swoją wersję tej funkcji – my_strlen – w asemblerze.

Napisz program w C, który przetestuje tę funkcję – np. manualnie ją wywołaj dla kilku różnych stringów i porównaj to co funkcja zwraca z tym co zwróci prawdziwa funkcja strlen.

Reimplementacja standardowych funkcji standardowej biblioteki języka jest ogólnie bardzo dobrym ćwiczeniem programistycznym. Co za tym idzie, chętnych zachęcam również do zaimplementowania i przetestowania kilku innych funkcji:

1. atoi (konwersja liczby zapisanej tekstowo na jej wartość)

2. puts (wypisanie napisu na standardowe wyjście, a potem wypisanie jeszcze znaku końca linii)

3. strcpy (kopiowanie stringów; można to załatwić bardzo bardzo prosto w asemblerze)

4. memset (ustawianie wszystkich bajtów w obszarze pamięci na daną wartość)
