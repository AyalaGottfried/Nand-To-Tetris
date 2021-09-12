import sys
import os

from CodeWriter import CodeWriter
from CommandType import CommandType
from Parser import Parser


def parse_file():
    """ parse one file from vm to asm """
    write_command()
    while parser.has_more_commands():
        parser.advance()
        write_command()


def write_command():
    """ translate one command """
    if parser.command_type() is CommandType.C_ARITHMETIC:
        command = parser.arg1()
        writer.write_arithmetic(command)
    elif parser.command_type() is CommandType.C_PUSH or parser.command_type() is CommandType.C_POP:
        command = parser.command_type()
        segment = parser.arg1()
        index = int(parser.arg2())
        writer.write_push_pop(command, segment, index)
    elif parser.command_type() is CommandType.C_LABEL:
        label = parser.arg1()
        writer.write_label(label)
    elif parser.command_type() is CommandType.C_GOTO:
        label = parser.arg1()
        writer.write_goto(label)
    elif parser.command_type() is CommandType.C_IF:
        label = parser.arg1()
        writer.write_if(label)
    elif parser.command_type() is CommandType.C_FUNCTION:
        function_name = parser.arg1()
        num_vars = parser.arg2()
        writer.write_function(function_name, int(num_vars))
    elif parser.command_type() is CommandType.C_RETURN:
        writer.write_return()
    else:
        function_name = parser.arg1()
        num_args = parser.arg2()
        writer.write_call(function_name, int(num_args))


if __name__ == '__main__':
    path = sys.argv[1]
    if os.path.isfile(path):
        parser = Parser(path)
        writer = CodeWriter(path.rsplit('.', 1)[0] + ".asm")
        parse_file()
        writer.close()

    elif os.path.isdir(path):
        files = os.listdir(path)
        writer = CodeWriter(path + "/" + os.path.basename(path) + ".asm")
        writer.write_init()
        for file in files:
            if file.rsplit('.', 1)[1] == "vm":
                parser = Parser(path + "/" + file)
                writer.set_file_name(file.rsplit('.', 1)[0])
                parse_file()
        writer.close()
