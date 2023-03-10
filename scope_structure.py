from scope import Scope
from consts import *


class ScopeStructure():

    current_scope = None

    def __init__(self, global_scope: Scope):
        self.current_scope = global_scope
        return
    

    def l_izraz_of_idn_in_scope(self, name):
        return self.current_scope.l_izraz_of_idn_in_scope(name)

    def add_l_izraz(self, idn, l_izraz):
        self.current_scope.add_l_izraz(idn, l_izraz)
    
    def return_scope_containg_name(self, name):
        return self.current_scope.scope_containing_name(name)

    def idn_name_in_scope(self, name: str):
        return self.current_scope.idn_name_in_scope(name)

    def idn_name_in_local_scope(self, name):
        return self.current_scope.idn_name_in_local_scope(name)
    
    def idn_name_not_in_local_scopes(self, name):
        return self.current_scope.idn_name_not_in_local_scopes(name)
        
    def type_of_idn_in_scope(self, name):
        return self.current_scope.type_of_idn_in_scope(name)

    def add_definition(self, idn, type):
        self.current_scope.add_definition(idn, type)
        return
    
    def add_declaration(self, idn, type):
        self.current_scope.add_declaration(idn, type)
        return

    def add_child_scope(self, child: Scope):
        self.current_scope.add_child_scope(child)
        self.current_scope = child
        return
    

    def remove_scope(self):
        if self.current_scope.scope_type == GLOBAL:
            return
        self.current_scope = self.current_scope.parent_scope
        self.current_scope.remove_child_scope()
        return
    
    def global_scope(self):
        return self.current_scope.global_scope()

    def all_functions_definitions(self):
        return self.global_scope().function_definitions()

    def all_functions_declarations(self):
        return self.global_scope().function_declarations()