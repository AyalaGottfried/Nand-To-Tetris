from CommandType import CommandType


class CodeWriter:
    def __init__(self, file_name):
        self.file = open(file_name, "w")
        self.labels = "0"

    def _write(self, lines):
        """ write lines to the file """
        self.file.write('\n'.join(lines))
        self.file.write('\n')

    def _write_action(self, action):
        """ write code for arithmetic action on RAM[SP-1], RAM[SP-2] to RAM[SP-2] and to D """
        self._write(["@SP", "AM=M-1", "D=M", "A=A-1", "MD=M" + action + "D"])

    def _write_result(self, val):
        """ write code for save val in RAM[SP-1] """
        self._write(["@SP", "A=M-1", "M=" + val])

    def _write_binary_cond(self, cond):
        """ write code which perform binary condition arithmetic action """
        self._write_action("-")
        self._write(["@FALSE" + self.labels, "D;" + cond])
        self._write_result("-1")
        self._write(["@CONTINUE" + self.labels, "0;JMP", "(FALSE" + self.labels + ")"])
        self._write_result("0")
        self._write(["(CONTINUE" + self.labels + ")"])
        self.labels = str(int(self.labels) + 1)

    def _write_unary(self, action):
        """ write code which perform unary arithmetic action """
        self._write_result(action + "M")

    def _write_address_push_pop(self, src, index, for_push):
        """ write code which put the address for push or pop to D """
        self._write(["@" + src, "D=M", "@" + str(index)] + for_push)

    def _write_value_push_pop(self, src, is_address):
        """ write code which put the value for push or pop to D """
        self._write(["@" + src, "D=" + is_address])

    def write_arithmetic(self, command):
        """ write code which perform arithmetic action """
        if command == "add":
            self._write_action("+")
        elif command == "sub":
            self._write_action("-")
        elif command == "neg":
            self._write_unary("-")
        elif command == "eq":
            self._write_binary_cond("JNE")
        elif command == "gt":
            self._write_binary_cond("JLE")
        elif command == "lt":
            self._write_binary_cond("JGE")
        elif command == "and":
            self._write_action("&")
        elif command == "or":
            self._write_action("|")
        elif command == "not":
            self._write_unary("!")

    def write_push_pop(self, command, segment, index):
        """ write code which perform push or pop action """
        dic_address = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}
        dic_value = {"constant": str(index), "static": self.file.name.rsplit('.', 1)[0] + "." + str(index),
                     "temp": str(5 + index), "pointer": str(3 + index)}
        if segment in dic_address:
            for_push = ["D=D+A"] if command is CommandType.C_POP else ["A=D+A", "D=M"]
            self._write_address_push_pop(dic_address[segment], index, for_push)
        else:
            is_address = "A" if command is CommandType.C_POP or segment == "constant" else "M"
            self._write_value_push_pop(dic_value[segment], is_address)
        if command is CommandType.C_PUSH:
            self._write(["@SP", "A=M", "M=D", "@SP", "M=M+1"])
        elif command is CommandType.C_POP:
            self._write(["@R13", "M=D", "@SP", "M=M-1", "@SP", "A=M", "D=M", "@R13", "A=M", "M=D"])

    def close(self):
        """ write code for close the program and close the file """
        self._write(["(END)", "@END", "0;JMP"])
        self.file.close()
