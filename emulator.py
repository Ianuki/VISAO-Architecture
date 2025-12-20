import sys
import threading
import time
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

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

ram = [0] * 256

jump = False
halt = False
pc = 0

def write_register(register, value):
    if not register in registers:
        halt = True
    else:
        if register > 0:
            registers[register] = value & 0xFF

def read_register(register):
    if not register in registers:
        halt = True
    else:
        return registers[register] & 0xFF

# Instructions
def op_nop(null):
    pass

def op_sta(value):
    global RA
    RA = value & 0xFF

def op_stb(value):
    global RB
    RB = value & 0xFF

def op_lda(register):
    global RA
    RA = read_register(register) & 0xFF

def op_ldb(register):
    global RB
    RB = read_register(register) & 0xFF

def op_add(register):
    global zero_flag

    result = (RA + RB) & 0xFF
    if result == 0:
        zero_flag = True
    else:
        zero_flag = False

    write_register(register, result)

def op_rsh(register):
    write_register(register, (RA << 1) & 0b1111)
    
def op_and(register):
    write_register(register, (RA & RB) & 0xFF)

def op_or(register):
    write_register(register, (RA | RB) & 0xFF)

def op_nand(register):
    write_register(register, (~(RA & RB)) & 0b1111)

def op_nor(register):
    write_register(register, (~(RA | RB)) & 0b1111)

def op_xor(register):
    write_register(register, (RA ^ RB) & 0xFF)

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

    result = (RA - RB) & 0xFF
    if result == 0:
        zero_flag = True
    else:
        zero_flag = False

    write_register(register, result)

def op_jez(value):
    if zero_flag == True:
        global jump
        global pc
        pc = value
        jump = True
        

def op_stm(register):
    ram[RA] = registers[register] & 0xFF

    pass

def op_ldm(register):
    write_register(register, ram[RA])

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
    9: op_xor,
    10: op_add,
    11: op_sub,
    12: op_jnz,
    13: op_jez,
    14: op_stm,
    15: op_ldm
}

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def execute(bin, filename):
    global pc
    global halt
    global jump

    words = [w for w in bin.split(" ") if w != ""]
    pc = 0
    total_executed = 0
    goal = 0
    finish = False

    print(f"{len(words)} instructions.")

    while not halt:
        if total_executed == goal:
            goal += int(input(" >>> "))
        elif goal < 0:
            finish = True

        instructions[int(words[pc * 2], 2)](int(words[pc * 2 + 1], 2))

        if jump:
            jump = False
        else:
            if total_executed < goal or finish:
                pc += 1
                total_executed += 1

        time.sleep(0.001)


pygame.init()

NODES_X = 20
NODES_Y = 10
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 200
NODE_WIDTH = int(SCREEN_WIDTH / NODES_X)
NODE_HEIGHT = int(SCREEN_HEIGHT / NODES_Y)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Emulator")

bin = None

if len(sys.argv) < 2:
    print("No file provided.")
else:
    with open(sys.argv[1], "r") as file:
        bin = file.read()

    print("STARTING EMULATION")

    execute_thread = threading.Thread(target=execute, args=(bin, sys.argv[1]), daemon=True)
    execute_thread.start()

    last_x = ram[87]
    last_y = ram[88]
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        if ram[89] > 0:
            last_x = ram[87]
            last_y = ram[88]
            ram[89] = 0

        rect = pygame.Rect(last_x * NODE_WIDTH, last_y * NODE_HEIGHT, NODE_WIDTH, NODE_HEIGHT)
        pygame.draw.rect(screen, WHITE, rect)

        pygame.display.update()

    with open(sys.argv[1] + ".visaolog", "w") as file:
        file.write(f"RA: {RA}\n")
        file.write(f"RB: {RB}\n")
        file.write(f"Program Counter: {pc}\n")

        file.write("\nRegisters:\n")
        for register in range(len(registers)):
            file.write(f"\t{register}: {registers[register]}\n")

        file.write("\nRAM:\n")
        for mem in range(len(ram)):
            file.write(f"\t{mem}: {ram[mem]}\n")

    pygame.quit()
    sys.exit()
    
