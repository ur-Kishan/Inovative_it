"""Reference functional simulator for a 4-bit ALU.

Operations (select S2S1S0):
000 ADD, 001 SUB, 010 AND, 011 OR,
100 XOR, 101 NOT A, 110 INC A, 111 PASS B.

Flags:
Z = 1 when result is zero; N = result bit 3.
For ADD, C is carry-out; for SUB, C=1 means no borrow.
For INC, C is carry-out. For logic/PASS operations C=0.
V is signed two's-complement overflow for ADD/SUB/INC; otherwise 0.
All results are restricted to four bits.
"""
from dataclasses import dataclass
from typing import Dict, Iterable, Tuple

MASK = 0xF

OPCODES = {
    0b000: "ADD",
    0b001: "SUB",
    0b010: "AND",
    0b011: "OR",
    0b100: "XOR",
    0b101: "NOT_A",
    0b110: "INC_A",
    0b111: "PASS_B",
}

@dataclass(frozen=True)
class ALUResult:
    value: int
    Z: int
    C: int
    N: int
    V: int

    def bits(self) -> str:
        return f"{self.value:04b}"

    def flags(self) -> str:
        return f"Z={self.Z} C={self.C} N={self.N} V={self.V}"


def _signed4(value: int) -> int:
    value &= MASK
    return value - 16 if value & 0b1000 else value


def execute(a: int, b: int, sel: int) -> ALUResult:
    """Execute one ALU operation for 4-bit unsigned inputs."""
    if not (0 <= a <= MASK and 0 <= b <= MASK):
        raise ValueError("A and B must be integers in the range 0..15")
    if sel not in OPCODES:
        raise ValueError("sel must be a 3-bit opcode from 0 to 7")

    c = 0
    v = 0
    if sel == 0b000:  # ADD
        full = a + b
        result = full & MASK
        c = (full >> 4) & 1
        v = int((~(a ^ b) & (a ^ result) & 0b1000) != 0)
    elif sel == 0b001:  # SUB: A + two's complement of B
        result = (a - b) & MASK
        c = int(a >= b)  # Carry convention: 1 means no borrow.
        v = int(((a ^ b) & (a ^ result) & 0b1000) != 0)
    elif sel == 0b010:
        result = a & b
    elif sel == 0b011:
        result = a | b
    elif sel == 0b100:
        result = a ^ b
    elif sel == 0b101:
        result = (~a) & MASK
    elif sel == 0b110:
        full = a + 1
        result = full & MASK
        c = (full >> 4) & 1
        v = int(a == 0b0111)
    else:  # PASS_B
        result = b

    result &= MASK
    z = int(result == 0)
    n = (result >> 3) & 1
    return ALUResult(result, z, c, n, v)


def self_test() -> Tuple[int, int]:
    """Exhaustively verify all 4-bit input combinations for each opcode."""
    checks = 0
    for a in range(16):
        for b in range(16):
            for sel in range(8):
                got = execute(a, b, sel)
                if sel == 0:
                    expected = (a + b) & MASK
                    expected_c = int(a + b > MASK)
                    expected_v = int(not (-8 <= _signed4(a) + _signed4(b) <= 7))
                elif sel == 1:
                    expected = (a - b) & MASK
                    expected_c = int(a >= b)
                    expected_v = int(not -8 <= _signed4(a) - _signed4(b) <= 7)
                elif sel == 2:
                    expected, expected_c, expected_v = a & b, 0, 0
                elif sel == 3:
                    expected, expected_c, expected_v = a | b, 0, 0
                elif sel == 4:
                    expected, expected_c, expected_v = a ^ b, 0, 0
                elif sel == 5:
                    expected, expected_c, expected_v = (~a) & MASK, 0, 0
                elif sel == 6:
                    expected = (a + 1) & MASK
                    expected_c = int(a == MASK)
                    expected_v = int(a == 0b0111)
                else:
                    expected, expected_c, expected_v = b, 0, 0
                assert got.value == expected, (a, b, sel, got, expected)
                assert got.C == expected_c, (a, b, sel, got, expected_c)
                assert got.V == expected_v, (a, b, sel, got, expected_v)
                assert got.Z == int(expected == 0)
                assert got.N == ((expected >> 3) & 1)
                checks += 1
    return checks, 16 * 16 * 8


def demo() -> None:
    a, b = 0b0101, 0b0011
    print(f"Inputs: A={a:04b} (5), B={b:04b} (3)")
    print("SEL  OP      RESULT  FLAGS")
    for sel, name in OPCODES.items():
        out = execute(a, b, sel)
        print(f"{sel:03b}  {name:<7} {out.bits()}   {out.flags()}")
    checks, total = self_test()
    print(f"\nSELF-TEST: PASS - {checks}/{total} exhaustive opcode/input checks")

if __name__ == "__main__":
    demo()
