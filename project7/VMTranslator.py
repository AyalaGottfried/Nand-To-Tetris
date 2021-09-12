import sys

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


if __name__ == '__main__':
    path = sys.argv[1]
    parser = Parser(path)
    writer = CodeWriter(path.rsplit('.', 1)[0] + ".asm")
    parse_file()
    writer.close()
