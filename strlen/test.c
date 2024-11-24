/*
    Kazimierz Biskup
    https://github.com/kazikb/random-bits
*/
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

//     RAX                    RDI
extern int my_strln_in_asm(char *text);

//     RAX                    RDI
extern int my_atoi_in_asm(char *text);

//     RAX                    RDI
extern int my_puts_in_asm(char *text);

//     RAX                    RDI         RSI
extern char *my_strcpy_in_asm(char *dst, char *src);

//     RAX                    RDI         RSI             RDX
extern void *my_memset_in_asm(void *ptr, int ascii_char, int count);

#define NR_LINE_BREAK_COUNT 50

int main(void) {
  // start strlen
  printf("******* strlen *******\n");

  char testStringArray[4][50] = {
    "For the emperor!!!!!",
    "We fight",
    "Alll go well",
    "NULL string\0 is cool"
  };

  for (int i = 0; i < 4; i++) {
    printf("Test string: [%s]\n", testStringArray[i]);
    printf("%-20s %ld\n", "strlen:", strlen(testStringArray[i]));
    printf("%-20s %d\n", "my_strln_in_asm:", my_strln_in_asm(testStringArray[i]));
  }
  for (int i = 0; i < NR_LINE_BREAK_COUNT; i++)
    printf("-");
  printf("\n");
  // end strlen

  // start atoi
  printf("******* atoi *******\n");

  char testAtoiArray[4][50] = {
    "12345",
    "abc",
    "+-a",
    "0xa"
  };

  for (int i = 0; i < 4; i++) {
    printf("Test atoi string: [%s]\n", testAtoiArray[i]);
    printf("%-20s %d\n", "atoi:", atoi(testAtoiArray[i]));
    printf("%-20s %d\n", "my_atoi_in_asm:", my_atoi_in_asm(testAtoiArray[i]));
  }
  for (int i = 0; i < NR_LINE_BREAK_COUNT; i++)
    printf("-");
  printf("\n");
  // end atoi

  // start puts
  printf("******* puts *******\n");

  for (int i = 0; i < 4; i++) {
    printf("Test string: [%s]\n", testStringArray[i]);
    printf("%-20s", "puts: ");
    fflush(stdout);
    puts(testStringArray[i]);
    printf("%-20s", "my_puts_in_asm: ");
    fflush(stdout);
    my_puts_in_asm(testStringArray[i]);
  }
  for (int i = 0; i < NR_LINE_BREAK_COUNT; i++)
    printf("-");
  printf("\n");
  //end puts

  // start strcpy
  printf("******* strcpy *******\n");

  char testStringCopySrc[4][50] = {
    "Ok to bedzie ciekawe",
    "Now what?",
    "Demo stage v82",
    "NULL string\0 is cool"
  };
  char testStringCopyDst[4][50] = { "\0" };
  char testStringCopyDstAsm[4][50] = { "\0" };

  for (int i = 0; i < 4; i++) {
    printf("Test string: [%s]\n", testStringCopySrc[i]);
    printf("%-20s %s\n", "strcp:", strcpy(testStringCopyDst[i], testStringCopySrc[i]));
    printf("%-20s %s\n", "my_strcpy_in_asm:", my_strcpy_in_asm(testStringCopyDstAsm[i], testStringCopySrc[i]));
  }
  for (int i = 0; i < NR_LINE_BREAK_COUNT; i++)
    printf("-");
  printf("\n");
  //end strcpy

  // start memset
  printf("******* memset *******\n");

  char testMemset[4][50] = {
    "Ok to bedzie ciekawe",
    "Now what we can do with?",
    "Demo stage v82",
    "NULL string\0 is cool"
  };
  char testMemsetMy[4][50] = {
    "Ok to bedzie ciekawe",
    "Now what we can do with?",
    "Demo stage v82",
    "NULL string\0 is cool"
  };

  for (int i = 0; i < 4; i++) {
    printf("Test string: [%s]\n", testMemset[i]);
    char *cptr = testMemset[i];
    cptr += 9;
    memset(cptr, '*', 5);
    printf("%-20s %s\n", "memset:", testMemset[i]);

    cptr = testMemsetMy[i];
    cptr += 9;
    my_memset_in_asm(cptr, '-', 5);
    printf("%-20s %s\n", "my_memset_in_asm:", testMemsetMy[i]);
  }
  for (int i = 0; i < NR_LINE_BREAK_COUNT; i++)
    printf("-");
  printf("\n");
  //end memset

  return 0;
}
