RA = 0
RB = 0
zero_flag = True

registers = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0
}

jump = False
halt = False
pc = 0

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
def op_nop(null):
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
    global zero_flag

    result = RA + RB
    if result == 0:
        zero_flag = True
    else:
        zero_flag = False

    write_register(register, result)

def op_rsh(register):
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

def op_jnz(value):
    if zero_flag == False:
        global jump
        global pc
        pc = value
        jump = True

def op_hlt(null):
    global halt
    halt = True

def op_sub(register):
    global zero_flag

    result = RA - RB
    if result == 0:
        zero_flag = True
    else:
        zero_flag = False

    write_register(register, result)

def op_out(register):
    print(registers[register])

def op_stm(value):
    pass

def op_ldm(register):
    pass

instructions = {
    0: op_nop,
    1: op_hlt,
    2: op_sta,
    3: op_lda,
    4: op_stb,
    5: op_ldb,
    6: op_and,
    7: op_or,
    8: op_nor,
    9: op_rsh,
    10: op_add,
    11: op_sub,
    12: op_jnz,
    13: op_out,
    14: op_stm,
    15: op_ldm
}

def execute(bin, filename):
    global pc
    global halt
    global jump

    words = [w for w in bin.split(" ") if w != ""]
    pc = 0

    while not halt:
        instructions[int(words[pc * 2], 2)](int(words[pc * 2 + 1], 2))
        
        if jump:
            jump = False
        else:
            pc += 1

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
    
