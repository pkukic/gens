class GlobalVariables:

    def __init__(self):
        self.body = []
    

    def add_line(self, line):
        self.body.append(line)

    def size(self):
        return len(self.body)
    
    def print(self):
        output_string = '\n'.join(self.body) + '\n'
        return output_string