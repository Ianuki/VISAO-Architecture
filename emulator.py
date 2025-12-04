RA = 0
RB = 0
R0 = 0 # Read only

registers = {
    1: 0,
    2: 0,
    3: 0,
    4: 0
}

halt = False

def write_register(register, value):
    if not register in registers:
        print("Segmentation fault.")
        halt = True
    else:
        registers[register] = value

def read_register(register):
    if not register in registers:
        print("Segmentation fault.")
        halt = True
    else:
        return registers[register]

# Instructions
def op_nop(scrap):
    pass

def op_sta(value):
    global RA
    RA = value

def op_stb(value):
    global RB
    RB = value

def op_lda(register):
    global RA
    RA = read_register(register)

def op_ldb(register):
    global RB
    RB = read_register(register)

def op_add(register):
    write_register(register, RA + RB)

def op_ls(register):
    write_register(register, (RA << 1) & 0b1111)
    
def op_and(register):
    write_register(register, RA & RB)

def op_or(register):
    write_register(register, RA | RB)

def op_nand(register):
    write_register(register, (~(RA & RB)) & 0b1111)

def op_nor(register):
    write_register(register, (~(RA | RB)) & 0b1111)

def op_xor(register):
    write_register(register, RA ^ RB)

instructions = {
    0: op_nop,
    8: op_sta,
    9: op_lda,
    10: op_stb,
    11: op_ldb,
    6: op_add,
    7: op_ls,
    1: op_and,
    2: op_or,
    3: op_nand,
    4: op_nor,
    5: op_xor
}

def execute(bin, filename):
    words = bin.split(" ")

    for word_i in range(len(words) // 2):
        instructions[int(words[word_i * 2], 2)](int(words[word_i * 2 + 1], 2))

    with open(filename + ".visaolog", "w") as file:
        file.write(f"R1: {registers[1]}\nR2: {registers[2]}")

import sys

bin = None

if len(sys.argv) < 2:
    print("No file provided.")
else:
    with open(sys.argv[1], "r") as file:
        bin = file.read()

    execute(bin, sys.argv[1])

