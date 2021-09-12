from CommandType import CommandType


class Parser:
    def __init__(self, file_name):
        self.file = open(file_name, "r")
        self.code = self.file.readlines()
        self.current = 0
        self._clean_line()
        self.line = self.code[self.current].split()
        self.file.close()

    def _clean_line(self):
        """ go to the next non-space line and clean it from spaces and remarks """
        self.code[self.current] = self.code[self.current].split("//")[0].split("\n")[0]
        while self.code[self.current] == "" or self.code[self.current].isspace():
            self.current += 1
            self.code[self.current] = self.code[self.current].split("//")[0].split("\n")[0]

    def has_more_commands(self):
        """ return if the code has more commands """
        return len(self.code) - 1 > self.current

    def advance(self):
        """ advance the parser to the next command """
        self.current += 1
        self._clean_line()
        self.line = self.code[self.current].split()

    def command_type(self):
        """ return the type of the current command """
        arithmetics = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
        if self.line[0] in arithmetics:
            return CommandType.C_ARITHMETIC
        if self.line[0] == "if-goto":
            return CommandType.C_IF
        return CommandType["C_"+self.line[0].upper()]

    def arg1(self):
        """ return the first argument of the current command """
        return self.line[0] if self.command_type() is CommandType.C_ARITHMETIC else self.line[1]

    def arg2(self):
        """ return the second argument of the current command """
        return self.line[2]
