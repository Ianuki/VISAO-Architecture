TOKENS_TABLE = {
    "nop": {"bin": "0000", "arg_type":"reg"},
    "and": {"bin": "0001", "arg_type":"reg"},
    "or": {"bin": "0010", "arg_type":"reg"},
    "nand": {"bin": "0011", "arg_type":"reg"},
    "nor": {"bin": "0100", "arg_type":"reg"},
    "xor": {"bin": "0101", "arg_type":"reg"},
    "add": {"bin": "0110", "arg_type":"reg"},
    "ls": {"bin": "0111", "arg_type":"reg"},
    "sta": {"bin": "1000", "arg_type":"val"},
    "lda": {"bin": "1001", "arg_type":"reg"},
    "stb": {"bin": "1010", "arg_type":"val"},
    "ldb": {"bin": "1011", "arg_type":"reg"},
}

REGISTERS_TABLE = {
    "r0": "0000",
    "r1": "0001",
    "r2": "0010",
    "r3": "0011",
    "r4": "0100",
}

def assemble(source):
    lines = source.split("\n")
    output = ""

    for line in lines:
        words = line.split(" ")

        if len(words) >= 2:
            instruction = words[0]
            param = words[1]

            if not instruction in TOKENS_TABLE:
                print("\nUnknown instruction: ", instruction)
                return 

            output += TOKENS_TABLE[instruction]["bin"] + " "

            if TOKENS_TABLE[instruction]["arg_type"] == "reg":
                if not param in REGISTERS_TABLE:
                    print("\nUknown register: ", param)
                    return
                
                output += REGISTERS_TABLE[param] + " "
            elif TOKENS_TABLE[instruction]["arg_type"] == "val":
                if not param.isdigit():
                    print("\nValue parameter is not a number: ", param)
                    return
                
                output += format(int(param), '04b') + " "
    
    data = "hello world"

    with open("o.bisao", "w") as file:
        file.write(output)

import sys

source_code = None

if len(sys.argv) < 2:
    print("No file provided.")
else:
    with open(sys.argv[1], "r") as file:
        source_code = file.read()

    assemble(source_code)