TOKENS_TABLE = {
    "nop": {"bin": "00000000", "arg_type":"null"},
    "hlt": {"bin": "00000001", "arg_type":"null"},
    "sta": {"bin": "00000010", "arg_type":"val"},
    "lda": {"bin": "00000011", "arg_type":"reg"},
    "stb": {"bin": "00000100", "arg_type":"val"},
    "ldb": {"bin": "00000101", "arg_type":"reg"},
    "and": {"bin": "00000110", "arg_type":"reg"},
    "orr": {"bin": "00000111", "arg_type":"reg"},
    "nor": {"bin": "00001000", "arg_type":"reg"},
    "xor": {"bin": "00001001", "arg_type":"reg"},
    "add": {"bin": "00001010", "arg_type":"reg"},
    "sub": {"bin": "00001011", "arg_type":"reg"},
    "jnz": {"bin": "00001100", "arg_type":"val"},
    "jez": {"bin": "00001101", "arg_type":"val"},
    "stm": {"bin": "00001110", "arg_type":"reg"},
    "ldm": {"bin": "00001111", "arg_type":"reg"}
}

REGISTERS_TABLE = {
    "r0": "00000000",
    "r1": "00000001",
    "r2": "00000010",
    "r3": "00000011",
    "r4": "00000100",
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
            
            line_count += 1

    line_count = 0
    print(labels)

    for line in lines:
        if len(line) > 0:
            if line[0] == ";":
                continue

        line = line.lstrip()
        words = line.split(" ")

        if len(words) >= 1 and words[0] != "":
            instruction = words[0]      

            if instruction.startswith("."): 
                continue

            if not instruction in TOKENS_TABLE:
                print("\nUnknown instruction: ", instruction)
                return 

            output += TOKENS_TABLE[instruction]["bin"] + " "
            line_count += 1

            if TOKENS_TABLE[instruction]["arg_type"] == "null":

                output += "00000000 "
                continue

            if TOKENS_TABLE[instruction]["arg_type"] == "reg":
                param = words[1]

                if not param in REGISTERS_TABLE:
                    print("\nUknown register: ", param)
                    return
                
                output += REGISTERS_TABLE[param] + " "
            elif TOKENS_TABLE[instruction]["arg_type"] == "val":
                param = words[1]
                
                if instruction == "jnz" or instruction == "jez" and not param.isdigit():
                    if not param in labels:
                        print(f"Label {param} does not exist")
                        return

                    param = labels[param]
                else:
                    if not param.isdigit():
                        print("\nValue parameter is not a number: ", param)
                        return
                
                output += format(int(param) & 0xFF, '08b') + " "
    
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
