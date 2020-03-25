"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.reg[self.sp] = 0xf4
        self.branchtable = {}
        self.branchtable[0b00000001] = self.operand_hlt
        self.branchtable[0b01000111] = self.operand_prn
        self.branchtable[0b10000010] = self.operand_ldi
        self.branchtable[0b10100010] = self.operand_mlt
        self.branchtable[0b01000110] = self.operand_pop
        self.branchtable[0b01000101] = self.operand_push
    
    
    def ram_read(self, mar):
        return self.ram[mar]
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr    
    def read_params(self):
        params = sys.argv
        if len(params) != 2: # a file is being passed through
            print("usage: file.py filename")
            sys.exit(1)
        if len(params)==2:   
            try:
                with open(params[1]) as f:
                    address = 0
                    for line in f:
                        # print(line)
                        comment_split = line.split("#")
                        # Strip out whitespace
                        num = comment_split[0].strip()
                        # Ignore blank lines
                        if num == '':
                            continue
                        val = int("0b"+num,2)
                        self.ram_write(address, val)
                        address += 1    
            except FileNotFoundError:
                print("File not found")
                sys.exit(2)

    def load(self):
        """Load a program into memory."""
        self.read_params()

        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    def operand_ldi(self):
        reg_num = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.reg[reg_num] = value
        self.pc += 3
    def operand_prn(self):
        reg_num = self.ram_read(self.pc + 1)
        print(self.reg[reg_num])
        self.pc += 2  
    def operand_hlt(self):
        self.pc += 1
        return False
    def operand_mlt(self):
        reg_num = self.ram_read(self.pc + 1)
        reg_num2 = self.ram_read(self.pc + 2)
        value = self.reg[reg_num] * self.reg[reg_num2]
        self.reg[reg_num] = value
        print(value)
        self.pc += 3
    def operand_pop(self):
        value = self.ram[self.reg[self.sp]]
        reg_num = self.ram[self.pc + 1]
        self.reg[reg_num] = value
        self.reg[self.sp] += 1
        self.pc += 2
    def operand_push(self):
        self.reg[self.sp] -= 1
        reg_num = self.ram[self.pc + 1]
        value = self.reg[reg_num]
        self.ram[self.reg[self.sp]] = value
        self.pc += 2

    

    def run(self):
        """Run the CPU."""

        ldi = 0b10000010
        prn = 0b01000111
        hlt = 0b00000001
        mlt = 0b10100010
        push = 0b01000101
        pop = 0b01000110 

        running = True
        ram = self.ram 
        reg = self.reg 
        pc = self.pc 
        
        # while running:
        #     command = self.ram[self.pc]
            # if command == hlt:
            #     running = False
            # elif command == push:
            #     self.reg[self.sp] -= 1
            #     reg_num = self.ram[self.pc + 1]
            #     value = self.reg[reg_num]
            #     self.ram[self.reg[self.sp]] = value
            #     self.pc += 2
            # elif command == pop:
            #     value = self.ram[self.reg[self.sp]]
            #     reg_num = self.ram[self.pc + 1]
            #     self.reg[reg_num] = value
            #     self.reg[self.sp] += 1
            #     self.pc += 2
            # else:
        while not (self.ram_read(self.pc) is hlt):
                    instruction = self.ram_read(self.pc)
                    self.branchtable[instruction]()
            # command = ram[pc]
            # if command == ldi:
            #     reg_num = self.ram_read(pc + 1)
            #     value = self.ram_read(pc + 2)
            #     reg[reg_num] = value
            #     pc += 3
            # elif command == prn:
            #     reg_num = self.ram_read(pc + 1)
            #     print(reg[reg_num])
            #     pc += 2
            # elif command == hlt:
            #     running = False 
            #     pc += 1
            # elif command == mlt:
            #     reg_num = self.ram_read(pc + 1)
            #     reg_num2 = self.ram_read(pc + 2)
            #     value = reg[reg_num] * reg[reg_num2]
            #     reg[reg_num] = value
            #     pc += 3

            # else:
            #     print(f"Unknown instruction: {command}")
                