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

    dijeljenje_kod = ""
    dijeljenje_kod += "DIJELI\n"
    dijeljenje_kod += "\t\tLOAD R1, (R7+8)\n"
    dijeljenje_kod += "\t\tLOAD R2, (R7+4)\n"
    dijeljenje_kod += "\t\tMOVE 0, R6\n"
    dijeljenje_kod += "\t\tMOVE 0, R5\n"
    dijeljenje_kod += "\t\tCMP R2, 0\n"
    dijeljenje_kod += "\t\tJP_EQ IZADJI\n"
    dijeljenje_kod += "PRVI\n"
    dijeljenje_kod += "\t\tCMP R1, 0\n"
    dijeljenje_kod += "\t\tJP_SGE DRUGI\n"
    dijeljenje_kod += "\t\tXOR R5, 1, R5\n"
    dijeljenje_kod += "\t\tXOR R1, -1, R1\n"
    dijeljenje_kod += "\t\tADD R1, 1, R1\n"
    dijeljenje_kod += "DRUGI\n"
    dijeljenje_kod += "\t\tCMP R2, 0\n"
    dijeljenje_kod += "\t\tJP_SGE LOOPD\n"
    dijeljenje_kod += "\t\tXOR R5, 1, R5\n"
    dijeljenje_kod += "\t\tXOR R2, -1, R2\n"
    dijeljenje_kod += "\t\tADD R2, 1, R2\n"
    dijeljenje_kod += "LOOPD\n"
    dijeljenje_kod += "\t\tCMP R1, R2\n"
    dijeljenje_kod += "\t\tJP_SLT IZADJI\n"
    dijeljenje_kod += "\t\tSUB R1, R2, R1\n"
    dijeljenje_kod += "\t\tADD R6, 1, R6\n"
    dijeljenje_kod += "\t\tJP LOOPD\n"
    dijeljenje_kod += "IZADJI\n"
    dijeljenje_kod += "\t\tCMP R5, 1\n"
    dijeljenje_kod += "\t\tJP_EQ KOMPL\n"
    dijeljenje_kod += "\t\tJP_NE BAS_IZADJI\n"
    dijeljenje_kod += "KOMPL\n"
    dijeljenje_kod += "\t\tXOR R6, -1, R6\n"
    dijeljenje_kod += "\t\tADD R6, 1, R6\n"
    dijeljenje_kod += "\t\tJP BAS_IZADJI\n"
    dijeljenje_kod += "BAS_IZADJI\n"
    dijeljenje_kod += "\t\tLOAD R1, (R7+8)\n"
    dijeljenje_kod += "\t\tLOAD R2, (R7+4)\n"
    dijeljenje_kod += "\t\tRET\n"

    modulo_kod = ""
    modulo_kod += "MODULO\n"
    modulo_kod += "\t\tLOAD R1, (R7+8)\n"
    modulo_kod += "\t\tLOAD R2, (R7+4)\n"
    modulo_kod += "\t\tCMP R2, 0\n"
    modulo_kod += "\t\tJP_SLE IZADJI_MODULO\n"
    modulo_kod += "\t\tCMP R1, 0\n"
    modulo_kod += "\t\tJP_SLT IZADJI_MODULO\n"
    modulo_kod += "\t\tMOVE R1, R5\n"
    modulo_kod += "\t\tCALL DIJELI\n"
    modulo_kod += "\t\tMOVE R6, R1\n"
    modulo_kod += "\t\tCALL PUTA\n"
    modulo_kod += "\t\tSUB R5, R6, R5\n"
    modulo_kod += "\t\tMOVE R5, R6\n"
    modulo_kod += "IZADJI_MODULO\n"
    modulo_kod += "\t\tLOAD R1, (R7+8)\n"
    modulo_kod += "\t\tLOAD R2, (R7+4)\n"
    modulo_kod += "\t\tRET\n"

    output += mnozenje_kod
    output += dijeljenje_kod
    output += modulo_kod

    with open("a.frisc", "w") as frisc:
        frisc.write(output)
            

if __name__ == '__main__':
    main()