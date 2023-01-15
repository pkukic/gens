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
    

    def set_name(self, name):
        self.name = "F_" + name.upper()
    

    def add_commands(self, commands):
        self.body = commands


    def __str__(self):
        name = self.name + "\n"
        body = self.body
        return name + body
