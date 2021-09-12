from CommandType import CommandType


class Parser:
    def __init__(self, file_name):
        self.file = open(file_name, "r")
        self.code_lines = self.file.readlines()
        self.current_command = 0
        self.__clean_line()
        self.line_number = 0

    def __clean_line(self):
        self.code_lines[self.current_command] = \
            self.code_lines[self.current_command].replace(" ", "").split("//")[0].split("\n")[0]
        while self.code_lines[self.current_command] == "" or self.code_lines[self.current_command].isspace():
            self.current_command += 1
            self.code_lines[self.current_command] = \
                self.code_lines[self.current_command].replace(" ", "").split("//")[0].split("\n")[0]

    def has_more_commands(self):
        return len(self.code_lines) - 1 > self.current_command

    def advance(self):
        self.current_command += 1
        self.__clean_line()
        if self.command_type() != CommandType.L_COMMAND:
            self.line_number += 1

    def command_type(self):
        return CommandType.A_COMMAND if self.code_lines[self.current_command][0] == '@' else CommandType.L_COMMAND if \
            self.code_lines[self.current_command][0] == '(' else CommandType.C_COMMAND

    def symbol(self):
        return self.code_lines[self.current_command][1:] if self.command_type() is CommandType.A_COMMAND else \
            self.code_lines[self.current_command][1:-1]

    def dest(self):
        s = self.code_lines[self.current_command].split('=')
        return "" if len(s) == 1 else s[0]

    def comp(self):
        s = self.code_lines[self.current_command].split('=')
        return self.code_lines[self.current_command].split(';')[0] if len(s) == 1 else s[1].split(';')[0]

    def jump(self):
        s = self.code_lines[self.current_command].split(';')
        return "" if len(s) == 1 else s[1]
