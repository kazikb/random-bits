/*
    Kazimierz Biskup
    https://github.com/kazikb/random-bits
*/
.intel_syntax noprefix

.data
  /* Tablica z danymi do skopiowania do zaalokowanej dynamicznie pamieci */
  secret_message:
    .8byte 0x7365597b41786548, 0x696854746f474921, 0x6c6c616373795373, 0x4c216b726f576f54, 0x656c654373277465, 0x7d21216574617262 , 0x000000000000000a
  secret_message_size = (. - secret_message) / 8  /* Dynamiczne wyliczenie
                                                   * wielkosci tablicy. Symbol "."
                                                   * oznacza aktualne miejsce w pamieci
                                                   * czyli zaraz po ostatnim elemencie
                                                   * zadeklarowanej wczesniej tablicy.
                                                   * https://sourceware.org/binutils/docs/as/Dot.html
                                                   */

.text
.global _start  /* Eksportuje funkcje start jako punkt wejscia do programu.
                 * Funkcja _start stanowi punkt wejscia (pierwsza wolana funkcja)
                 * zanim zostanie zawołana _libc_start_main() -> _main()
                 */
_start:
  push rbp
  mov rbp, rsp
  sub rsp, 8    /* Miejsce na zmienną z adresem zaalokowanej pamiecie przez
                 * syscall mmap()
                 */
  mov QWORD PTR [rbp-8], 0x0

  /* Wolanie syscall mmap()
   * mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0)
   */
  xor r9, r9                  /* Param. 0 */
  mov r8, 0xffffffffffffffff  /* Param. -1 */
  mov r10, 0x20               /* Param. Flaga MAP_ANONYMOUS */
  or r10, 0x02                /* Param. Flaga MAP_PRIVATE */
  mov edx, 0x1                /* Param. PROT_READ */
  or edx, 0x2                 /* Param. PROT_WRITE */
  mov esi, 0x1000             /* Param. Size 4096 */
  xor edi, edi                /* Param. NULL pointer */
  mov eax, 0x9                /* syscall 9 -> mmap */
  syscall

  cmp rax, 0xffffffffffffffff /* Sprawdzenie czy mmap nie zwrocil -1 */
  je syscall_failed

  mov QWORD PTR [rbp-8], rax  /* Zapisanie nowo zaalokowanego adresu pamieci */

  /* Wczytanie pod zaalokowane miejsce w pamieci 6 wartosci 64 bitowych */
  lea rsi, [secret_message]   /* source dla iteracyjnego kopiowania tablicy przez
                               * instrukcji movsq
                               */
  mov rdi, rax                /* destination dla iteracyjnego kopiowania tablicy
                               * przez instrukcje movsq
                               */
  mov rcx, secret_message_size  /* loop counter */

  insert_value:
    movsq
    loop insert_value

  /* Wyswietlenie zawartosci zaalokowanej pamieci na ekranie poprzez wywolanie
   * syscall write()
   */
   mov r8, secret_message_size  /* loop counter */
   mov edx, 0x8                 /* Param. 8 bytes size */
   mov rsi, QWORD PTR [rbp-8]   /* Param. char buffer pointer */
   mov edi, 0x1                 /* Param. stdout */

   print_value:
    mov eax, 0x1                 /* syscall 1 -> write */
    syscall
    cmp rax, 0xffffffffffffffff  /* Sprawdzenie czy write nie zwrocil -1 */
    je syscall_failed
    add rsi, 8                   /* Przesuniecie pointera na kolejny element */
    dec r8
    cmp r8, 0x1
    jge print_value

  /* Wolanie syscall unmap()
   * munmap(pmemaddr, 0x1000)
   */
  mov esi, 0x1000             /* Param. Size 4096 */
  mov rdi, QWORD PTR [rbp-8]  /* Param. Memory address */
  mov eax, 0xb                /* syscall 11 -> munmap */
  syscall

  xor edi, edi    /* 1 parametr syscall: return code -> 0 */
  mov eax, 0x3c   /* syscall 60 -> exit */
  syscall


  syscall_failed:
    mov rdi, 0x1    /* 1 parametr syscall: return code -> 1 */
    mov rax, 0x3c   /* syscall 60 -> exit */
    syscall
