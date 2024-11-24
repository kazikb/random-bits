/*
    Kazimierz Biskup
    https://github.com/kazikb/random-bits
*/
.intel_syntax noprefix

.data
  new_line: .string "\n"  /* string zawierajacy znak nowej linii na potrzeby my_puts_in_asm() */

.section .note.GNU-stack,"",@progbits

.text

.global my_strln_in_asm
my_strln_in_asm:
  /*
   *  RDI char PTR  - pointer do poczatku stringa
   *  RAX           - return liczba znakow
   */
  push rbp
  mov rbp, rsp

  xor rax, rax

  petla_strln:
    /* można to na 2 sposoby rozwiązać */
    /*
        lea rsi, BYTE PTR [rdi + rax]
        movzx rbx, BYTE PTR [rsi]
    */
    movzx rbx, BYTE PTR [rdi]

    cmp rbx, 0x0      /* sprawdzamy czy byte jaki znajduje się w rbx jext NULL
                       * terminated string
                       */
    je end_strln
    inc rax
    inc rdi           /* przesuwamy BYTE PTR na kolejny znak */
    jmp petla_strln

  end_strln:
    /* zwracamy w RAX liczbe znakow */
    mov rsp, rbp
    pop rbp
    ret

.global my_atoi_in_asm
my_atoi_in_asm:
  /*
   *  RDI char PTR  - pointer do poczatku stringa z int
   *  RAX           - return liczba znakow
   */
  push rbp
  mov rbp, rsp

  xor rax, rax   /* res */

  petla_atoi:
    movzx rbx, BYTE PTR [rdi]  /* załadowanie jednego BYTE z lokalizacji na ktora
                                * wskazuje adres przekazany jako PTR w
                                * rejestrze RDI
                                */

    /* sprawdzamy czy byte jaki znajduje się w rbx jext NULL terminated string
     * while (c[i] != '\0')
     */
    cmp rbx, 0x0
    je end_atoi

    /* sprawdzamy czy znak ASCII w rejestrze RBX jest z zakresu 0..9
     * bo tylko takie mozna skonwertowac na int
     * if (c[i] >= 0x30 && c[i] <= 0x39)
     */
    cmp rbx, 0x30   /* ASCII '0' */
    jl set_error
    cmp rbx, 0x39   /* ASCII '9' */
    jg set_error

    /* res = res * 10 + (c[i] - 0x30) */
    imul rax, 0xa   /* przesuwamy 10 o jedna pozycje w lewo */
    sub rbx, 0x30   /* znak "0" ASCII jest przesunięty o 48 dec względem int = 0 */
    add rax, rbx

    inc rdi           /* przesuwamy BYTE PTR na kolejny znak */
    jmp petla_atoi

  /* Ustawiam return value na 0 w momencie jak znak nie jest z przedzialu 0..9
   * nastepnie wychodze z funkcji
   */
  set_error:
    xor rax, rax
    jmp end_atoi

  end_atoi:
    /* zwracamy w RAX skonwertowany int */
    mov rsp, rbp
    pop rbp
    ret

.global my_puts_in_asm
my_puts_in_asm:
  /*
   *  RDI char PTR  - pointer do poczatku stringa z int
   *  RAX           - return liczba znakow
   */
  push rbp
  mov rbp, rsp
  sub rsp, 8        /* na stosie tworze zmienna ktora bedzie przechowywac wskaznik
                     * przekazany w momencie wywolania funkcji w rejestrze RDI
                     */

  mov [rbp-8], rdi      /* odkladam na stos wartosc rejestru RDI */
  call my_strln_in_asm  /* sprawdzamy długosc stringa jaki ma zostac wyswietlony
                         * na ekranie a wartosc z wywolania my_strln_in_asm
                         * bedzie zwrocona w RAX
                         */
  mov rdx, rax          /* Param. syscall write size_t */
  mov rsi, [rbp-8]      /* Param. syscall write char PTR */
  mov rdi, 0x1          /* Param. syscall write fd */
  mov rax, 0x1          /* syscall write() */
  syscall

  /* wyswietlam znak nowej linii */
  mov rdx, 0x1                /* Param. syscall write size_t */
  lea rsi, [rip + new_line]   /* Note the rip+ relative addressing! - potrzebuje PTR */
  mov rdi, 0x1                /* Param. syscall write fd */
  mov rax, 0x1                /* syscall write() */
  syscall

  end_puts:
    /* zwracamy w RAX status wykonania funkcji */
    mov rsp, rbp
    pop rbp
    ret

.global my_strcpy_in_asm
my_strcpy_in_asm:
  /*
   *  RDI char PTR  - pointer do poczatku docelowego stringa
   *  RSI char PTR  - pointer do poczatku zrodlowego stringa
   *  RAX           - pointer do poczatku docelowego stringa
   */
  push rbp
  mov rbp, rsp

  mov rax, rdi
  xor rdx, rdx

  petla_strcpy:
    movzx rdx, BYTE PTR [rsi] /* odpowiednik z C dereferencji PTR czyli rdx = *rsi */
    cmp rdx, 0x0
    je end_strcpy
    mov [rdi], rdx            /* odpowiednik z C dereferencji PTR *rdi = rdx */
    inc rsi
    inc rdi
    jmp petla_strcpy

  end_strcpy:
    /* zwracamy w RAX poczatek docelowego stringa */
    mov rsp, rbp
    pop rbp
    ret

.global my_memset_in_asm
my_memset_in_asm:
  /*
   *  RDI void PTR  - pointer do poczatku obszaru pamieci
   *  RSI int       - kod ASCII znaku jaki ma byc wstawiony
   *  RDX int       - liczba znakow jaka ma byc wstawiona
   *  RAX           - pointer do poczatku docelowego stringa
   */
  push rbp
  mov rbp, rsp

  mov rax, rdi              /* zapisuje poczatek modyfikowanego obszaru pamieci do RAX */

  petla_memset:
    cmp rdx, 0x0
    je end_memset
    mov BYTE PTR [rdi], sil   /* biore dolne 8 bitow rejestru RAX (znak ASCII ma
                               * 8 bitow) i zapisuje je w obszarze pamieci na
                               * jaki wskazuje RDI poprzez dereferencje
                               * BYTE PTR RDI -> *rdi = sil
                               */
    inc rdi
    dec rdx
    jmp petla_memset

  end_memset:
    mov rsp, rbp
    pop rbp
    ret
