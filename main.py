import toml
from enum import Enum
import numpy as np


class Opcodes(Enum):
    ADD = 0
    SUB = 1
    MOV = 2
    DBG = 3
    AND = 4
    OR = 5
    MUT = 6
    DIV = 7

    def get_str(num):
        match num:
            case 0:
                return "ADD"
            case 1:
                return "SUB"
            case 2:
                return "MOV"
            case 3:
                return "DBG"
            case 4:
                return "AND"
            case 5:
                return "OR"
            case 6:
                return "MUT"
            case 7:
                return "DIV"
            case _:
                return "UNKOWN"


class Operand:
    def __init__(self, data: int, is_registry=False) -> None:
        self.data: int = data
        self.is_registry = is_registry

    def __repr__(self) -> str:
        return f"\n\tData: {self.data}\n\tIs Registry: {self.is_registry}"

    def check_if_registry(self) -> bool:
        return self.is_registry

    def get_data(self) -> int:
        return self.data


class Registry:
    def __init__(self, index) -> None:
        self.index: int = index
        self.data = 0

    def set_data(self, data: int):
        self.data = data

    def get_data(self) -> int:
        return self.data


class RegistryStack:
    def __init__(self, max_size: int) -> None:
        self.registeries = np.empty(max_size, dtype=object)
        for i in range(len(self.registeries)):
            self.registeries[i] = Registry(i)

    def get_registry_data(self, index: int) -> int:
        if index < len(self.registeries):
            return self.registeries[index].get_data()
        else:
            raise IndexError(
                "Index of registry is out of range, to fix it increase the 'max_reg_size' key in config.toml, or check your code for typos.")

    def set_registry_data(self, index: int, data: int):
        if index < len(self.registeries):
            self.registeries[index].set_data(data)
        else:
            raise IndexError(
                "Index of registry is out of range, to fix it increase the 'max_reg_size' key in config.toml, or check your code for typos.")

    def get_max_size(self) -> int:
        return len(self.registeries)


class Instruction:
    def __init__(self, opcode: Opcodes, operands: list[Operand]) -> None:
        self.opcode: Opcodes = opcode
        self.operands: list[Operand] = operands
    def __repr__(self) -> str:
        return f"(Opcode: '{Opcodes.get_str(self.opcode)}', {self.operands})\n)"
class Machine:
    def __init__(self, max_size: int) -> None:
        self.registry_stack = RegistryStack(max_size)
        self.instructions: list[Instruction] = []

    def set_instructions(self, instructions: list[Instruction]):
        self.instructions = instructions

    def append_instruction(self, instruction: Instruction):
        self.instructions.append(instruction)

    def run(self):
        for ins in self.instructions:
            match ins.opcode:
                case Opcodes.DIV:
                    # divising first operand and second operand and store to third operand
                    s = 0
                    fo = ins.operands[0]
                    vfo = fo.get_data()
                    if fo.check_if_registry() == True:
                        vfo = self.registry_stack.get_registry_data(vfo)
                    s = vfo

                    so = ins.operands[1]
                    vso = so.get_data()
                    if so.check_if_registry() == True:
                        vso = self.registry_stack.get_registry_data(vso)
                    s = s // vso

                    if ins.operands[2].check_if_registry() == True:
                        self.registry_stack.set_registry_data(
                            ins.operands[2].get_data(), s)
                    else:
                        raise TypeError(
                            "Operand should be registry, but it is not")
                case Opcodes.MUT:
                    # mutliplying first operand and second operand and store to third operand
                    s = 0
                    fo = ins.operands[0]
                    vfo = fo.get_data()
                    if fo.check_if_registry() == True:
                        vfo = self.registry_stack.get_registry_data(vfo)
                    s = vfo

                    so = ins.operands[1]
                    vso = so.get_data()
                    if so.check_if_registry() == True:
                        vso = self.registry_stack.get_registry_data(vso)
                    s = s * vso

                    if ins.operands[2].check_if_registry() == True:
                        self.registry_stack.set_registry_data(
                            ins.operands[2].get_data(), s)
                    else:
                        raise TypeError(
                            "Operand should be registry, but it is not")
                case Opcodes.OR:
                    # or-ing first operand and second operand and store to third operand
                    s = 0
                    fo = ins.operands[0]
                    vfo = fo.get_data()
                    if fo.check_if_registry() == True:
                        vfo = self.registry_stack.get_registry_data(vfo)
                    s = vfo

                    so = ins.operands[1]
                    vso = so.get_data()
                    if so.check_if_registry() == True:
                        vso = self.registry_stack.get_registry_data(vso)
                    s |= vso
                    if ins.operands[2].check_if_registry() == True:
                        self.registry_stack.set_registry_data(
                            ins.operands[2].get_data(), s)
                    else:
                        raise TypeError(
                            "Operand should be registry, but it is not")
                case Opcodes.AND:
                    # and-ing first operand and second operand and store to third operand
                    s = 0
                    fo = ins.operands[0]
                    vfo = fo.get_data()
                    if fo.check_if_registry() == True:
                        vfo = self.registry_stack.get_registry_data(vfo)
                    s = vfo

                    so = ins.operands[1]
                    vso = so.get_data()
                    if so.check_if_registry() == True:
                        vso = self.registry_stack.get_registry_data(vso)
                    s = s & vso

                    if ins.operands[2].check_if_registry() == True:
                        self.registry_stack.set_registry_data(
                            ins.operands[2].get_data(), s)
                    else:
                        raise TypeError(
                            "Operand should be registry, but it is not")
                case Opcodes.SUB:
                    # Substracting first operand and second operand and store to third operand
                    s = 0
                    fo = ins.operands[0]
                    vfo = fo.get_data()
                    if fo.check_if_registry() == True:
                        vfo = self.registry_stack.get_registry_data(vfo)
                    s = vfo

                    so = ins.operands[1]
                    vso = so.get_data()
                    if so.check_if_registry() == True:
                        vso = self.registry_stack.get_registry_data(vso)
                    s -= vso
                    if ins.operands[2].check_if_registry() == True:
                        self.registry_stack.set_registry_data(
                            ins.operands[2].get_data(), s)
                    else:
                        raise TypeError(
                            "Operand should be registry, but it is not")
                case Opcodes.ADD:
                    # Adding first operand and second operand and store to third operand
                    s = 0
                    fo = ins.operands[0]
                    vfo = fo.get_data()
                    if fo.check_if_registry() == True:
                        vfo = self.registry_stack.get_registry_data(vfo)
                    s += vfo

                    so = ins.operands[1]
                    vso = so.get_data()
                    if so.check_if_registry() == True:
                        vso = self.registry_stack.get_registry_data(vso)
                    s += vso
                    if ins.operands[2].check_if_registry() == True:
                        self.registry_stack.set_registry_data(
                            ins.operands[2].get_data(), s)
                    else:
                        raise TypeError(
                            "Operand should be registry, but it is not")
                case Opcodes.MOV:
                    fo = ins.operands[0]
                    vfo = fo.get_data()
                    if fo.check_if_registry() == True:
                        vfo = self.registry_stack.get_registry_data(vfo)

                    so = ins.operands[1]
                    vso = so.get_data()
                    if so.check_if_registry() == True:
                        self.registry_stack.set_registry_data(vso, vfo)
                    else:
                        raise TypeError(
                            "Operand should be registry, but it is not")
                case Opcodes.DBG:
                    for op in ins.operands:
                        val = op.get_data()
                        reg = ""
                        if op.check_if_registry() == True:
                            reg = "r"+str(val)
                            val = self.registry_stack.get_registry_data(val)
                        print(f"DEBUG: {reg}-> ", val)
class Parser:

    def parse(filename: str) -> list[Instruction]:
        instructions: list[Instruction] = []
        content = []
        with open(filename, "r") as f:
            content = f.readlines()
        content = [i.strip() for i in content]
        for line in content:
            opcode = ""
            operands: list[Operand] = []
            cursor = 0
            tmp = ""
            while True:
                if cursor >= len(line):
                    break
                if line[cursor] == " ":
                    if not opcode:
                        opcode = tmp
                        tmp = ""
                        cursor += 1

                tmp += line[cursor]
                cursor += 1

            operands_ = line.replace(opcode, "").split(",")
            for op in operands_:
                if op:
                    op = op.replace(" ", "")
                    if op.startswith("r"):
                        operands.append(Operand(int(op[1:]), is_registry=True))
                    else:
                        operands.append(Operand(int(op), is_registry=False))

            if operands:
                match opcode.lower():
                    case "add":
                        instructions.append(Instruction(Opcodes.ADD, operands))
                    case "mov":
                        instructions.append(Instruction(Opcodes.MOV, operands))
                    case "sub":
                        instructions.append(Instruction(Opcodes.SUB, operands))
                    case "dbg":
                        instructions.append(Instruction(Opcodes.DBG, operands))
                    case "and":
                        instructions.append(Instruction(Opcodes.AND, operands))
                    case "or":
                        instructions.append(Instruction(Opcodes.OR, operands))
                    case "mut":
                        instructions.append(Instruction(Opcodes.MUT, operands))
                    case "div":
                        instructions.append(Instruction(Opcodes.DIV, operands))
        return instructions


config = toml.load("config.toml")

max_reg_size = int(config["vm"]["max_reg_size"])

instructions = Parser.parse("file.pvm")

pyvm = Machine(max_reg_size)

pyvm.set_instructions(instructions)

pyvm.run()
