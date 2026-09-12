#!/usr/bin/env python3
"""
Generate null-free push instructions to build a string on the stack.

For chunks containing null bytes, the XOR method is used:
    mov reg, chunk ^ key
    xor reg, key
    push reg

Both `key` and `chunk ^ key` are guaranteed to be null-free, so the
resulting instruction bytes contain no 0x00.
"""

VALID_REGISTERS = {'eax', 'ebx', 'ecx', 'edx', 'esi', 'edi', 'ebp', 'esp'}

# Preferred XOR keys, tried in order.  All of these are null-free.
PREFERRED_KEYS = [
    0x11111111, 0x12121212, 0x13131313, 0x14141414,
    0x15151515, 0x16161616, 0x17171717, 0x18181818,
    0x19191919, 0x1A1A1A1A, 0x1B1B1B1B, 0x1C1C1C1C,
    0x1D1D1D1D, 0x1E1E1E1E, 0x1F1F1F1F, 0x20202020,
    0x21212121, 0x22222222, 0x23232323, 0x24242424,
    0x01010101, 0x02020202, 0x03030303, 0x04040404,
    0x05050505, 0x06060606, 0x07070707, 0x08080808,
    0x09090909, 0x0A0A0A0A, 0x0B0B0B0B, 0x0C0C0C0C,
    0x0D0D0D0D, 0x0E0E0E0E, 0x0F0F0F0F, 0x10101010,
]


def choose_key(chunk_bytes):
    """
    Return a 4-byte null-free key such that neither the key itself
    nor (chunk ^ key) contains a null byte.
    """
    chunk_val = int.from_bytes(chunk_bytes, 'little')

    for key_val in PREFERRED_KEYS:
        key_bytes = key_val.to_bytes(4, 'little')
        if b'\x00' in key_bytes:
            continue
        result = (chunk_val ^ key_val).to_bytes(4, 'little')
        if b'\x00' in result:
            continue
        return key_bytes

    # Fallback (always works): per-byte key of (c+1) mod 256, with 0xFF -> 0x01.
    def next_byte(c):
        nxt = (c + 1) & 0xFF
        return nxt if nxt != 0 else 0x01

    key_bytes = bytes(next_byte(c) for c in chunk_bytes)
    result = bytes(a ^ b for a, b in zip(chunk_bytes, key_bytes))
    assert b'\x00' not in key_bytes and b'\x00' not in result, "fallback failed"
    return key_bytes


def gen_shellcode_pushes(target_string, register='esi'):
    if register not in VALID_REGISTERS:
        raise ValueError(f"Unknown register: {register}")

    # Encode string + NUL terminator, then pad to a multiple of 4
    byte_string = target_string.encode('utf-8') + b'\x00'
    while len(byte_string) % 4 != 0:
        byte_string += b'\x00'

    # Split into 4-byte chunks; the *last* chunk must be pushed first.
    chunks = [byte_string[i:i + 4] for i in range(0, len(byte_string), 4)]
    chunks.reverse()

    lines = []
    for chunk in chunks:
        chunk_val = int.from_bytes(chunk, 'little')

        if b'\x00' not in chunk:
            # Plain push, 5 bytes: 68 xx xx xx xx
            lines.append(f"    push 0x{chunk_val:08X}")
        else:
            # XOR bypass, 12 bytes total
            key = choose_key(chunk)
            key_val = int.from_bytes(key, 'little')
            loaded_val = chunk_val ^ key_val

            lines.append(f"    ; {chunk!r} contains null byte(s) -> XOR bypass\n")
            lines.append(f"    mov {register}, 0x{loaded_val:08X}")
            lines.append(f"    xor {register}, 0x{key_val:08X}")
            lines.append(f"    push {register}")

    return "\n".join(lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate null-free push instructions for a string."
    )
    parser.add_argument("string", nargs="?", help="String to push (prompted if omitted)")
    parser.add_argument(
        "-r", "--register", default="esi", choices=sorted(VALID_REGISTERS),
        help="Register to use for the XOR bypass (default: esi)",
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true",
        help="Only print the assembly, no header comment.",
    )
    args = parser.parse_args()

    target = args.string if args.string is not None else input("String to push: ")

    if not args.quiet:
        print(f"; Null-free pushes for {target!r} (register: {args.register})")
        print("; NOTE: this code clobbers the chosen register and the stack.")
    print(gen_shellcode_pushes(target, args.register),"\n")