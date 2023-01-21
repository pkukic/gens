class Functions:

    def __init__(self):
        self.functions = []
    

    def add(self, function):
        self.functions.append(function)
    

    def current_function(self):
        return self.functions[-1]
    

    def print(self):
        functions = [str(f) for f in self.functions]
        return "\n\n".join(functions)



class Function:

    def __init__(self):
        self.name = ""
        self.body = ""
        self.local_vars = []
        self.undecalred = 0
    

    def set_name(self, name):
        self.name = "F_" + name.upper()
    

    def add_local_var(self, name):
        self.local_vars.append(name)
    

    def in_process_of_declaring(self):
        self.undecalred += 1
    

    def declared(self):
        self.undecalred -= 1
    

    def is_local_var(self, name):
        return name in self.local_vars
    
    def local_var_offset(self, name):
        return (len(self.local_vars) - self.local_vars.index(name) - 1 - self.undecalred) * 4

    def local_var_count(self):
        return len(self.local_vars)
    

    def add_commands(self, commands):
        self.body = commands


    def __str__(self):
        name = self.name + "\n"
        body = self.body
        return name + body
