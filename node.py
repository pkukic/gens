from consts import *
from utils import *
from scope_structure import ScopeStructure
from scope import Scope
from FunctionType import FunctionType
from functions import Function


class Node():

    name = ""
    parent_node = None
    children = []
    leaf_node = False
    scope_structure = None
    root_node = False

    # params for semantic analysis
    tip = None
    ntip = None
    l_izraz = None
    tipovi = []
    identifikatori = []
    vrijednost = None
    br_elem = None


    def __init__(self, name: str, parent_node, scope_structure: ScopeStructure,
                functions, global_variables, root_node=False):
        self.functions = functions
        self.global_variables = global_variables
        self.root_node = root_node
        self.name = name
        self.parent_node = parent_node
        self.scope_structure = scope_structure
        self.children = list()
        # node
        if self.name.startswith("<"):
            self.leaf_node = False
        # leaf
        else:
            self.name = name.split(' ')[0]
            self.line = name.split(' ')[1]
            self.lex = name.split(' ')[2]
            self.leaf_node = True
        
        self.tip = None
        self.ntip = None
        self.l_izraz = None
        self.tipovi = []
        self.identifikatori = []
        self.vrijednost = None
        self.br_elem = None

        if self.name == BROJ:
            self.vrijednost = int(self.lex)
        return
    

    def add_child(self, child_node):
        self.children.append(child_node)
        return
    

    def __str__(self):
        return self.name
    

    def __repr__(self):
        return self.name


    def print(self, depth: int):
        print(" " * depth + self.name)
        for child in self.children:
            child.print(depth + 1)
        return
    

    def right_side(self, *args):
        if len(args) != len(self.children):
            return False
        for i in range(len(self.children)):
            if self.children[i].name != args[i]:
                return False
        return True


    def is_argument(self):
        if not self.parent_node:
            return False
        if self.parent_node.name == LISTA_ARGUMENATA:
            return True
        return self.parent_node.is_argument()


    def in_loop(self):
        p = self.parent_node
        allowed_parents = [
            NAREDBA, 
            LISTA_NAREDBI, 
            SLOZENA_NAREDBA, 
            NAREDBA_GRANANJA
        ]
        if p.name != NAREDBA_PETLJE:
            if p.name not in allowed_parents:
                return False
            return p.in_loop()
        return True

    
    def nesting_function_type(self):
        p = self.parent_node
        allowed_parents = [
            NAREDBA,
            LISTA_NAREDBI,
            SLOZENA_NAREDBA,
            NAREDBA_GRANANJA,
            NAREDBA_PETLJE
        ]
        if p.name != DEFINICIJA_FUNKCIJE:
            if p.name not in allowed_parents:
                return None
            return p.nesting_function_type()
        return p.tip.return_type


    def goes_to_niz_znakova(self):
        if self.name == NIZ_ZNAKOVA:
            return (True, self.br_elem)
        if self.leaf_node:
            return (False, None)
        if len(self.children) > 1:
            return (False, None)
        return self.children[0].goes_to_niz_znakova()
            

    # very important function!!
    # call it if an error is spotted
    def error(self):
        output_string = self.name + " ::="
        for child in self.children:
            output_string += (" " + child.name)
            if (child.leaf_node):
                output_string += (f"({child.line},{child.lex})")
        output_string += "\n"
        return output_string
    

    def generate_output(self, scope=None, lista_identifikatora=None, lista_tipova=None, ntip=None, inside_if=False):
        output = ""
        if (self.name == PRIMARNI_IZRAZ):
            output = self.primarni_izraz()
        elif (self.name == POSTFIKS_IZRAZ):
            output = self.postfiks_izraz()
        elif (self.name == LISTA_ARGUMENATA):
            output = self.lista_argumenata()
        elif (self.name == UNARNI_IZRAZ):
            output = self.unarni_izraz()
        elif (self.name == CAST_IZRAZ):
            output = self.cast_izraz()
        elif (self.name == IME_TIPA):
            output = self.ime_tipa()
        elif (self.name == SPECIFIKATOR_TIPA):
            output = self.specifikator_tipa()
        elif (self.name == MULTIPLIKATIVNI_IZRAZ):
            output = self.multiplikativni_izraz()
        elif (self.name == ADITIVNI_IZRAZ):
            output = self.aditivni_izraz()
        elif (self.name == ODNOSNI_IZRAZ):
            output = self.odnosni_izraz()
        elif (self.name == JEDNAKOSNI_IZRAZ):
            output = self.jednakosni_izraz()
        elif (self.name == BIN_I_IZRAZ):
            output = self.bin_i_izraz()
        elif (self.name == BIN_XILI_IZRAZ):
            output = self.bin_xili_izraz()
        elif (self.name == BIN_ILI_IZRAZ):
            output = self.bin_ili_izrazi()
        elif (self.name == LOG_I_IZRAZ):
            output = self.log_i_izraz()
        elif (self.name == LOG_ILI_IZRAZ):
            output = self.log_ili_izraz(inside_if=inside_if)
        elif (self.name == IZRAZ_PRIDRUZIVANJA):
            output = self.izraz_pridruzivanja(inside_if=inside_if)
        elif (self.name == IZRAZ):
            output = self.izraz(inside_if=inside_if)

        elif (self.name == SLOZENA_NAREDBA):
            output = self.slozena_naredba(scope=scope, 
                                            lista_identifikatora=lista_identifikatora, 
                                            lista_tipova=lista_tipova)
        elif (self.name == LISTA_NAREDBI):
            output = self.lista_naredbi()
        elif (self.name == NAREDBA):
            output = self.naredba()
        elif (self.name == IZRAZ_NAREDBA):
            output = self.izraz_naredba()
        elif (self.name == NAREDBA_GRANANJA):
            output = self.naredba_grananja()
        elif (self.name == NAREDBA_PETLJE):
            output = self.naredba_petlje()
        elif (self.name == NAREDBA_SKOKA):
            output = self.naredba_skoka()

        elif (self.name == PRIJEVODNA_JEDINICA):
            output = self.prijevodna_jedinica()
        elif (self.name == VANJSKA_DEKLARACIJA):
            output = self.vanjska_deklaracija()
        elif (self.name == DEFINICIJA_FUNKCIJE):
            output = self.definicija_funkcije()
        elif (self.name == LISTA_PARAMETARA):
            output = self.lista_parametara()
        elif (self.name == DEKLARACIJA_PARAMETRA):
            output = self.deklaracija_parametra()
        elif (self.name == LISTA_DEKLARACIJA):
            output = self.lista_deklaracija()

        elif (self.name == DEKLARACIJA):
            output = self.deklaracija()
        elif (self.name == LISTA_INIT_DEKLARATORA):
            output = self.lista_init_deklaratora(ntip)
        elif (self.name == INIT_DEKLARATOR):
            output = self.init_deklarator(ntip)
        elif (self.name == IZRAVNI_DEKLARATOR):
            output = self.izravni_deklarator(ntip)
        elif (self.name == INICIJALIZATOR):
            output = self.inicijalizator()        
        elif (self.name == LISTA_IZRAZA_PRIDRUZIVANJA):
            output = self.lista_izraza_pridruzivanja()

        elif (self.name == UNARNI_OPERATOR):
            output = self.unarni_operator()

        return output
    

    # <primarni_izraz>
    def primarni_izraz(self):
        if self.right_side(IDN):

            self.tip = self.scope_structure.type_of_idn_in_scope(self.children[0].lex)
            self.l_izraz = self.scope_structure.l_izraz_of_idn_in_scope(self.children[0].lex)

            if isinstance(self.tip, FunctionType):
                if self.tip.arguments_types == [VOID]:
                    return f"\t\tCALL F_{self.children[0].lex.upper()}\n"
                else:
                    return f" F_{self.children[0].lex.upper()}"

            if self.scope_structure.idn_name_not_in_local_scopes(self.children[0].lex):
                return f"\t\tLOAD R6, (G_{(self.children[0].lex).upper()})\n"
            else:
                if self.functions.current_function().is_local_var(self.children[0].lex):
                    stack_offset = self.functions.current_function().local_var_offset(self.children[0].lex)
                else:
                    scope_container = self.scope_structure.return_scope_containg_name(self.children[0].lex)
                    stack_offset = scope_container.get_variable_offset(self.children[0].lex)
                return f"\t\tLOAD R6, (R7+{make_frisc_hex(stack_offset)})\n"

        elif self.right_side(BROJ):
            # if self.is_argument():
            #     self.global_variables.add_line(f"K_{self.global_variables.size()}\t\tDW %D {self.children[0].lex}")
            #     output = f"\t\tLOAD R6, (K_{self.global_variables.size() - 1})\n"
            #     output += f"\t\tPUSH R6\n"
            #     return output
            self.tip = BROJ
            self.l_izraz = 0
            if self.scope_structure.current_scope.is_global():
                return "%D " + self.children[0].lex
            else:
                self.global_variables.add_line(f"K_{self.global_variables.size()}\t\tDW %D {self.children[0].lex}")
                return f"\t\tLOAD R6, (K_{self.global_variables.size() - 1})\n"
            
        elif self.right_side(ZNAK):
            if not check_char(self.children[0].lex):    
                return self.error()
            self.tip = CHAR
            self.l_izraz = 0

        elif self.right_side(NIZ_ZNAKOVA):
            if not check_string(self.children[0].lex):
                return "|" + self.children[0].lex + "|" + self.error()
            self.tip = NIZ_CONST_CHAR
            self.l_izraz = 0

        elif self.right_side(L_ZAGRADA, IZRAZ, D_ZAGRADA):
            output = self.children[1].generate_output()
            # if error:
            #     return error
            self.tip = self.children[1].tip
            self.l_izraz = self.children[1].l_izraz
        return output
    

    # <postfiks_izraz>
    def postfiks_izraz(self):
        if self.right_side(PRIMARNI_IZRAZ):
            output = self.children[0].generate_output()
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz
        
        elif self.right_side(POSTFIKS_IZRAZ, L_UGL_ZAGRADA, IZRAZ, D_UGL_ZAGRADA):
            # <postfiks_izraz>
            output = self.children[0].generate_output()
            # if error:
            #     return error
            # if not is_niz_x(self.children[0].tip):
            #     return self.error()
            # <izraz>
            output = self.children[2].generate_output()
            # if error:
            #     return error
            # if not implicit_cast(self.children[2].tip, INT):
            #     return self.error()

            output 
            
            self.tip = remove_niz_from_niz_x(self.children[0].tip)
            if is_const_x(self.tip):
                self.l_izraz = 0
            else:
                self.l_izraz = 1
            return output

        elif self.right_side(POSTFIKS_IZRAZ, L_ZAGRADA, D_ZAGRADA):
            output = self.children[0].generate_output()
            # if error:
            #     return error
            ft = self.children[0].tip
            # if not ft.arguments_types == [VOID]:
            #     self.error()
            self.tip = ft.return_type
            self.l_izraz = 0
            return output

        elif self.right_side(POSTFIKS_IZRAZ, L_ZAGRADA, LISTA_ARGUMENATA, D_ZAGRADA):
            function_name = self.children[0].generate_output()
            # if error:
            #     return error
            output = self.children[2].generate_output()
            # if error:
            #     return error
            # required_types_list = self.children[0].tip.arguments_types
            # current_types_list = self.children[2].tipovi
            # n = len(required_types_list)
            # m = len(current_types_list)
            # if n != m:
            #     return self.error()
            # for i in range(n):
            #     if not implicit_cast(current_types_list[i], required_types_list[i]):
            #         self.error()
            self.tip = self.children[0].tip.return_type
            self.l_izraz = 0
            output += f"\t\tCALL {function_name}\n"
            # count the number of PUSH
            no_args = output.count("PUSH")
            output += f"\t\tADD R7, %D {no_args * 4}, R7\n"
            return output


        elif self.right_side(POSTFIKS_IZRAZ, OP_INC):
            output = self.children[0].generate_output()
            # works only if output is of type 'LOAD R6, (R7+4)'
            variable_address = output.split(" ")[2]
            output += "\t\tMOVE R6, R1\n"
            output += "\t\tMOVE 1, R2\n"
            output += "\t\tADD R1, R2, R3\n"
            output += f"\t\tSTORE R3, {variable_address}\n"
            # if error:
            #     return error
            # if self.children[0].l_izraz != 1:
            #     return self.error()
            # if not implicit_cast(self.children[0].tip, INT):
            #     return self.error()
            self.tip = INT
            self.l_izraz = 0
            
        elif self.right_side(POSTFIKS_IZRAZ, OP_DEC):
            output = self.children[0].generate_output()
            # works only if output is of type 'LOAD R6, (R7+4)'
            variable_address = output.split(" ")[2]
            output += "\t\tMOVE R6, R1\n"
            output += "\t\tMOVE 1, R2\n"
            output += "\t\SUB R1, R2, R3\n"
            output += f"\t\tSTORE R3, {variable_address}\n"
            # if error:
            #     return error
            # if self.children[0].l_izraz != 1:
            #     return self.error()
            # if not implicit_cast(self.children[0].tip, INT):
            #     return self.error()
            self.tip = INT
            self.l_izraz = 0
        return output
        
    
    # <lista_argumenata>
    def lista_argumenata(self):
        if self.right_side(IZRAZ_PRIDRUZIVANJA):
            output = self.children[0].generate_output()
            # if error:
            #     return error
            self.tipovi = [self.children[0].tip]
            output += "\t\tPUSH R6\n"

        elif self.right_side(LISTA_ARGUMENATA, ZAREZ, IZRAZ_PRIDRUZIVANJA):
            output = self.children[0].generate_output()
            # if error:
            #     return error
            output += self.children[2].generate_output()
            output += "\t\tPUSH R6\n"
            # if error:
            #     return error
            self.tipovi = self.children[0].tipovi.copy()
            self.tipovi.append(self.children[2].tip)
        return output
    

    # <unarni_izraz>
    def unarni_izraz(self):
        if self.right_side(POSTFIKS_IZRAZ):
            output = self.children[0].generate_output()
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz

        elif self.right_side(OP_INC, UNARNI_IZRAZ):
            output = self.children[1].generate_output()
            # work only if output like 'LOAD R6, (R7+4)'
            variable_address = output.split(" ")[2]
            output += "\t\tMOVE R6, R1\n"
            output += "\t\tMOVE 1, R2\n"
            output += "\t\tADD R1, R2, R6\n"
            output += f"\t\tSTORE R6, {variable_address}\n"
            # if error:
            #     return error
            # if self.children[1].l_izraz != 1:
            #     return self.error()
            # if not implicit_cast(self.children[1].tip, INT):
            #     return self.error()
            self.tip = INT
            self.l_izraz = 0

        elif self.right_side(OP_DEC, UNARNI_IZRAZ):
            output = self.children[1].generate_output()
            # work only if output like 'LOAD R6, (R7+4)'
            variable_address = output.split(" ")[2]
            output += "\t\tMOVE R6, R1\n"
            output += "\t\tMOVE 1, R2\n"
            output += "\t\SUB R1, R2, R6\n"
            output += f"\t\tSTORE R6, {variable_address}\n"
            # if error:
            #     return error
            # if self.children[1].l_izraz != 1:
            #     return self.error()
            # if not implicit_cast(self.children[1].tip, INT):
            #     return self.error()
            self.tip = INT
            self.l_izraz = 0

        elif self.right_side(UNARNI_OPERATOR, CAST_IZRAZ):
            output = self.children[1].generate_output()
            output += self.children[0].generate_output()
            # if error:
            #     return error
            # if not implicit_cast(self.children[1].tip, INT):
            #     return self.error()
            # if self.children[0].name == MINUS:
            #     output += "\t\tXOR R6, -1, R6\n"
            #     output += "\t\tADD R6, 1, R6\n"
            self.tip = INT
            self.l_izraz = 0
        return output
    

    # <unarni_operator>
    def unarni_operator(self):
        # nothing needs to be checked here
        output = ""
        if self.children[0].name == MINUS:
            output += "\t\tXOR R6, -1, R6\n"
            output += "\t\tADD R6, 1, R6\n"
        if self.children[0].name == OP_TILDA:
            output += "\t\tXOR R6, -1, R6\n"
        if self.children[0].name == OP_NEG:
            output += "\t\tXOR R6, 1, R6\n"
        return output
    

    # <cast_izraz>
    def cast_izraz(self):
        if self.right_side(UNARNI_IZRAZ):
            output = self.children[0].generate_output()
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz
        
        elif self.right_side(L_ZAGRADA, IME_TIPA, D_ZAGRADA, CAST_IZRAZ):
            error = self.children[1].generate_output()
            if error:
                return error
            error = self.children[3].generate_output()
            if error:
                return error
            if not explicit_cast(self.children[3].tip, self.children[1].tip):
                return self.error()
            self.tip = self.children[1].tip
            self.l_izraz = 0
        return output
    

    # <ime_tipa>
    def ime_tipa(self):
        if self.right_side(SPECIFIKATOR_TIPA):
            error = self.children[0].generate_output()
            if error:
                return error
            self.tip = self.children[0].tip
        
        elif self.right_side(KR_CONST, SPECIFIKATOR_TIPA):
            error = self.children[1].generate_output()
            if error:
                return error
            if self.children[1].tip == VOID:
                return self.error()
            self.tip = make_const(self.children[1].tip)
        return ""
    

    # <specifikator_tipa>
    def specifikator_tipa(self):
        if self.right_side(KR_VOID):
            self.tip = VOID
        elif self.right_side(KR_CHAR):
            self.tip = CHAR
        elif self.right_side(KR_INT):
            self.tip = INT
        return ""
    

    # <multiplikativni_izraz>
    def multiplikativni_izraz(self):
        if self.right_side(CAST_IZRAZ):
            output = self.children[0].generate_output()
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz
        
        elif (self.right_side(MULTIPLIKATIVNI_IZRAZ, OP_PUTA, CAST_IZRAZ) or
                self.right_side(MULTIPLIKATIVNI_IZRAZ, OP_DIJELI, CAST_IZRAZ) or
                self.right_side(MULTIPLIKATIVNI_IZRAZ, OP_MOD, CAST_IZRAZ)):
            
            if self.right_side(MULTIPLIKATIVNI_IZRAZ, OP_PUTA, CAST_IZRAZ):
                output = self.children[0].generate_output()
                output += "\t\tMOVE R6, R1\n"
                output += self.children[2].generate_output()
                output += "\t\tMOVE R6, R2\n"
                output += "\t\tPUSH R1\n"
                output += "\t\tPUSH R2\n"
                output += "\t\tCALL PUTA\n"
                output += "\t\tADD R7, 8, R7\n"

            if self.right_side(MULTIPLIKATIVNI_IZRAZ, OP_DIJELI, CAST_IZRAZ):
                output = self.children[0].generate_output()
                output += "\t\tMOVE R6, R1\n"
                output += self.children[2].generate_output()
                output += "\t\tMOVE R6, R2\n"
                output += "\t\tPUSH R1\n"
                output += "\t\tPUSH R2\n"
                output += "\t\tCALL DIJELI\n"
                output += "\t\tADD R7, 8, R7\n"

            if self.right_side(MULTIPLIKATIVNI_IZRAZ, OP_MOD, CAST_IZRAZ):
                output = self.children[0].generate_output()
                output += "\t\tMOVE R6, R1\n"
                output += self.children[2].generate_output()
                output += "\t\tMOVE R6, R2\n"
                output += "\t\tPUSH R1\n"
                output += "\t\tPUSH R2\n"
                output += "\t\tCALL MODULO\n"
                output += "\t\tADD R7, 8, R7\n"

            # error = self.children[0].generate_output()
            # if error:
            #     return error
            # if not implicit_cast(self.children[0].tip, INT):
            #     return self.error()
            # error = self.children[2].generate_output()
            # if error:
            #     return error
            # if not implicit_cast(self.children[2].tip, INT):
            #     return self.error()
            self.tip = INT
            self.l_izraz = 0
        return output
    

    # <aditivni_izraz>
    def aditivni_izraz(self):
        if self.right_side(MULTIPLIKATIVNI_IZRAZ):
            output = self.children[0].generate_output()
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz

        elif (self.right_side(ADITIVNI_IZRAZ, PLUS, MULTIPLIKATIVNI_IZRAZ) or 
                self.right_side(ADITIVNI_IZRAZ, MINUS, MULTIPLIKATIVNI_IZRAZ)):
            # error = self.children[0].generate_output()
            # if error:
            #     return error
            # if not implicit_cast(self.children[0].tip, INT):
            #     return self.error()
            # error = self.children[2].generate_output()
            # if error:
            #     return error
            # if not implicit_cast(self.children[2].tip, INT):
            #     return self.error()
            self.tip = INT
            self.l_izraz = 0
            # output = self.children[0].generate_output()
            # output += "\t\tMOVE R6, R1\n"
            # output += self.children[2].generate_output()
            # output += "\t\tMOVE R6, R2\n"

            # if self.right_side(ADITIVNI_IZRAZ, PLUS, MULTIPLIKATIVNI_IZRAZ):
            #     output += "\t\tADD R1, R2, R6\n"
            # else:
            #     output += "\t\tSUB R1, R2, R6\n"
            first_operand_mem = self.global_variables.size()
            self.global_variables.add_line(f"G_{first_operand_mem}\t\tDW 0")
            output = self.children[0].generate_output()
            output += f"\t\tSTORE R6, (G_{first_operand_mem})\n"

            second_operand_mem = self.global_variables.size()
            self.global_variables.add_line(f"G_{second_operand_mem}\t\tDW 0")
            output += self.children[2].generate_output()
            output += f"\t\tSTORE R6, (G_{second_operand_mem})\n"

            output += f"\t\tLOAD R1, (G_{first_operand_mem})\n"
            output += f"\t\tLOAD R2, (G_{second_operand_mem})\n"

            if self.right_side(ADITIVNI_IZRAZ, PLUS, MULTIPLIKATIVNI_IZRAZ):
                output += "\t\tADD R1, R2, R6\n"
            else:
                output += "\t\tSUB R1, R2, R6\n"
        return output
    

    # <odnosni_izraz>
    def odnosni_izraz(self):
        if self.right_side(ADITIVNI_IZRAZ):
            output = self.children[0].generate_output()
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz
        
        elif (self.right_side(ODNOSNI_IZRAZ, OP_LT, ADITIVNI_IZRAZ) or
                self.right_side(ODNOSNI_IZRAZ, OP_GT, ADITIVNI_IZRAZ) or
                self.right_side(ODNOSNI_IZRAZ, OP_LTE, ADITIVNI_IZRAZ) or
                self.right_side(ODNOSNI_IZRAZ, OP_GTE, ADITIVNI_IZRAZ)):

            first_operand_mem = self.global_variables.size()
            self.global_variables.add_line(f"G_{first_operand_mem}\t\tDW 0")
            output = self.children[0].generate_output()
            output += f"\t\tSTORE R6, (G_{first_operand_mem})\n"
    
            second_operand_mem = self.global_variables.size()
            self.global_variables.add_line(f"G_{second_operand_mem}\t\tDW 0")
            output += self.children[2].generate_output()
            output += f"\t\tSTORE R6, (G_{second_operand_mem})\n"

            output += f"\t\tLOAD R1, (G_{first_operand_mem})\n"
            output += f"\t\tLOAD R2, (G_{second_operand_mem})\n"
            output += f"\t\tCMP R1, R2\n"
            label_index = UniqueCounter.get_unique()

            if self.right_side(ODNOSNI_IZRAZ, OP_LT, ADITIVNI_IZRAZ):

                output += f"\t\tJP_SLT T_{label_index}\n"
                output += f"\t\tMOVE 0, R6\n"
                output += f"\t\tJP I_{label_index}\n"
                output += f"T_{label_index}\n"
                output += f"\t\tMOVE 1, R6\n"
                output += f"I_{label_index}\n"

            elif self.right_side(ODNOSNI_IZRAZ, OP_GT, ADITIVNI_IZRAZ):

                output += f"\t\tJP_SGT T_{label_index}\n"
                output += f"\t\tMOVE 0, R6\n"
                output += f"\t\tJP I_{label_index}\n"
                output += f"T_{label_index}\n"
                output += f"\t\tMOVE 1, R6\n"
                output += f"I_{label_index}\n"

            elif self.right_side(ODNOSNI_IZRAZ, OP_LTE, ADITIVNI_IZRAZ):

                output += f"\t\tJP_SLE T_{label_index}\n"
                output += f"\t\tMOVE 0, R6\n"
                output += f"\t\tJP I_{label_index}\n"
                output += f"T_{label_index}\n"
                output += f"\t\tMOVE 1, R6\n"
                output += f"I_{label_index}\n"

            elif self.right_side(ODNOSNI_IZRAZ, OP_GTE, ADITIVNI_IZRAZ):

                output += f"\t\tJP_SGE T_{label_index}\n"
                output += f"\t\tMOVE 0, R6\n"
                output += f"\t\tJP I_{label_index}\n"
                output += f"T_{label_index}\n"
                output += f"\t\tMOVE 1, R6\n"
                output += f"I_{label_index}\n"

            # output = self.children[0].generate_output()
            
            # if error:
            #     return error
            # if not implicit_cast(self.children[0].tip, INT):
            #     return self.error()
            # output += self.children[2].generate_output()

            # if error:
            #     return error
            # if not implicit_cast(self.children[2].tip, INT):
            #     return self.error()
            self.tip = INT
            self.l_izraz = 0
        return output
    

    # <jednakosni_izraz>
    def jednakosni_izraz(self):
        if self.right_side(ODNOSNI_IZRAZ):
            output = self.children[0].generate_output()
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz
        
        elif (self.right_side(JEDNAKOSNI_IZRAZ, OP_EQ, ODNOSNI_IZRAZ) or
                self.right_side(JEDNAKOSNI_IZRAZ, OP_NEQ, ODNOSNI_IZRAZ)):

            output = self.children[0].generate_output()
            output += "\t\tMOVE R6, R1\n"
            # if error:
            #     return error
            # if not implicit_cast(self.children[0].tip, INT):
            #     return self.error()
            output += self.children[2].generate_output()
            output += "\t\tMOVE R6, R2\n"

            output += "\t\tXOR R1, R2, R6\n"
            output += "\t\tAND R6, 1, R6\n"

            if self.right_side(JEDNAKOSNI_IZRAZ, OP_EQ, ODNOSNI_IZRAZ):
                output += "\t\tXOR R6, 1, R6\n"

            # if error:
            #     return error
            # if not implicit_cast(self.children[2].tip, INT):
            #     return self.error()
            self.tip = INT
            self.l_izraz = 0
        return output
    

    # <bin_i_izraz>
    def bin_i_izraz(self):
        if self.right_side(JEDNAKOSNI_IZRAZ):
            output = self.children[0].generate_output()
            # if error:
            #     return error
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz
        
        elif self.right_side(BIN_I_IZRAZ, OP_BIN_I, JEDNAKOSNI_IZRAZ):

            output = self.children[0].generate_output()
            output += "\t\tMOVE R6, R1\n"
            output += self.children[2].generate_output()
            output += "\t\tMOVE R6, R2\n"
            output += "\t\tAND R1, R2, R6\n"
            # if error:
            #     return error
            # if not implicit_cast(self.children[0].tip, INT):
            #     return self.error()
            # if error:
            #     return error
            # if not implicit_cast(self.children[2].tip, INT):
            #     return self.error()
            self.tip = INT
            self.l_izraz = 0
        return output
    

    # <bin_xili_izraz>
    def bin_xili_izraz(self):
        if self.right_side(BIN_I_IZRAZ):
            output = self.children[0].generate_output()
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz
        
        elif self.right_side(BIN_XILI_IZRAZ, OP_BIN_XILI, BIN_I_IZRAZ):
            output = self.children[0].generate_output()
            output += "\t\tMOVE R6, R1\n"
            output += self.children[2].generate_output()
            output += "\t\tMOVE R6, R2\n"
            output += "\t\tXOR R1, R2, R6\n"

            # error = self.children[0].generate_output()
            # if error:
            #     return error
            # if not implicit_cast(self.children[0].tip, INT):
            #     return self.error()
            # error = self.children[2].generate_output()
            # if error:
            #     return error
            # if not implicit_cast(self.children[2].tip, INT):
            #     return self.error()
            self.tip = INT
            self.l_izraz = 0
        return output
    

    # <bin_ili_izrazi>
    def bin_ili_izrazi(self):
        if self.right_side(BIN_XILI_IZRAZ):
            output = self.children[0].generate_output()
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz
        
        elif self.right_side(BIN_ILI_IZRAZ, OP_BIN_ILI, BIN_XILI_IZRAZ):
            output = self.children[0].generate_output()
            output += "\t\tMOVE R6, R1\n"
            output += self.children[2].generate_output()
            output += "\t\tMOVE R6, R2\n"
            output += "\t\tOR R1, R2, R6\n"

            # error = self.children[0].generate_output()
            # if error:
            #     return error
            # if not implicit_cast(self.children[0].tip, INT):
            #     return self.error()
            # error = self.children[2].generate_output()
            # if error:
            #     return error
            # if not implicit_cast(self.children[2].tip, INT):
            #     return self.error()
            self.tip = INT
            self.l_izraz = 0
        return output
    

    # <log_i_izraz>
    def log_i_izraz(self):
        if self.right_side(BIN_ILI_IZRAZ):
            output = self.children[0].generate_output()
            # if inside_if:
            #     count = UniqueCounter.get_unique()
            #     output += f"\t\tMOVE R6, R5\n"
            #     output += f"\t\tCMP R5, 0\n"
            #     output += f"\t\tJP_NE ASS_{count}\n"
            #     output += f"\t\tJP_EQ NA_{count}\n"
            #     output += f"ASS_{count}\n"
            #     output += f"\t\tMOVE 1, R5\n"
            #     output += f"NA_{count}\n"
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz
        
        elif self.right_side(LOG_I_IZRAZ, OP_I, BIN_ILI_IZRAZ):
            label_index = UniqueCounter.get_unique()

            first_operand_mem = self.global_variables.size()
            self.global_variables.add_line(f"G_{first_operand_mem}\t\tDW 0")
            output = self.children[0].generate_output()
            output += f"\t\tSTORE R6, (G_{first_operand_mem})\n"
            output += f"\t\tMOVE 0, R4\n"
            output += f"\t\tCMP R6, R4\n"
            output += f"\t\tJP_EQ T_{label_index}\n"

    
            second_operand_mem = self.global_variables.size()
            self.global_variables.add_line(f"G_{second_operand_mem}\t\tDW 0")
            output += self.children[2].generate_output()
            output += f"\t\tSTORE R6, (G_{second_operand_mem})\n"

            output += f"\t\tLOAD R1, (G_{first_operand_mem})\n"
            output += f"\t\tLOAD R2, (G_{second_operand_mem})\n"
            output += f"\t\tAND R6, R1, R2\n"
            output += f"\t\tMOVE 0, R6\n"
            output += f"\t\tCMP R6, R1\n"

            

            output += f"\t\tJP_EQ T_{label_index}\n"
            output += f"\t\tMOVE 1, R6\n"
            output += f"\t\tJP I_{label_index}\n"
            output += f"T_{label_index}\n"
            output += f"\t\tMOVE 0, R6\n"
            output += f"I_{label_index}\n"
            # output = self.children[0].generate_output()
            # if error:
            #     return error
            # if not implicit_cast(self.children[0].tip, INT):
            #     return self.error()
            # output += self.children[2].generate_output()
            # if error:
            #     return error
            # if not implicit_cast(self.children[2].tip, INT):
            #     return self.error()
            self.tip = INT
            self.l_izraz = 0
        return output
    

    # <log_ili_izraz>
    def log_ili_izraz(self, inside_if=False):
        if self.right_side(LOG_I_IZRAZ):
            output = self.children[0].generate_output()
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz
            if inside_if:
                count = UniqueCounter.get_unique()
                output += f"\t\tMOVE R6, R5\n"
                output += f"\t\tCMP R5, 0\n"
                output += f"\t\tJP_NE ASS_{count}\n"
                output += f"\t\tJP_EQ NA_{count}\n"
                output += f"ASS_{count}\n"
                output += f"\t\tMOVE 1, R5\n"
                output += f"NA_{count}\n"
            
        elif self.right_side(LOG_ILI_IZRAZ, OP_ILI, LOG_I_IZRAZ):
            # if error:
            #     return error
            # if not implicit_cast(self.children[0].tip, INT):
            #     return self.error()
            # if error:
            #     return error
            # if not implicit_cast(self.children[2].tip, INT):
            #     return self.error()
            label_index = UniqueCounter.get_unique()

            first_operand_mem = self.global_variables.size()
            self.global_variables.add_line(f"G_{first_operand_mem}\t\tDW 0")
            output = self.children[0].generate_output()
            output += f"\t\tSTORE R6, (G_{first_operand_mem})\n"
            output += f"\t\tMOVE 1, R4\n"
            output += f"\t\tCMP R6, R4\n"
            output += f"\t\tJP_EQ I_{label_index}\n"
    
            second_operand_mem = self.global_variables.size()
            self.global_variables.add_line(f"G_{second_operand_mem}\t\tDW 0")
            output += self.children[2].generate_output()
            output += f"\t\tSTORE R6, (G_{second_operand_mem})\n"

            output += f"\t\tLOAD R1, (G_{first_operand_mem})\n"
            output += f"\t\tLOAD R2, (G_{second_operand_mem})\n"
            output += f"\t\tOR R6, R1, R2\n"
            output += f"\t\tMOVE 0, R1\n"
            output += f"\t\tCMP R6, R1\n"


            output += f"\t\tJP_EQ T_{label_index}\n"
            output += f"\t\tMOVE 1, R6\n"
            output += f"\t\tJP I_{label_index}\n"
            output += f"T_{label_index}\n"
            output += f"\t\tMOVE 0, R6\n"
            output += f"I_{label_index}\n"

            # output = self.children[0].generate_output()
            # output += "\t\tMOVE R6, R1\n"
            # output += self.children[2].generate_output()
            # output += "\t\tMOVE R6, R2\n"
            # output += "\t\tOR R1, R2, R6\n"

            self.tip = INT
            self.l_izraz = 0
        return output
    

    # <izraz_pridruzivanja>
    def izraz_pridruzivanja(self, inside_if=False):
        if self.right_side(LOG_ILI_IZRAZ):
            output = self.children[0].generate_output(inside_if=inside_if)
            # if error:
            #     return error
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz
        
        elif self.right_side(POSTFIKS_IZRAZ, OP_PRIDRUZI, IZRAZ_PRIDRUZIVANJA):
            load_idn_in_r6 = self.children[0].generate_output()
            stack_position_of_idn = load_idn_in_r6.split(" ")[-1]
            # if error:
            #     return error
            # if self.children[0].l_izraz != 1:
            #     return self.error()
            output = self.children[2].generate_output()
            output += f"\t\tSTORE R6, {stack_position_of_idn}\n"
            # if error:
            #     return error
            # if not implicit_cast(self.children[2].tip, self.children[0].tip):
            #     return self.error()
            self.tip = self.children[0].tip
            self.l_izraz = 0
        return output
    

    # <izraz>
    def izraz(self, inside_if=False):
        if self.right_side(IZRAZ_PRIDRUZIVANJA):
            output = self.children[0].generate_output(inside_if=inside_if)
        elif self.right_side(IZRAZ, ZAREZ, IZRAZ_PRIDRUZIVANJA):
            error = self.children[0].generate_output(inside_if=inside_if)
            if error:
                return error
            error = self.children[2].generate_output(inside_if=inside_if)
            if error:
                return error
            self.tip = self.children[2].tip
            self.l_izraz = 0
        return output


    # <slozena_naredba>
    def slozena_naredba(self, scope=None, lista_identifikatora=None, lista_tipova=None):
        child_scope = Scope(self.scope_structure.current_scope, scope, stack_position=0)
        self.scope_structure.add_child_scope(child_scope)
        if lista_identifikatora is not None and lista_tipova is not None:
            for (idn, tip) in zip(lista_identifikatora, lista_tipova):
                self.scope_structure.add_declaration(idn, tip)
        
        if self.right_side(L_VIT_ZAGRADA, LISTA_NAREDBI, D_VIT_ZAGRADA):
            output = self.children[1].generate_output()
            # self.functions.current_function().add_commands(output)
        elif self.right_side(L_VIT_ZAGRADA, LISTA_DEKLARACIJA, LISTA_NAREDBI, D_VIT_ZAGRADA):
            output = self.children[1].generate_output()
            # if error:
            #     return error
            output += self.children[2].generate_output()
            # if error:
            #     return error
        # remove local vars from stack
        scope_len = len(self.scope_structure.current_scope.idn_values)
        self.functions.current_function().remove_n_local_vars(scope_len)
        if self.scope_structure.current_scope.scope_type != FUNCTION:
            output += f"\t\tADD R7, {make_frisc_hex(scope_len * 4)}, R7\n"
        self.scope_structure.remove_scope()
        return output
        
    # <lista_naredbi>
    def lista_naredbi(self):
        if self.right_side(NAREDBA):
            output = self.children[0].generate_output()
        elif self.right_side(LISTA_NAREDBI, NAREDBA):
            output = self.children[0].generate_output()
            # if error:
            #     return error
            output += self.children[1].generate_output()
            # if error:
            #     return error
        return output

    # <naredba>
    def naredba(self):
        # sve produkcije su jedinicne
        output = self.children[0].generate_output()
        return output
    
    # <izraz_naredba>
    def izraz_naredba(self):
        if self.right_side(TOCKAZAREZ):
            self.tip = INT
        if self.right_side(IZRAZ, TOCKAZAREZ):
            error = self.children[0].generate_output()
            if error:
                return error
            self.tip = self.children[0].tip

    # <naredba_grananja>
    def naredba_grananja(self):
        if self.right_side(KR_IF, L_ZAGRADA, IZRAZ, D_ZAGRADA, NAREDBA):
            count = UniqueCounter.get_unique()
            output = self.children[2].generate_output(inside_if=True)
            output += f"\t\tCMP R5, 1\n"
            output += f"\t\tJP_EQ THEN_{count}\n"
            output += f"\t\tJP_NE END_{count}\n"
            output += f"THEN_{count}\n"
            # if error:
            #     return error
            # if not implicit_cast(self.children[2].tip, INT):
            #     return self.error()
            output += self.children[4].generate_output()
            output += f"\t\tJP END_{count}\n"
            output += f"END_{count}\n"
            # if error:
            #     return error
        elif self.right_side(KR_IF, L_ZAGRADA, IZRAZ, D_ZAGRADA, NAREDBA, KR_ELSE, NAREDBA):
            count = UniqueCounter.get_unique()
            output = self.children[2].generate_output(inside_if=True)
            # if error:
            #     return error
            # if not implicit_cast(self.children[2].tip, INT):
            #     return self.error()
            output += f"\t\tCMP R5, 1\n"
            output += f"\t\tJP_EQ THEN_{count}\n"
            output += f"\t\tJP_NE ELSE_{count}\n"
            output += f"THEN_{count}\n"
            output += self.children[4].generate_output()
            output += f"\t\tJP END_{count}\n"
            # if error:
            #     return error
            output += f"ELSE_{count}\n"
            output += self.children[6].generate_output()
            output += f"\t\tJP END_{count}\n"
            output += f"END_{count}\n"
            # if error:
            #     return error
        return output

    # <naredba_petlje>
    def naredba_petlje(self):
        if self.right_side(KR_WHILE, L_ZAGRADA, IZRAZ, D_ZAGRADA, NAREDBA):
            count = UniqueCounter.get_unique()
            output = f"WHL_{count}\n"
            output += self.children[2].generate_output()

            output += "\t\tCMP R6, 0\n"
            output += f"\t\tJP_EQ OUT_{count}\n"
            # if error:
            #     return error
            # if not implicit_cast(self.children[2].tip, INT):
            #     return self.error()
            output += self.children[4].generate_output()
            output += f"\t\tJP WHL_{count}\n"
            output += f"OUT_{count}\n"
            # if error:
            #     return error
        elif self.right_side(KR_FOR, L_ZAGRADA, IZRAZ_NAREDBA, IZRAZ_NAREDBA, D_ZAGRADA, NAREDBA):
            # error = self.children[2].generate_output()
            # if error:
            #     return error
            # error = self.children[3].generate_output()
            # if error:
            #     return error
            # if not implicit_cast(self.children[3].tip, INT):
            #     return self.error()
            # error = self.children[5].generate_output()
            # if error:
            #     return error
            count = UniqueCounter.get_unique()
            output = self.children[2].generate_output()

            output += f"FOR_{count}\n"
            output += self.children[3].generate_output()
            output += "\t\tCMP R6, 0\n"
            output += f"\t\tJP_EQ OUT_{count}\n"

            output += self.children[5].generate_output()

            output += f"\t\tJP FOR_{count}\n"
            output += f"OUT_{count}\n"

        elif self.right_side(KR_FOR, L_ZAGRADA, IZRAZ_NAREDBA, IZRAZ_NAREDBA, IZRAZ, D_ZAGRADA, NAREDBA):
            # error = self.children[2].generate_output()
            # if error:
            #     return error
            # error = self.children[3].generate_output()
            # if error:
            #     return error
            # if not implicit_cast(self.children[3].tip, INT):
            #     return self.error()
            # error = self.children[4].generate_output()
            # if error:
            #     return error
            # error = self.children[6].generate_output()
            # if error:
            #     return error
            count = UniqueCounter.get_unique()
            output = self.children[2].generate_output()

            output += f"FOR_{count}\n"
            output += self.children[3].generate_output()
            output += "\t\tCMP R6, 0\n"
            output += f"\t\tJP_EQ OUT_{count}\n"

            output += self.children[6].generate_output()

            output += self.children[4].generate_output()
            output += f"\t\tJP FOR_{count}\n"
            output += f"OUT_{count}\n"


        return output

    # <naredba_skoka>
    def naredba_skoka(self):
        # if self.right_side(KR_CONTINUE, TOCKAZAREZ) or self.right_side(KR_BREAK, TOCKAZAREZ):
        #     if not self.in_loop():
        #         return self.error()
        if self.right_side(KR_RETURN, TOCKAZAREZ):
            # if self.nesting_function_type() != VOID:
            #     return self.error()
            output = f"\t\tADD R7, {make_frisc_hex(self.functions.current_function().local_var_count() * 4)}, R7\n"
            output += "\t\tRET\n"
        if self.right_side(KR_RETURN, IZRAZ, TOCKAZAREZ):
            output = self.children[1].generate_output()
            output += f"\t\tADD R7, {make_frisc_hex(self.functions.current_function().local_var_count() * 4)}, R7\n"
            output += "\t\tRET\n"
        return output

    
    # <prijevodna_jedinica>
    def prijevodna_jedinica(self):
        if self.right_side(VANJSKA_DEKLARACIJA):
            self.children[0].generate_output()

        if self.right_side(PRIJEVODNA_JEDINICA, VANJSKA_DEKLARACIJA):
            self.children[0].generate_output()
            self.children[1].generate_output()
        
        if self.root_node:
            header = "\t\tMOVE 40000, R7\n\t\tCALL F_MAIN\n\t\tHALT\n"
            full_output = header + "\n" + self.functions.print() + "\n" + self.global_variables.print()
            return full_output
        
        return ""


    # <vanjska_deklaracija>    
    def vanjska_deklaracija(self):
        self.children[0].generate_output()
        return ""
    

    # <definicija_funkcije>
    def definicija_funkcije(self):
        new_function = Function()
        if self.right_side(IME_TIPA, IDN, L_ZAGRADA, KR_VOID, D_ZAGRADA, SLOZENA_NAREDBA):
            ime_tipa = self.children[0]
            idn = self.children[1]
            current_return_type = ime_tipa.tip
            self.tip = FunctionType([VOID], current_return_type)
            self.scope_structure.add_definition(idn.lex, FunctionType([VOID], current_return_type))
            self.scope_structure.add_declaration(idn.lex, FunctionType([VOID], current_return_type))

            new_function.set_name(self.children[1].lex)
            self.functions.add(new_function)
            output = self.children[5].generate_output(scope=FUNCTION)
            self.functions.current_function().add_commands(output)
            # # generate_output ime tipa
            # error = self.children[0].generate_output()
            # if error:
            #     return error
            # # ime_tipa.tip != const(T)
            # if is_const_x(ime_tipa.tip):
            #     return self.error()
            # # ne postoji prije definirana funcija IDN.ime
            # if idn.lex in self.scope_structure.all_functions_definitions().keys():
            #     return self.error()
            # # if self.scope_structure.idn_name_in_scope(idn.lex):
            # #     return self.error()
            # # ako postoji deklaracija imena IDN.ime u globalnom djelokrugu
            # # onda je pripadni tip de deklaracije funkcija(void -> <ime_tipa>.tip)
            # global_scope = self.scope_structure.current_scope.global_scope()
            # if idn.lex in global_scope.declarations:
            #     required_type = global_scope.declarations[idn.lex]
            #     if required_type != FunctionType([VOID], current_return_type):
            #         self.error()
            # # zabiljezi definiciju i deklaraciju funkcije
            
            # # generate_output(<slozena_naredba>)
            # error = self.children[5].generate_output()
            # if error:
            #     return error

        elif self.right_side(IME_TIPA, IDN, L_ZAGRADA, LISTA_PARAMETARA, D_ZAGRADA, SLOZENA_NAREDBA):
            error = self.children[0].generate_output()
            # # generate_output ime tipa
            # if error:
            #     return error
            ime_tipa = self.children[0]
            idn = self.children[1]
            lista_parametara = self.children[3]
            # ime_tipa.tip != CONST(T)
            # if is_const_x(ime_tipa.tip):
            #     return self.error()
            # global_scope = self.scope_structure.current_scope.global_scope()
            # ne postoji prije definirana funkcija IDN.ime
            # if idn.lex in self.scope_structure.all_functions_definitions().keys():
            #     return self.error()
            # generate_output(lista_parametara)
            # output = lista_parametara.generate_output()
            lista_parametara.generate_output()
            # if error:
            #     return error
            # ako postoji deklaracija IDN.ime u globalnom djelokrugu,
            # onda je pripadni tip funkcija(lista_param.tipovi -> ime_tipa.tip)
            current_return_type = ime_tipa.tip
            current_argument_types = lista_parametara.tipovi
            # if idn.lex in global_scope.declarations:
            #     required_type = global_scope.declarations[idn.lex]
            #     if required_type != FunctionType(current_argument_types, current_return_type):
            #         return self.error()
            # zabiljezi definiciju i deklaraciju funkcije
            self.tip = FunctionType(current_argument_types, current_return_type)
            self.scope_structure.add_definition(idn.lex, FunctionType(current_argument_types, current_return_type))
            self.scope_structure.add_declaration(idn.lex, FunctionType(current_argument_types, current_return_type))
            # generate_output(slozena_naredba) uz parametre funkcije
            # koristeci <lista_param>.tipovi i <lista_param>.imena
            new_function.set_name(self.children[1].lex)
            self.functions.add(new_function)
            output = self.children[5].generate_output(lista_identifikatora=lista_parametara.identifikatori, 
                lista_tipova=lista_parametara.tipovi, scope=FUNCTION)
            # if error:
            #     return error
            self.functions.current_function().add_commands(output)
        return ""

    def lista_parametara(self):
        if self.right_side(DEKLARACIJA_PARAMETRA):
            output = self.children[0].generate_output()
            # if error:
            #     return error
            self.tipovi = [self.children[0].tip]
            self.identifikatori = [self.children[0].lex]
        elif self.right_side(LISTA_PARAMETARA, ZAREZ, DEKLARACIJA_PARAMETRA):
            output = self.children[0].generate_output()
            # if error:
            #     return error
            output = self.children[2].generate_output()
            # if error:
            #     return error
            # if self.children[2].lex in self.children[0].identifikatori:
            #     return self.error()
            self.tipovi = self.children[0].tipovi + [self.children[2].tip]
            self.identifikatori = self.children[0].identifikatori + [self.children[2].lex]
        return ""

    def deklaracija_parametra(self):
        if self.right_side(IME_TIPA, IDN):
            output = self.children[0].generate_output()
            # if error:
            #     return error
            # if self.children[0].tip == VOID:
            #     return self.error()
            self.tip = self.children[0].tip
            self.lex = self.children[1].lex
        elif self.right_side(IME_TIPA, IDN, L_UGL_ZAGRADA, D_UGL_ZAGRADA):
            output = self.children[0].generate_output()
            # if error:
            #     return error
            # if self.children[0].tip == VOID:
            #     return self.error()
            self.tip = make_niz(self.children[0].tip)
            self.lex = self.children[1].lex
        return ""

    def lista_deklaracija(self):
        if self.right_side(DEKLARACIJA):
            output = self.children[0].generate_output()
            # if error:
            #     return error
        elif self.right_side(LISTA_DEKLARACIJA, DEKLARACIJA):
            output = self.children[0].generate_output()
            # if error:
            #     return error
            output += self.children[1].generate_output()
            # if error:
            #     return error
        return output

    def deklaracija(self):
        if self.right_side(IME_TIPA, LISTA_INIT_DEKLARATORA, TOCKAZAREZ):
            output = self.children[0].generate_output()
            current_ntip = self.children[0].tip
            output += self.children[1].generate_output(ntip=current_ntip)
        return output
    
    def lista_init_deklaratora(self, ntip):
        # if ntip is None:
        #     return self.error()
        self.ntip = ntip
        current_ntip = self.ntip
        if self.right_side(INIT_DEKLARATOR):
            output = self.children[0].generate_output(ntip=current_ntip)
        elif self.right_side(LISTA_INIT_DEKLARATORA, ZAREZ, INIT_DEKLARATOR):
            output = self.children[0].generate_output(ntip=current_ntip)
            # if error:
            #     return error
            output += self.children[2].generate_output(ntip=current_ntip)
            # if error:
            #     return error
        return output
    
    def init_deklarator(self, ntip):
        # if ntip is None:
        #     return self.error()
        self.ntip = ntip
        current_ntip = self.ntip
        if self.right_side(IZRAVNI_DEKLARATOR):
            output = self.children[0].generate_output(ntip=current_ntip)
            # if error:
            #     return error
            # if is_const_x(self.children[0].tip):
            #     return self.error()
            # if is_niz_x(self.children[0].tip):
            #     if is_const_x(remove_niz_from_niz_x(self.children[0].tip)):
            #         return self.error()
            if not self.scope_structure.current_scope.is_global():
                output += "\t\tPUSH R6\n"
                self.functions.current_function().declared()
        elif self.right_side(IZRAVNI_DEKLARATOR, OP_PRIDRUZI, INICIJALIZATOR):
            if self.scope_structure.current_scope.is_global():
                name = self.children[0].generate_output(ntip=current_ntip)
                value = self.children[2].generate_output()
                if len(name) < 4:
                    tabs = "\t\t"
                else:
                    tabs = "\t"
                if self.ntip == INT:
                    type_to_save = "DW"
                else:
                    type_to_save = "DH"
                self.global_variables.add_line(name + tabs + type_to_save + " " + value)
                output = ""
            else:
                name = self.children[0].generate_output(ntip=current_ntip)
                output = self.children[2].generate_output()
                output += "\t\tPUSH R6\n"
                self.functions.current_function().declared()

            # error = self.children[0].generate_output(ntip=current_ntip)
            # if error:
            #     return error
            # error = self.children[2].generate_output()
            # if error:
            #     return error
            # izravni_deklarator_type = self.children[0].tip
            # if not is_niz_x(izravni_deklarator_type):
            #     stripped_type = izravni_deklarator_type
            #     if is_const_x(stripped_type):
            #         stripped_type = remove_const_from_const_x(stripped_type)
            #     if not implicit_cast(self.children[2].tip, stripped_type):
            #         return self.error() 
            # elif is_niz_x(izravni_deklarator_type):
            #     stripped_type = remove_niz_from_niz_x(izravni_deklarator_type)
            #     if is_const_x(stripped_type):
            #         stripped_type = remove_const_from_const_x(stripped_type)
            #     if not (self.children[2].br_elem <= self.children[0].br_elem):
            #         return self.error()
            #     for u in self.children[2].tipovi:
            #         if not implicit_cast(u, stripped_type):
            #             return self.error()
        return output
    
    def izravni_deklarator(self, ntip):
        # if ntip is None:
        #     return self.error()
        self.ntip = ntip
        if self.right_side(IDN):
            # if self.ntip == VOID:
            #     return self.error()
            # if self.scope_structure.idn_name_in_local_scope(self.children[0].lex):
            #     return self.error()
            self.scope_structure.add_declaration(self.children[0].lex, self.ntip)
            self.scope_structure.add_l_izraz(self.children[0].lex, 1)
            self.tip = self.ntip
            if self.scope_structure.current_scope.is_global():
                return "G_" + (self.children[0].lex).upper()
            else:
                self.functions.current_function().add_local_var(self.children[0].lex)
                self.functions.current_function().in_process_of_declaring()
                return ""
                
        elif self.right_side(IDN, L_UGL_ZAGRADA, BROJ, D_UGL_ZAGRADA):
            # if self.ntip == VOID:
            #     return self.error()
            # if self.scope_structure.idn_name_in_local_scope(self.children[0].lex):
            #     return self.error()
            # if self.children[2].vrijednost is None:
            #     return self.error()
            # if self.children[2].vrijednost <= 0:
            #     return self.error()
            # elif self.children[2].vrijednost > 1024:
            #     return self.error()
            array_type = make_niz(self.ntip)
            self.scope_structure.add_declaration(self.children[0].lex, array_type)
            self.scope_structure.add_l_izraz(self.children[0].lex, 1)
            self.tip = array_type
            self.br_elem = self.children[2].vrijednost
            for i in range(self.br_elem):
                self.global_variables.add_line(f"{self.children[0].lex}_{self.global_variables.size()}\t\tDW %D 0")
        elif self.right_side(IDN, L_ZAGRADA, KR_VOID, D_ZAGRADA):
            if self.scope_structure.idn_name_in_local_scope(self.children[0].lex):
                required_type = self.scope_structure.type_of_idn_in_scope(self.children[0].lex)
                if required_type != FunctionType([VOID], self.ntip):
                    return self.error()
            else:
                self.scope_structure.add_declaration(self.children[0].lex, 
                    FunctionType([VOID], self.ntip))
                self.scope_structure.add_l_izraz(self.children[0].lex, 0)
        elif self.right_side(IDN, L_ZAGRADA, LISTA_PARAMETARA, D_ZAGRADA):
            error = self.children[2].generate_output()
            if error:
                return error
            if self.scope_structure.idn_name_in_local_scope(self.children[0].lex):
                required_type = self.scope_structure.type_of_idn_in_scope(self.children[0].lex)
                if required_type != FunctionType(self.children[2].tipovi, self.ntip):
                    return self.error()
            else:
                self.scope_structure.add_declaration(self.children[0].lex, 
                    FunctionType(self.children[2].tipovi, self.ntip))
                self.scope_structure.add_l_izraz(self.children[0].lex, 0)
        return ""

    def inicijalizator(self):
        if self.right_side(IZRAZ_PRIDRUZIVANJA):
            # error = self.children[0].generate_output()
            # if error:
            #     return error
            # flag, array_length = self.children[0].goes_to_niz_znakova()
            # if flag:
            #     self.br_elem = array_length + 1
            #     self.tipovi = [CHAR] * self.br_elem
            # else:
            #     self.tip = self.children[0].tip
            return self.children[0].generate_output()
        elif self.right_side(L_VIT_ZAGRADA, LISTA_IZRAZA_PRIDRUZIVANJA, D_VIT_ZAGRADA):
            error = self.children[1].generate_output()
            if error: 
                return error
            self.br_elem = self.children[1].br_elem
            self.tipovi = self.children[1].tipovi
        return ""
    
    
    def lista_izraza_pridruzivanja(self):
        if self.right_side(IZRAZ_PRIDRUZIVANJA):
            error = self.children[0].generate_output()
            if error:
                return error
            self.tipovi = [self.children[0].tip]
            self.br_elem = 1
        elif self.right_side(LISTA_IZRAZA_PRIDRUZIVANJA, ZAREZ, IZRAZ_PRIDRUZIVANJA):
            error = self.children[0].generate_output()
            if error:
                return error
            error = self.children[1].generate_output()
            if error:
                return error
            self.tipovi = self.children[0].tipovi + [self.children[2].tip]
            self.br_elem = self.children[0].br_elem + 1
