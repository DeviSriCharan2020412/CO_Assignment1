from colorama import Fore


def TypeA(instruction, reg1, reg2, reg3):
    dic1 = {"add": "00000", "sub": "00001", "mul": "00110", "xor": "01010", "or": "01011", "and": "01100"}

    dic2 = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}

    return dic1[instruction] + "00" + dic2[reg1] + dic2[reg2] + dic2[reg3]


def TypeB(instruction, reg1, immediateValue):
    dic1 = {"mov": "00010", "rs": "'01000", "ls": "01001"}

    dic2 = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}

    return dic1[instruction] + dic2[reg1] + format(immediateValue, '08b')


def TypeC(instruction, reg1, reg2):
    dic1 = {"mov": "00011", "div": "00111", "not": "01101", "cmp": "01110"}

    dic2 = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}

    return dic1[instruction] + "00000" + dic2[reg1] + dic2[reg2]


def TypeD(instruction, reg1, mem_addr):
    dic1 = {"ld": "00100", "st": "00101"}

    dic2 = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}

    return dic1[instruction] + dic2[reg1] + format(mem_addr, '08b')


def TypeE(instruction, mem_addr):
    dic1 = {"jmp": "01111", "jlt": "10000", "jgt": "10001", "je": "10010"}

    return dic1[instruction] + "000" + format(mem_addr, '08b')


def mem_address(list1, list2, f):
    for i in range(len(list2)):
        if list2[i][1] == f:
            return len(list1) + i
    return 0


def error_identifier(list1, list2, labels, label_addr):
    code = []
    code.extend(list2)
    code.extend(list1)

    var = []
    for i in range(len(list2)):
        var.append(list2[i][1])

    list_typeA = ['add', 'sub', 'mul', 'xor', 'or', 'and']
    list_typeB = ['mov', 'rs', 'ls']
    list_typeC = ["mov", "div", "not", "cmp"]
    list_typeD = ["ld", "st"]
    list_typeE = ["jmp", "jlt", "jgt", "je"]
    list_register = ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'FLAGS']

    checker = False
    temp = True
    tempvar = True
    end = len(code) - 1
    count_hlt = 0
    s = 0

    if var != list(set(var)):
        print(Fore.RED + "Error>> Misuse of variables ")

    if labels != list(set(labels)):
        print(Fore.RED + "Error>> Misuse of labels ")

    for k in range(len(code)):
        if code[k][0] != "var":
            tempvar = False

        if s < len(label_addr) and k == label_addr[s]:
            temp1 = True
            for i in range(len(labels[s])):
                if not labels[s][i].isalnum() and labels[s][i] != "_":
                    temp1 = False
                    break
            if not temp1:
                checker = True
                print(Fore.RED + "Error>> Line:" + str(k + 1) + " not a correct label name")
            s += 1

        if len(code[k]) > 4:
            print(Fore.RED + "Error>> Line: " + str(k + 1) + " Wrong syntax used for instructions")

        elif (len(code[k])) == 4:
            if code[k][0] not in list_typeA and code[k][0][-1] != ":":
                checker = True
                print(Fore.RED + "Error>> Line: " + str(k + 1) + " Typos in instruction name")
                if (code[k][1] not in list_register) or (code[k][2] not in list_register) or (
                        code[k][3] not in list_register):
                    checker = True
                    print(Fore.RED + "Error>> Line: " + str(k + 1) + " Typos in register name")

        elif (len(code[k])) == 3:
            if (code[k][0] not in list_typeB) and (code[k][0] not in list_typeC) and (code[k][0] not in list_typeD):
                checker = True
                print(Fore.RED + "Error>> Line: " + str(k + 1) + " Wrong syntax used for instructions")

            if code[k][0] in list_typeB:
                if code[k][1] not in list_register:
                    print("TYPE_B")
                    checker = True
                    print(Fore.RED + "Error>> Line: " + str(k + 1) + " Typos in register name")

                if code[k][2][0] == "$":
                    if int(code[k][2][1:]) > 255 or int(code[k][2][1:]) < 0:
                        checker = True
                        print(Fore.RED + "Error>> Line: " + str(
                            k + 1) + " Illegal Immediate values (less than 0 or more than 255)")

            if (code[k][0] in list_typeC) and code[k][2][0] != "$":
                if (code[k][1] not in list_register) or (code[k][2] not in list_register):
                    print("TYPE_C")
                    checker = True
                    print(Fore.RED + "Error>> Line: " + str(k + 1) + " Typos in register name")

            if code[k][0] in list_typeD:
                if code[k][1] not in list_register:
                    print("TYPE_D")
                    checker = True
                    print(Fore.RED + "Error>> Line: " + str(k + 1) + " Typos in register name")

                if code[k][2] not in var:
                    checker = True
                    print(Fore.RED + "Error>> Line: " + str(k + 1) + " Use of undefined variables")

                if code[k][2] in labels:
                    checker = True
                    print(Fore.RED + "Error>> Line: " + str(k + 1) + " Misuse of labels as variables or vice-versa")

        elif (len(code[k])) == 2:
            if code[k][0] not in list_typeE and code[k][0] != "var":
                checker = True
                print(Fore.RED + "Error>> Line: " + str(k + 1) + " Wrong syntax used for instructions")

            if code[k][0] in list_typeE:
                if code[k][1] not in labels:
                    print(Fore.RED + "Error>> Line: " + str(k + 1) + " Use of undefined labels")

                if code[k][1] in var:
                    checker = True
                    print(Fore.RED + "Error>> Line: " + str(k + 1) + " Misuse of labels as variables or vice-versa")

            if code[k][0] == "var":
                if not tempvar:
                    checker = True
                    print(Fore.RED + "Error>> Line: " + str(k + 1) + " Variable not defined at the beginning")

        elif code[k][0] == 'hlt':
            count_hlt += 1
            temp = False
        else:
            print(Fore.RED + "Error>> Line: " + str(k + 1) + " Wrong syntax used for instructions")

    if temp:
        checker = True
        print(Fore.RED + "Error>> Missing hlt instruction")

    if not temp and code[end][0] != "hlt":
        checker = True
        print(Fore.RED + "Error>> hlt not being used as the last instruction")
    if count_hlt > 1:
        checker = True
        print(Fore.RED + "Error>> Wrong syntax used for instructions")

    return checker


def ans(list1, list2, labels, labels_addr):
    for i in list1:
        if i[0] == "hlt":
            print("1001100000000000")
            break

        if len(i) == 4:
            if i[0] == "add" or i[0] == "mul" or i[0] == "and" or i[0] == "sub" or i[0] == "xor" or i[0] == "or":
                print(Fore.WHITE + TypeA(i[0], i[1], i[2], i[3]))

        elif len(i) == 3:
            if i[0] == "mov":
                if i[2][0] == "$":
                    print(Fore.WHITE + TypeB(i[0], i[1], int(i[2][1:])))
                else:
                    print(Fore.WHITE + TypeC(i[0], i[1], i[2]))

            elif i[0] == "rs" or i[0] == "ls":
                print(Fore.WHITE + TypeB(i[0], i[1], int(i[2][1:])))

            elif i[0] == "div" or i[0] == "not" or i[0] == "cmp":
                print(Fore.WHITE + TypeC(i[0], i[1], i[2]))

            elif i[0] == "ld" or i[0] == "st":
                print(Fore.WHITE + TypeD(i[0], i[1], mem_address(list1, list2, i[2])))

        elif len(i) == 2:
            if i[0] == "jmp" or i[0] == "jlt" or i[0] == "jgt" or i[0] == "je":
                label_addr = 0
                for j in range(len(labels)):
                    if i[1] == labels[j]:
                        label_addr = labels_addr[j]
                print(Fore.WHITE + TypeE(i[0], label_addr))


def main():
    list1 = []
    list2 = []
    labels = []
    labels_addr = []
    count = 0
    temp_var_main = False
    while True:
        try:
            s = input()
            if s == "":
                continue
            else:
                p = s.split(" ")
                if p[0] != "var":
                    temp_var_main = True

                if (p[0] == "var") and not temp_var_main and len(p) == 2:
                    list2.append(p)

                if p[0] == "var" and temp_var_main:
                    list1.append(p)

                elif len(p) > 1:
                    if p[0][-1] == ":" and p[1] == "hlt":
                        labels.append(p[0][:-1])
                        labels_addr.append(count)
                        list1.append([p[1]])
                        count += 1

                    elif p[0][-1] == ":":
                        labels.append(p[0][:-1])
                        labels_addr.append(count)
                        p.remove(p[0])
                        list1.append(p)
                        count += 1
                    elif p[0] != "var":
                        list1.append(p)
                        count += 1
                elif len(p) == 1:
                    list1.append(p)

        except EOFError:
            break
    print(list1)
    print(list2)
    if not error_identifier(list1, list2, labels, labels_addr):
        ans(list1, list2, labels, labels_addr)


if __name__ == '__main__':
    main()
