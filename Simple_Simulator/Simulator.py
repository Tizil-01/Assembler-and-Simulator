import sys

# TODO: Set flag in current instruction or reset them
# TODO: Jump mem_addr collides with variables address


def raise_error(s):
    print(s)
    sys.exit()


def decimal_from_binary(binary):
    if (binary_check(binary) == False):
        raise_error("Binary value error")
        return 0
    else:
        # print(binary, " was passed into function")
        binary = binary[::-1]
        # print("now it is", binary)

        exponent = 1
        num = 0
        for digit in binary:
            num += exponent * (int(digit))
            exponent *= 2
        return num

# Checks for binary


def binary_check(b):
    for digit in b:
        if (digit != '0' and digit != '1'):
            return False
    return True


def binary_of_length(b, length):
    if (not binary_check(b)):
        raise_error(f"Line {i} : Binary value error")
        return
    l = len(b)
    
    if(l == length):
        return b
    if(l < length):
        num_0 = length - l
        b = "0"* num_0 + b
        if(binary_check(b)):
            return b
        raise_error(f"Line {i} : Binary value error")
        return
    if (l > length):
        b = b[-length:]
        return b


def binary_from_decimal(decimal):
    if (decimal == 0):
        return "0"
    binary = ""
    while decimal > 0:
        bin = decimal % 2
        binary = str(bin) + binary

        decimal = decimal//2
    # print(binary)
    if binary_check(binary) and len(binary):
        return binary
    raise_error("Unexpected error")

def get_register(ins, num):
    r_num = ins[num:num+3]
    r_num = decimal_from_binary(r_num)
    if (0 <= r_num < 7):
        return "R"+str(r_num)
    return "FLAG"

def get_immediate_value(ins, num):
    imm = ins[num:num+7]
    imm = decimal_from_binary(imm)
    return imm

def fetch_data(memory, pc):
    if (len(memory) > pc):
        return memory[pc]
    print("Invalid program counter :", pc, ", maximum value is", len(memory))
    sys.exit()


def execute(instruction):
    if (len(instruction) != 16) and binary_check(instruction):
        raise_error(f"Inalid instruction in line {pc}")
    opcode = instruction[:5]
    op = operation[opcode]
    op_type = operation_type[op]
    
    flag = False
    if op_type == "A":
        r1 = get_register(instruction, 7)
        r2 = get_register(instruction, 10)
        r3 = get_register(instruction, 13)
        result = 0
        if op == "add":
            result = Registor_File[r2] + Registor_File[r3]
        elif op == "sub":
            result = Registor_File[r2] - Registor_File[r3]
        elif op == "mul":
            result = Registor_File[r2] * Registor_File[r3]
        elif op == "xor":
            result = Registor_File[r2] ^ Registor_File[r3]
        elif op == "or" :
            result = Registor_File[r2] | Registor_File[r3]
        elif op == "and":
            result = Registor_File[r2] & Registor_File[r3]
            
        if -1 < result < 2**16:
            Registor_File[r1] = result
        else:
            Registor_File[r1] = 0
            Registor_File["FLAG"] = 8
            flag = True
                
    elif op_type == "B":
        r1 = get_register(instruction, 6)
        imm = get_immediate_value(instruction, 9)
        if op == "mov_i":
            Registor_File[r1] = imm
        elif op == "rs":
            Registor_File[r1] = (Registor_File[r1] >> imm) % 2**16
        elif op == "ls":  
            Registor_File[r1] = (Registor_File[r1] << imm) % 2**16
            
    elif op_type == "C":
        r1 = get_register(instruction, 10)
        r2 = get_register(instruction, 13)
        op1 = Registor_File[r1]
        op2 = Registor_File[r2]
        if op == "mov_r":
            Registor_File[r1] = op2
        elif op == "div":
            if op2 == 0:
                Registor_File["R0"] = 0
                Registor_File["R1"] = 0
                Registor_File["FLAG"] = 8
                flag = True
            else:
                Registor_File["R0"] = op1 // op2
                Registor_File["R1"] = op1 % op2
        elif op == "not":
            Registor_File[r1] = ~op2
        elif op == "cmp":
            if op1 < op2:
                Registor_File["FLAG"] = 4
            elif op1 == op2:
                Registor_File["FLAG"] = 1
            else:
                Registor_File["FLAG"] = 2
            flag = True
              
    elif op_type == "D":
        r1 = get_register(instruction, 6)
        mem_addr = instruction[9:]
        if op == "ld":
            if mem_addr not in Variables:
                Variables[mem_addr] = 0
            Registor_File[r1] = Variables[mem_addr]
              
        elif op == "st":
            Variables[mem_addr] = Registor_File[r1]
        
        
    elif op_type == "E": 
        BranchTarget = decimal_from_binary(instruction[9:])
        isBranch = False
        if op == "jmp":
            isBranch = True
        elif op == "jlt" and Registor_File["FLAG"] == 4:
            isBranch = True
        elif op == "jgt" and Registor_File["FLAG"] == 2:
            isBranch = True
        elif op == "je" and Registor_File["FLAG"] == 1:
            isBranch = True
       
        if isBranch:
            return BranchTarget, False, flag
        else:
            return pc+1, False, flag 
        
                  
    elif op_type == "F":
        return pc + 1, True, flag

    return pc+1, False, flag
            
user_input = sys.stdin.readlines()  

with open("input.txt", "w") as file:
    file.writelines(user_input)

f = open("input.txt", "r")
memory = f.readlines()
f.close()
for i in range(len(memory)):
    memory[i] = memory[i].strip()


pc = 0
is_halt = False

operation = {'00000': 'add',
             '00001': 'sub',
             '00011': 'mov_r',
             '00010': 'mov_i',
             '00100': 'ld',
             '00101': 'st',
              '00110': 'mul',
              '00111': 'div',
              '01000': 'rs',
              '01001': 'ls',
             '01010': 'xor',
              '01011': 'or',
              '01100': 'and',
              '01101': 'not',
              '01110': 'cmp',
              '01111': 'jmp',
              '11100': 'jlt',
              '11101': 'jgt',
              '11111': 'je',
              '11010': 'hlt'}
operation_type = {'add': 'A', 'sub': 'A', 'mov_i': 'B', 'mov_r': 'C', 'ld': 'D', 'st': 'D', 'mul': 'A', 'div': 'C', 'rs': 'B',
                  'ls': 'B', 'xor': 'A', 'or': 'A', 'and': 'A', 'not': 'C', 'cmp': 'C', 'jmp': 'E', 'jlt': 'E', 'jgt': 'E', 'je': 'E', 'hlt': 'F'}
Registor_File = {"R0" : 0, "R1" : 0, "R2" : 0, "R3" : 0, "R4" : 0, "R5" : 0, "R6" : 0, "FLAG" : 0}
Variables = {}



f = open("output.txt", "w")


while (not is_halt):
    instruction = fetch_data(memory, pc)
    current_pc = pc
    pc, is_halt, flag_currently_set = execute(instruction)
    
    pc_in_bin = binary_from_decimal(current_pc)
    pc_in_bin = binary_of_length(pc_in_bin, 7)
    
    if not flag_currently_set:
        Registor_File["FLAG"] = 0
        
    f.write(f"{pc_in_bin}       ")
    
    for Registor in Registor_File:
        val = Registor_File[Registor]
        val_in_bin = binary_from_decimal(val)
        val_in_bin = binary_of_length(val_in_bin, 16)
        f.write(f" {val_in_bin}")
    f.write("\n")

for i in memory:
    f.write(i + "\n")
    
var_pcs = list( decimal_from_binary(i) for i in list(Variables.keys()))
# var_pcs = list(5 for i in range(len(Variables)))
for i in range (len(memory), 128):
    if i in var_pcs:
        pc_var = binary_from_decimal(i)
        pc_var = binary_of_length(pc_var, 7)
        
        val = Variables[pc_var]
        val = binary_from_decimal(val)
        val = binary_of_length(val, 16)
        f.write(val)
    else:        
        f.write("0000000000000000")
        
    if i != 127:
        f.write("\n")
    
f.close()
with open("output.txt", "r") as file:
    output = file.read() 

sys.stdout.write(output)