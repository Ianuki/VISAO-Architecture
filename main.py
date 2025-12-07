TOKENS_TABLE = {
    "nop": {"bin": "0000", "arg_type":"null"},
    "hlt": {"bin": "0001", "arg_type":"null"},
    "sta": {"bin": "0010", "arg_type":"val"},
    "lda": {"bin": "0011", "arg_type":"reg"},
    "stb": {"bin": "0100", "arg_type":"val"},
    "ldb": {"bin": "0101", "arg_type":"reg"},
    "and": {"bin": "0110", "arg_type":"reg"},
    "orr": {"bin": "0111", "arg_type":"reg"},
    "nor": {"bin": "1000", "arg_type":"reg"},
    "rsh": {"bin": "1001", "arg_type":"reg"},
    "add": {"bin": "1010", "arg_type":"reg"},
    "sub": {"bin": "1011", "arg_type":"reg"},
    "jnz": {"bin": "1100", "arg_type":"val"},
    "out": {"bin": "1101", "arg_type":"reg"},
    "stm": {"bin": "1110", "arg_type":"val"},
    "ldm": {"bin": "1111", "arg_type":"reg"}
}

REGISTERS_TABLE = {
    "r0": "0000",
    "r1": "0001",
    "r2": "0010",
    "r3": "0011",
    "r4": "0100",
}

def assemble(source, filename):
    lines = source.split("\n")
    line_count = 0
    output = ""
    labels = {}

    for line in lines:
        if len(line) > 0:
            if line[0] == ";":
                continue

        line = line.lstrip()
        words = line.split(" ")

        if len(words) >= 1 and words[0] != "":
            instruction = words[0]      

            if instruction.startswith("."):
                name = line[1:]
                name = name.rstrip()
                labels[name] = line_count 
                continue

            if not instruction in TOKENS_TABLE:
                print("\nUnknown instruction: ", instruction)
                return 

            output += TOKENS_TABLE[instruction]["bin"] + " "
            line_count += 1

            if TOKENS_TABLE[instruction]["arg_type"] == "null":

                output += "0000 "
                continue

            if TOKENS_TABLE[instruction]["arg_type"] == "reg":
                param = words[1]

                if not param in REGISTERS_TABLE:
                    print("\nUknown register: ", param)
                    return
                
                output += REGISTERS_TABLE[param] + " "
            elif TOKENS_TABLE[instruction]["arg_type"] == "val":
                param = words[1]
                
                if instruction == "jnz" and not param.isdigit():
                    if not param in labels:
                        print(f"Label {param} does not exist")
                        return

                    param = labels[param]
                else:
                    if not param.isdigit():
                        print("\nValue parameter is not a number: ", param)
                        return
                
                output += format(int(param), '04b') + " "
    
    data = "hello world"

    with open(filename + ".bisao", "w") as file:
        file.write(output)

import sys

source_code = None

if len(sys.argv) < 3:
    print("Missing arguments.")
else:
    with open(sys.argv[1], "r") as file:
        source_code = file.read()

    assemble(source_code, sys.argv[2])
