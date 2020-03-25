"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
    
    
    def ram_read(self, mar):
        return self.ram[mar]
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr    

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

    def run(self):
        """Run the CPU."""

        ldi = 0b10000010
        prn = 0b01000111
        hlt = 0b00000001
        mlt = 0b10100010

        running = True
        ram = self.ram 
        reg =  self.reg 
        pc = self.pc 
        
        while running:
            command = ram[pc]
            if command == ldi:
                reg_num = self.ram_read(pc + 1)
                value = self.ram_read(pc + 2)
                self.ram_write(reg_num,value)
                pc += 3
            elif command == prn:
                reg_num = self.ram_read(pc + 1)
                print(reg[reg_num])
                pc += 2
            elif command == hlt:
                running = False 
                pc += 1
            elif command == mlt:
                reg_num = self.ram_read(pc + 1)
                reg_num2 = self.ram_read(pc + 2)
                value = reg[reg_num] * reg[reg_num2]
                reg[reg_num] = value

            else:
                print(f"Unknown instruction: {command}")
                