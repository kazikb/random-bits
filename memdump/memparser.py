#!/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
#
# Kazimierz Biskup
# https://github.com/kazikb/random-bits
#
import sys
import os

def dump_proc_info(procid) -> dict:
    procinfo = {
        "pid": procid,
        "pathname_list": [],
        "pages": [],
        "mem_total": 0
    }
    maps_file = f"/proc/{procid}/maps"

    if not os.path.exists(maps_file):
        raise FileNotFoundError(f"Missing file: {maps_file}")

    with open(maps_file, "r", encoding="utf-8") as proc_maps:
        for line in proc_maps.readlines():
            line = line.split()
            if len(line) == 6 and not line[5].startswith("["):
                procinfo["pathname_list"].append(line[5])

            procinfo["pages"].append(line)
            start, end = line[0].split("-")
            procinfo["mem_total"] = procinfo["mem_total"] \
                                    + (int(end, 16) - int(start, 16))

    return procinfo


def print_proc_info(procinfo) -> None:
    procinfo["mem_total"] = procinfo["mem_total"] / (1024 ** 2)
    print(f"Process total memory: {procinfo['mem_total']:.2f} MB\n")

    print("Process writable pages:")
    print(f"{'[address]':<30}{'[perms]':<8}{'[offset]':<10}[pathname]")
    for page in procinfo["pages"]:
        if not "w" in page[1]:
            continue
        if len(page) == 6:
            print(f"{page[0]:<30}{page[1]:<8}{page[2]:<10}{page[5]}")
        else:
            print(f"{page[0]:<30}{page[1]:<8}{page[2]:<10}")

    print("\nList of library used by process:\n")
    uniq = set(procinfo["pathname_list"])
    for lib in uniq:
        print(lib)


def dump_proc_mem(procinfo, path) -> None:
    f_mem = f"/proc/{procinfo['pid']}/mem"
    print(f"Dumping process memory regions: {f_mem} to: {path}")

    for page in procinfo["pages"]:
        start, end = page[0].split("-")
        start = int(start, 16)
        end = int(end, 16)
        size = end - start
        f_name = f"{hex(start)}_{size}_{page[1]}.bin"
        dump_path = os.path.join(path, f_name)
        print(dump_path)

        with open(f_mem, mode="rb") as mem:
            try:
                mem.seek(start)
                data = mem.read(size)
            except OSError as e:
                print(f"Cannot dump memory region: {page}\n{e}")
                continue
            except ValueError as e:
                print(f"Cannot dump memory region: {page}\n{e}")
                continue

        with open(dump_path, mode="wb") as dump_mem:
            dump_mem.write(data)


def help_func():
    print("Get process information")
    print(f"\t{sys.argv[0]} -i [PID]")
    print("Dumping process memory regions")
    print(f"\t{sys.argv[0]} -d [PID]")
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        help_func()
    elif sys.argv[1] not in ("-i", "-d"):
        help_func()

    pid = int(sys.argv[2])
    if sys.argv[1] == "-i":
        print_proc_info(dump_proc_info(procid=pid))
    elif sys.argv[1] == "-d":
        dump_dir = os.path.normpath(os.path.dirname(__file__))
        dump_dir = os.path.join(dump_dir, str(pid))
        if not os.path.exists(dump_dir):
            os.mkdir(dump_dir)
        dump_proc_mem(dump_proc_info(procid=pid), dump_dir)
