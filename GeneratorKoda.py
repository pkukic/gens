from generative_tree import GenerativeTree
from scope import Scope
from scope_structure import ScopeStructure
from FunctionType import FunctionType
from consts import *
from functions import Functions
from global_variables import GlobalVariables
import sys


INPUT_FILE_PATH = "./testovi/12_27_rek/test.in"
# INPUT_FILE_PATH = "/home/filip/Work/FER/5_semestar/ppj/labosi/sem/temp.txt"


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
    with open("a.frisc", "w") as frisc:
        frisc.write(output)
            

if __name__ == '__main__':
    main()