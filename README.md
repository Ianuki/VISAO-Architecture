# VISAO Architecture

The VISAO CPU Architecture was created as a simple, fast and minimalistic 
CPU design for survival Minecraft Servers.

## Programming guide:

### Basic operations

Before doing any operation, you must set the value of RA and RB.
STA and STB set their respective registers to a literal number.
LDA and LDB sets them to the value stored in another indexable register.

```
sta 6    ; Set RA to 6
stb 7    ; Set RB to 7
add r1   ; Add RA and RB and store it in R1
out r1   ; Send the value stored in R1 to the standard output
hlt      ; Halt the program counter
```

### Labels

Labels are declared in their own lines and represent the numerical position of the next instruction.
You can jump back to labels using JNZ, JZ or JMP. JNZ and JZ operate using the zero flag.
Indentation is not required but hels with readability.

```
sta 10            ; Set RA to 10
stb 1             ; Set RB to 1

.counting         ; Declare label "counting"
  sub r1          ; Subtract RB from RA and store it in R1
  jnz counting    ; Jump back to counting if the ZF = 1

hlt               ; Halt the program counter
```

## Instruction set:

```
NOP (0000) -> Null
HLT (0001) -> Null
STA (0010) -> Literal
LDA (0011) -> Register
STB (0100) -> Literal
LDB (0101) -> Register
AND (0110) -> Register
ORR (0111) -> Register
NOR (1000) -> Register
RSH (1001) -> Register
ADD (1010) -> Register
SUB (1011) -> Register
JMP (1100) -> Literal
JPZ (1101) -> Literal
STM (1110) -> Literal
LDM (1111) -> Register
```

## Registers:

```
RA -> Input A
RB -> Input B
R0 -> Reads zero
R1 -> Free to use
R2 -> Free to use
R3 -> Free to use
R4 -> Free to use
R5 -> Free to use
```
