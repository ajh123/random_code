# Instructions

## Bit layout

```
0 --- 3 4 ------------------ 15
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
^^^^^^^ ^^^^^^^^^^^^^^^^^^^^^^^
Opcode        Operands
```

## Opcodes

| Opcode | Name                 | Code   | Operands (**\*1**)                              | Notes                       |
| ------ | -------------------- | ------ | ----------------------------------------------- | --------------------------- |
| `0000` | No Operation         | `NOP`  | Not applicable                                  |                             |
| `0001` |
| `0010` |
| `0011` |
| `0100` |
| `0101` | Add                  | `ADD`  | Bits 0 - 2 = first reg, bits 3 - 5 = second reg | First reg updates to result |
| `0110` | Subtract             | `SUB`  | Bits 0 - 2 = first reg, bits 3 - 5 = second reg | First reg updates to result |
| `0111` | AND                  | `AND`  | Bits 0 - 2 = first reg, bits 3 - 5 = second reg | First reg updates to result |
| `1000` | OR                   | `OR`   | Bits 0 - 2 = first reg, bits 3 - 5 = second reg | First reg updates to result |
| `1001` | XOR                  | `XOR`  | Bits 0 - 2 = first reg, bits 3 - 5 = second reg | First reg updates to result |
| `1010` | NOT                  | `NOT`  | Bits 0 - 2 = register to invert                 | Register will be overridden |
| `1011` |
| `1100` |
| `1101` |
| `1110` |
| `1111` | Halt                 | `HLT`  | Not applicable                                  |                             |

> **\*1:** "Bits" means the bits used by the operands only, bits used by the opcode are ignored.
> So "Bits 0 - 2" means "Bits 4 - 6" of the whole instruction.