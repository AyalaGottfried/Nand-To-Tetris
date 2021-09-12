from CommandType import CommandType


class CodeWriter:
    def __init__(self, file_name):
        self.file = open(file_name, "w")
        self.labels = "0"
        self.file_name = "init"
        self.call_count = 0

    def set_file_name(self, file_name):
        self.file_name = file_name

    def _write(self, lines):
        """ writes lines to the file """
        self.file.write('\n'.join(lines))
        self.file.write('\n')

    def _write_action(self, action):
        """ writes code which calculates action on RAM[SP-1], RAM[SP-2] to RAM[SP-2] and to D """
        self._write(["@SP", "AM=M-1", "D=M", "A=A-1", "MD=M" + action + "D"])

    def _write_result(self, val):
        """ writes code which saves val to RAM[SP-1] """
        self._write(["@SP", "A=M-1", "M=" + val])

    def _write_binary_cond(self, cond):
        """ writes code which performs binary condition arithmetic action """
        self._write_action("-")
        self._write(["@FALSE" + self.labels, "D;" + cond])
        self._write_result("-1")
        self._write(["@CONTINUE" + self.labels, "0;JMP", "(FALSE" + self.labels + ")"])
        self._write_result("0")
        self._write(["(CONTINUE" + self.labels + ")"])
        self.labels = str(int(self.labels) + 1)

    def _write_unary(self, action):
        """ writes code which performs unary arithmetic action """
        self._write_result(action + "M")

    def _write_address_to_d(self, src, index, for_push):
        """ writes code which puts the address for push or pop to D """
        self._write(["@" + src, "D=M", "@" + str(index)] + for_push)

    def _write_value_to_d(self, src, is_address):
        """ writes code which puts the value for push or pop to D """
        self._write(["@" + src, "D=" + is_address])

    def _write_push_from_d(self):
        """ writes code which pushes D to RAM[SP] """
        self._write(["@SP", "A=M", "M=D", "@SP", "M=M+1"])

    def _write_pop_to_d(self):
        """ writes code which popes RAM[SP] to RAM[R13]"""
        self._write(["@R13", "M=D", "@SP", "M=M-1", "@SP", "A=M", "D=M", "@R13", "A=M", "M=D"])

    def _write_push_from_src(self, src, is_address):
        """ writes code which pushes RAM[src] to RAM[SP] """
        self._write_value_to_d(src, is_address)
        self._write_push_from_d()

    def _write_placement(self, num, dest):
        """ writes code which place RAM[R13-num] in RAM[dest] """
        self._write(["@" + str(num), "D=A", "@R13", "A=M-D", "D=M", "@" + dest, "M=D"])

    def write_arithmetic(self, command):
        """ writes code which performs arithmetic command """
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
        """ writes code which performs push or pop command """
        dic_address = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}
        dic_value = {"constant": str(index), "static": self.file_name + "." + str(index),
                     "temp": str(5 + index), "pointer": str(3 + index)}
        if segment in dic_address:
            for_push = ["D=D+A"] if command is CommandType.C_POP else ["A=D+A", "D=M"]
            self._write_address_to_d(dic_address[segment], index, for_push)
        else:
            is_address = "A" if command is CommandType.C_POP or segment == "constant" else "M"
            self._write_value_to_d(dic_value[segment], is_address)
        if command is CommandType.C_PUSH:
            self._write_push_from_d()
        elif command is CommandType.C_POP:
            self._write_pop_to_d()

    def write_init(self):
        """ writes code which inits the RAM """
        self._write(["@256", "D=A", "@SP", "M=D"])
        self.write_call("Sys.init", 0)

    def write_label(self, label):
        """ writes code which performs label command """
        self._write(["(" + label + ")"])

    def write_goto(self, label):
        """ writes code which performs goto command """
        self._write(["@" + label, "0;JMP"])

    def write_if(self, label):
        """ writes code which performs if-goto command """
        self._write(["@SP", "M=M-1", "A=M", "D=M", "@" + label, "D;JNE"])

    def write_function(self, function_name, num_vars):
        """ writes code which performs function command """
        self._write(["(" + function_name + ")"])
        for i in range(num_vars):
            self.write_push_pop(CommandType.C_PUSH, "constant", 0)

    def write_call(self, function_name, num_args):
        """ writes code which performs call command """
        ret = self.file_name + "$ret." + str(self.call_count)
        self.call_count += 1
        self._write_push_from_src(ret, "A")
        self._write_push_from_src("LCL", "M")
        self._write_push_from_src("ARG", "M")
        self._write_push_from_src("THIS", "M")
        self._write_push_from_src("THAT", "M")
        self._write(
            ["@5", "D=A", "@SP", "D=M-D", "@" + str(num_args), "D=D-A", "@ARG", "M=D", "@SP", "D=M", "@LCL", "M=D"])
        self.write_goto(function_name)
        self.write_label(ret)

    def write_return(self):
        """ writes code which performs return command """
        self._write(["@LCL", "D=M", "@R13", "M=D", "@5", "A=D-A", "D=M", "@R14", "M=D", "@SP", "M=M-1",
                     "@SP", "A=M", "D=M", "@ARG", "A=M", "M=D", "@ARG", "D=M", "@SP", "M=D+1"])
        self._write_placement(1, "THAT")
        self._write_placement(2, "THIS")
        self._write_placement(3, "ARG")
        self._write_placement(4, "LCL")
        self._write(["@R14", "A=M", "0;JMP"])

    def close(self):
        """ write code for close the program and close the file """
        self.file.close()
