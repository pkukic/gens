class GlobalVariables:

    def __init__(self):
        self.body = []
    

    def add_line(self, line):
        self.body.append(line)
    

    def print(self):
        output_string = '\n'.join(self.body)
        return output_string