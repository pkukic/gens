from generative_tree import GenerativeTree
from scope import Scope
from scope_structure import ScopeStructure
from FunctionType import FunctionType
from consts import *
from functions import Functions
from global_variables import GlobalVariables
import sys


INPUT_FILE_PATH = "./testovi/40_func_decl/test.in"


def main():
    read_from_stdin = 1
    if read_from_stdin:
        input = [line.rstrip() for line in sys.stdin.readlines()]
    else:
        with open(INPUT_FILE_PATH, 'r') as file:
            input = [line.rstrip() for line in file.readlines()]
    functions = Functions()
    global_variables = GlobalVariables()
    global_scope = Scope(None, GLOBAL)
    scope_structure = ScopeStructure(global_scope)
    gen_tree = GenerativeTree(input, scope_structure, functions, global_variables)
    # error = gen_tree.root_node.provjeri()
    # if error:
    #     print(error)
    # else:
    #     defs = gen_tree.root_node.scope_structure.all_functions_definitions()
    #     decs = gen_tree.root_node.scope_structure.all_functions_declarations()
    #     required_main = ('main', FunctionType([VOID], INT))
    #     if required_main not in defs.items() or required_main not in decs.items():
    #         print('main')
    #     elif defs != decs:
    #         print('funkcija')
    output = gen_tree.root_node.generate_output()

    mnozenje_kod = ""
    mnozenje_kod += "PUTA\n"
    mnozenje_kod += "\t\tLOAD R1, (R7+8)\n"
    mnozenje_kod += "\t\tLOAD R2, (R7+4)\n"
    mnozenje_kod += "\t\tMOVE 0, R6\n"
    mnozenje_kod += "\t\tXOR R1, R2, R3\n"
    mnozenje_kod += "TEST_1\n"
    mnozenje_kod += "\t\tOR R1, R1, R1\n"
    mnozenje_kod += "\t\tJR_P TEST_2\n"
    mnozenje_kod += "NEGAT_1\n"
    mnozenje_kod += "\t\tXOR R1, -1, R1\n"
    mnozenje_kod += "\t\tADD R1, 1, R1\n"
    mnozenje_kod += "TEST_2\n"
    mnozenje_kod += "\t\tOR R2, R2, R2\n"
    mnozenje_kod += "\t\tJR_P PETLJA\n"
    mnozenje_kod += "NEGAT_2\n"
    mnozenje_kod += "\t\tXOR R2, -1, R2\n"
    mnozenje_kod += "\t\tADD R2, 1, R2\n"
    mnozenje_kod += "PETLJA\n"
    mnozenje_kod += "\t\tADD R1, R6, R6\n"
    mnozenje_kod += "\t\tSUB R2, 1, R2\n"
    mnozenje_kod += "\t\tJR_NZ PETLJA\n"
    mnozenje_kod += "PREDZNAK\n"
    mnozenje_kod += "\t\tROTL R3, 1, R3\n"
    mnozenje_kod += "\t\tJR_NC GOTOVO\n"
    mnozenje_kod += "RAZLICIT\n"
    mnozenje_kod += "\t\tXOR R6, -1, R6\n"
    mnozenje_kod += "\t\tADD R6, 1, R6\n"
    mnozenje_kod += "GOTOVO\n"
    mnozenje_kod += "\t\tLOAD R1, (R7+8)\n"
    mnozenje_kod += "\t\tLOAD R2, (R7+4)\n"
    mnozenje_kod += "\t\tRET\n"

    output += mnozenje_kod

    with open("a.frisc", "w") as frisc:
        frisc.write(output)
            

if __name__ == '__main__':
    main()