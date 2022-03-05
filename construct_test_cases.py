for code in ['LDM', 'LDD', 'LDI', 'LDX', 'LDR', 'MOV', 'STO', 'ADD', 'SUB', 'INC', 'DEC', 'JMP', 'CMP', 'CMI', 'JPE', 'JPN', 'IN', 'OUT/', 'END', 'AND', 'OR', 'XOR', 'LSL', 'LSR']:

    print(f"{code} missing operand/", f"{code},OUT/", True if code in "OUT/,IN,END".split(",") else False, sep="")
    print(f"{code} den operand/", f"{code} #7,OUT/", True if code in 'ADD,SUB,AND,XOR,OR,LDM,LDR,CMP,LSL,LSR'.split(",") else False, sep="")
    print(f"{code} hex operand/", f"{code} &07,OUT/", True if code in 'ADD,SUB,AND,XOR,OR'.split(",") else False, sep="")
    print(f"{code} bin operand/", f"{code} B0111,OUT/", True if code in 'ADD,SUB,AND,XOR,OR'.split(",") else False, sep="")
    print(f"{code} valid address operand/", f"LDM #7,STO 99,{code} 99,OUT/", True if code not in ["IN", "OUT/", "CMP", "LDM", "MOV", "LSL", "LSR", "LDR", "END"] else False, sep="")
    print(f"{code} OUT/ of range address operand/", f"{code} 123,OUT/", False, sep="")
    print(f"{code} invalid address operand/", f"{code} a99,OUT/", False, sep="")
    print(f"{code} valid symbol operand/", f"{code} TEST,OUT,TEST: 7/", True if code not in ["IN", "OUT/", "CMP", "LDM", "MOV", "LSL", "LSR", "LDR", "END"] else False, sep="")
    print(f"{code} invalid symbol operand/", f"{code} TEST,OUT/", False, sep="")
