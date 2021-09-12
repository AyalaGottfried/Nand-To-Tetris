import sys

from Code import Code
from CommandType import CommandType
from Parser import Parser
from SymbolTable import SymbolTable

parser = Parser(sys.argv[1])
symbol_table = SymbolTable()

if parser.command_type() is CommandType.L_COMMAND:
    if not symbol_table.contains(parser.symbol()):
        symbol_table.add_entry(parser.symbol(), parser.line_number + 1)

while parser.has_more_commands():
    parser.advance()
    if parser.command_type() == CommandType.L_COMMAND:
        if not symbol_table.contains(parser.symbol()):
            symbol_table.add_entry(parser.symbol(), parser.line_number + 1)

parser.file.close()

parser = Parser(sys.argv[1])
code = Code()
t_file = open(sys.argv[1].rsplit('.', 1)[0] + ".hack", "w")


def to_16(num):
    string = "{0:b}".format(num)
    while len(string) < 16:
        string = '0' + string
    return string


def write_command(address):
    if parser.command_type() is CommandType.A_COMMAND:
        if parser.symbol().isnumeric():
            t_file.write(to_16(int(parser.symbol())) + '\n')
        else:
            if not symbol_table.contains(parser.symbol()):
                symbol_table.add_entry(parser.symbol(), address)
                address += 1
            t_file.write(to_16(symbol_table.get_address(parser.symbol())) + '\n')
    elif parser.command_type() is CommandType.C_COMMAND:
        t_file.write('111' + str(code.comp(parser.comp())) + str(code.dest(parser.dest())) + str(
            code.jump(parser.jump())) + '\n')
    return address


var_address = 16
var_address = write_command(var_address)
while parser.has_more_commands():
    parser.advance()
    var_address = write_command(var_address)
t_file.close()
