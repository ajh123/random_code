# `alu_test.asm`: Simple program to test maths and logic
NOP
LDI R1 100
LDI R2 10
LDI R3 40

ADD R1 R2
SUB R1 R3
AND R2 R1
OR R3 R3
XOR R1 R1
HLT
