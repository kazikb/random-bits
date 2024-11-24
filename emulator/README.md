Zadanie będące częścią kursu https://sklep.securitum.pl/wstep-do-inzynierii-wstecznej-i-asemblera

Minimalny emulator

W dowolnym języku programowania zaimplementuj emulator, który wykona następujący kod (kod jest podany w formie JSON dla uproszczenia).
```
{
  "code":[
      [ "MOV", "RSI", "0x4ab5a1688b3d9111" ],
      [ "MOV", "RBX", "0x82dd9b90edf1ea3c" ],
      [ "MOV", "RDI", "0x102e13ec65df58b7" ],
      [ "MOV", "RCX", "0x65c46b8c751dab6d" ],
      [ "MOV", "RDX", "0xb73661da75bc54f9" ],
      [ "MOV", "RAX", "0x8eb97ffaa25809e6" ],
      [ "XOR", "RBX", "0xcbaedad284838e68" ],
      [ "XOR", "RDI", "0x3e6747840cb133ca" ],
      [ "XOR", "RSI", "0x26ccf60de751bf3f" ],
      [ "XOR", "RDX", "0xf46634a927d93595" ],
      [ "XOR", "RAX", "0xc6dc07bbd91d6493" ],
      [ "XOR", "RCX", "0x0da51fc71b72dc1e" ]
  ]
}
```
Po zakończeniu wykonania wypisz wartości rejestrów w postaci heksadecymalnej bez prefiksów (i bez spacji pomiędzy) w następującej kolejności:

RAX RBX RCX RDX RSI RDI

Następnie zdekoduj tak otrzymany ciąg hexadecymalny (możesz użyć CyberChef albo zrobić to w dowolny inny sposób).