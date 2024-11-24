#!/bin/bash
as syscall-mem.S -o syscall-mem.o
ld syscall-mem.o -o syscall-mem
./syscall-mem