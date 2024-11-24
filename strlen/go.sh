#!/bin/bash
#gcc -Wall -Wextra -g -o functions-asm test.c functions-asm.S
gcc -Wall -Wextra -o functions-asm test.c functions-asm.S
./functions-asm