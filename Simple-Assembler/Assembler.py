import os
import sys


# binary is a string with 0 and 1
# Corresponding number will be returned
# else return -1, if input is invalid
def decimal_from_binary(binary):
    if (binary_check(binary) == False):
        Raise_error(f"Line {i} : Binary value error")
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
 
#Checks for binary              
def binary_check(b):
    for digit in b:
        if (digit != '0' and digit != '1'):
            return False
    return True

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
    Raise_error(f"Line {i} : Binary value error")

def binary_of_length(b, length):
    if (not binary_check(b)):
        Raise_error(f"Line {i} : Binary value error")
        return
    l = len(b)
    
    if(l == length):
        return b
    if(l < length):
        num_0 = length - l
        b = "0"* num_0 + b
        if(binary_check(b)):
            return b
        Raise_error(f"Line {i} : Binary value error")
        return
    if (l > length):
        b = b[-length:]
        return b



def Raise_error(s):
    print(s)
    f = open("output.txt", "w")
    f.write(s + "\n")
    f.close()
    sys.exit()



def input_valid_file_name_from_user():
    # Ask user for input file name
    name = input("Enter file name (without extension) : ")
    file = name + ".txt"
    # Checks for valid file existence in CWD
    while(os.path.exists(file) == False):
        name = input("Enter a valid file name please: ")
        file = name + ".txt"
    return file

def check_number_of_lines(program):
    # Number of lines > 128
    num_of_lines = len(program)
    if (num_of_lines > Max_num_of_lines):
        Raise_error("Memory Limit Exceeded, Number of lines in code are more than memory can handle")
    return num_of_lines

def separate_each_term_in_all_lines(program):
    program_ls = []
    for line in program:
        line = line.strip()
        while "\t" in line:
            line = line.replace("\t", "     ")
        while "  " in line:
            line = line.replace("  ", " ")
        if (line.count(" ") == len(line)):
            continue
        ls = list(line.split(" "))
        program_ls.append(ls)
    return program_ls



def check_and_set_variables(program_ls):
    i = 0
    while (True):
        l = len(program_ls[i])
        if (l == 0):
            i += 1
            continue
        
        command = program_ls[i][0]
        if (command == "var"):
            if (l == 2):
                variables[program_ls[i][1]] = i
            else:
                Raise_error("General Syntax Error in line " + str(i))        
            i += 1
            
        else:
            break
        
        if (i == num_of_lines):
            Raise_error("Missing hlt instruction")
    num_of_vars = i        
    for var in variables:
        variables[var] =  variables[var] + num_of_lines - num_of_vars
    return num_of_vars

def check_hlt(program):
    if ("hlt" not in program[-1]):
        # print("here", program[-1])
        Raise_error("Missing hlt instruction at the end")

def find_labels(program_ls):
    i = num_of_vars
    while (i < num_of_lines):
        ls = program_ls[i]
        l = len(ls)
        if (l == 0):
            i += 1
            continue
        if ":" in ls:
            Raise_error(f"Line {i} : Label Syntax Error")
        elif ls[0][-1] == ":":
            labels[ls[0][:-1]] = i - num_of_vars
            if(ls[-1][-1] == ":"):
                only_labels.append(i)
            i += 1
        else:
            i += 1
            



def machine_code(ls, i, opperation):
    s = ""
    command = opperation 
    typ = opp_code[command][1]
    
    if typ == "A":
        s = Validate_type_A(ls, i, opperation)
    elif typ == "B":
        s = Validate_type_B(ls, i, opperation)
    elif typ == "C":
        s = Validate_type_C(ls, i, opperation)
    elif typ == "D":
        s = Validate_type_D(ls, i, opperation)
    elif typ == "E":
        s = Validate_type_E(ls, i, opperation)
    s += "\n"
    return s
 
 
 
def Validate_type_A(ls, i, op):
    if len(ls) != 4:
        Raise_error(f"Line {i} : Invalid Syntax")
    s = opp_code[op][0] 
    s += "0"*2
    s += Validate_reg(ls[1])
    s += Validate_reg(ls[2])
    s += Validate_reg(ls[3])
    return s

def Validate_type_B(ls, i, op):
    if len(ls) != 3:
        Raise_error(f"Line {i} : Invalid Syntax")
    s = opp_code[op][0] 
    s += "0"*1
    s += Validate_reg(ls[1])
    s += Validate_Imm(ls[2])
    return s

def Validate_type_C(ls, i, op):
    if len(ls) != 3:
        Raise_error(f"Line {i} : Invalid Syntax")
    s = opp_code[op][0] 
    s += "0"*5
    s += Validate_reg(ls[1])
    if (op == "mov_r" and ls[2] == "FLAGS"):
        s += "111"
    else:
        s += Validate_reg(ls[2])
    return s

def Validate_type_D(ls, i, op):
    if len(ls) != 3:
        Raise_error(f"Line {i} : Invalid Syntax")
    s = opp_code[op][0] 
    s += "0"*1
    s += Validate_reg(ls[1])
    s += Validate_var(ls[2])
    return s

def Validate_type_E(ls, i, op):
    if len(ls) != 2:
        Raise_error(f"Line {i} : Invalid Syntax")
    s = opp_code[op][0] 
    s += "0"*4
    s += Validate_label(ls[1])
    return s



def Validate_reg(Reg_name):
    if Reg_name in reg_address:
        return reg_address[Reg_name]
    Raise_error(f"Line {i} : Invalid Register name")
    return ""

def Validate_Imm(Imm_value):
    Imm_value = Imm_value[1:]
    for digit in Imm_value:
        if not digit.isdigit():
            Raise_error(f"Line {i} : Invalid Imm value")
        
    if (127 >= int(Imm_value) >= 0):
        b = binary_from_decimal(int(Imm_value))
        b = binary_of_length(b, 7)
        return str(b)
    Raise_error(f"Line {i} : Invalid Imm value")
    return ""

def Validate_var(var_name):
    if var_name in variables:
        b = binary_from_decimal(variables[var_name])
        b = binary_of_length(b, 7)
        return str(b)
    Raise_error(f"Line {i} : Invalid Var name")
    return ""

def Validate_label(label_name):
    if label_name in labels:
        b = binary_from_decimal(labels[label_name])
        b = binary_of_length(b, 7)
        return str(b)
    Raise_error(f"Line {i} : Invalid Label name")
    return ""



Max_num_of_lines = 128

opp_code = {"add"   : ["00000", "A"],
            "sub"   : ["00001", "A"],
            "mov_i" : ["00010", "B"],
            "mov_r" : ["00011", "C"],
            "ld"    : ["00100", "D"],
            "st"    : ["00101", "D"],
            "mul"   : ["00110", "A"],
            "div"   : ["00111", "C"],
            "rs"    : ["01000", "B"],
            "ls"    : ["01001", "B"],
            "xor"   : ["01010", "A"],
            "or"    : ["01011", "A"],
            "and"   : ["01100", "A"],
            "not"   : ["01101", "C"],
            "cmp"   : ["01110", "C"],
            "jmp"   : ["01111", "E"],
            "jlt"   : ["11100", "E"],
            "jgt"   : ["11101", "E"],
            "je"    : ["11111", "E"]            
            }
commands = list(opp_code.keys())

inst_type =   {"A" : [2,4],
               "B" : [1,3],
               "C" : [5,3],
               "D" : [1,3],
               "E" : [4,2],
               "F" : [11,1]}

reg_address = {"R0"   : "000",
               "R1"   : "001",
               "R2"   : "010",
               "R3"   : "011",
               "R4"   : "100",
               "R5"   : "101",
               "R6"   : "110",
               }


# Reads file
# file = input_valid_file_name_from_user()
# f = open(file, "r")
# program= f.readlines()
# f.close()

program = sys.stdin.readlines()

# Number of lines > 128
num_of_lines = check_number_of_lines(program) 
# print("Number of lines is ", num_of_lines) 
  
# Stores the program as list of list with all terms separated    
program_ls = separate_each_term_in_all_lines(program)

# Reads variables and stores their mem_address
variables = {}      
num_of_vars = check_and_set_variables(program_ls)
# print("Number of variables is ", num_of_vars)
   
# Last line is hlt
check_hlt(program)
# print("Last line is hlt")

# Reads labes and stores their mem_address
labels = {}
only_labels = []
find_labels(program_ls)
labels_indexes = list(labels.values())
# print("Labels are ", len(labels))
# print(labels)
     
# Actual reading begins here        
i = num_of_vars

output_string = ""
for i in range (num_of_vars, num_of_lines - 1):
    if ((i - num_of_vars) in labels_indexes):
        if ((i - num_of_vars) in only_labels):
            continue
        elif (len(program_ls[i]) > 1): 
            program_ls[i] = program_ls[i][1:]
        else:
            Raise_error(f"Unexpected error in Line {i}")
    
    l = len(program_ls[i])
    if (l == 0):
        continue
    
    instruction = program_ls[i][0]
    if(instruction == "mov"):
        if (len (program_ls[i]) != 3):
            Raise_error(f"Line {i} : Number of arguments given is invalid")
            
        if (program_ls[i][2][0] == "$"):
            instruction = "mov_i"
        else:
            instruction = "mov_r"
            
    if instruction not in commands:
        print(program_ls[i])
        Raise_error(f"Line {i} : Invalid operation")
    
    command = instruction 
    typ = opp_code[command][1]
    req_len = inst_type[typ][1]
    
    if(l != req_len):
        Raise_error(f"Line {i} : Number of arguments given is invalid")
        
    output_string = output_string + machine_code(program_ls[i], i, instruction)
        

output_string += "1101000000000000" 

# f = open("output.txt", "w")
# f.write(output_string)
# f.close() 
# print(output_string)      
sys.stdout.write(output_string)