from generative_tree import GenerativeTree
from scope import Scope
from scope_structure import ScopeStructure
from FunctionType import FunctionType
from consts import *
from functions import Functions
from global_variables import GlobalVariables
import sys


INPUT_FILE_PATH = "./testovi/05_plus/test.in"
# INPUT_FILE_PATH = "/home/filip/Work/FER/5_semestar/ppj/labosi/sem/temp.txt"


def main():
    # with open(INPUT_FILE_PATH, 'r') as file:
        # input = [line.rstrip() for line in file.readlines()]
    input = [line.rstrip() for line in sys.stdin.readlines()]
    # make the generative tree from the input
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