"""Literal bounded-word RAM execution, with no macro or TM instructions."""

from compiler import OPS, require


class RAM:
    def __init__(self, width, code, inputs):
        require(type(width) is int and 10 <= width <= 512, "RAM width limit")
        require(1 <= len(code) <= 1000000 and len(inputs) <= 1000000,
                "RAM code/input limit")
        self.width = width
        self.mask = (1 << width) - 1
        require(all(type(x) is int and 0 <= x <= self.mask for x in inputs),
                "RAM input word")
        self.code, self.inputs = code, tuple(inputs)
        self.memory, self.output = {}, []
        self.pc = self.cursor = self.steps = 0
        self.data_reads, self.data_writes = set(), set()

    def get(self, address):
        return self.memory.get(address & self.mask, 0)

    def put(self, address, value):
        self.memory[address & self.mask] = value & self.mask

    def step(self):
        require(0 <= self.pc < len(self.code), "RAM program counter")
        op, *args = self.code[self.pc]
        require(op in OPS, "RAM opcode")
        if op == "halt" or (op == "read" and self.cursor == len(self.inputs)):
            return False
        self.pc += 1
        if op == "set":
            self.put(args[0], args[1])
        elif op == "load":
            address = self.get(args[1])
            self.data_reads.add(address)
            self.put(args[0], self.get(address))
        elif op == "store":
            address = self.get(args[0])
            self.data_writes.add(address)
            self.put(address, self.get(args[1]))
        elif op == "not":
            self.put(args[0], self.mask ^ self.get(args[1]))
        elif op in ("add", "sub", "and", "or", "shiftl", "shiftr"):
            self.arithmetic(op, args)
        elif op == "read":
            self.put(args[0], self.inputs[self.cursor])
            self.cursor += 1
        elif op == "write":
            require(len(self.output) < 1000000, "RAM output capacity")
            self.output.append(self.get(args[0]))
        elif op == "jump":
            self.pc = args[0]
        elif op == "jzero":
            if self.get(args[0]) == 0:
                self.pc = args[1]
        elif op == "jlt" and self.get(args[0]) < self.get(args[1]):
            self.pc = args[2]
        self.steps += 1
        return True

    def arithmetic(self, op, args):
        destination, left, right = args
        x, y = self.get(left), self.get(right)
        if op == "add":
            value = x + y
        elif op == "sub":
            value = max(0, x - y)
        elif op == "and":
            value = x & y
        elif op == "or":
            value = x | y
        elif op == "shiftl":
            value = x << y if y < self.width else 0
        else:
            value = x >> y if y < self.width else 0
        self.put(destination, value)
