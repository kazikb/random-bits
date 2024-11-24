#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Kazimierz Biskup
# https://github.com/kazikb/random-bits
#
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name

code = [
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

class SimpleEmulator:
    def __init__(self) -> None:
        self.registers = {
            "RSI": 0x0,
            "RBX": 0x0,
            "RDI": 0x0,
            "RCX": 0x0,
            "RDX": 0x0,
            "RAX": 0x0
        }

    def op_mov(self, dest, src) -> None:
        self.registers[dest] = int(src, 16)

    def op_xor(self, dest, src) -> None:
        self.registers[dest] ^= int(src, 16)

    def get_registers_hex(self, reg) -> str:
        return hex(self.registers[reg])

if __name__ == "__main__":
    emulator = SimpleEmulator()
    for inst in code:
        operation, register, value = inst
        if operation == "MOV":
            emulator.op_mov(register, value)
        elif operation == "XOR":
            emulator.op_xor(register, value)
        else:
            print(f"Instruction [{operation}] not implemented")

    for key, value in emulator.registers.items():
        print(f"Register: {key} val: {value:016x}")
        print(f"Debug Register: {key} val: {hex(value)}")

    # RAX RBX RCX RDX RSI RDI
    registers_to_read = ["RAX", "RBX", "RCX", "RDX", "RSI", "RDI"]
    out_hex = ''.join(f'{emulator.registers[i]:016x}' for i in registers_to_read)
    print(f"\nHex value: {out_hex}")

    try:
        decode_text = bytes.fromhex(out_hex).decode("utf-8")
        print(f"Decoded text: {decode_text}")
    except UnicodeDecodeError:
        print("Failed to decode as UTF-8.")

    out_hex = "".join(hex(emulator.registers[i]).lstrip('0x') for i in registers_to_read)
    print(f"Debug value: {out_hex}")

    try:
        decode_text = bytes.fromhex(out_hex).decode("utf-8")
        print(f"Debug decoded text: {decode_text}")
    except UnicodeDecodeError:
        print("Failed to decode as UTF-8.")

# Decoded text: HexA{EmuIsABirdThatKnowsCPUsReallyWell...IThink}
