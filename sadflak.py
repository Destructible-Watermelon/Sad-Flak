class TwinStacks:
    def __init__(self):
        self.stacks= ([],[])
    def pop(self, index):
        if self.stacks[index]:
            return self.stacks[index].pop()
        else:
            return 0
    def push(self, index, value):
        self.stacks[index].append(value)

class SadflakInterpreter:
    close_paren = {"{":"}", "[":"]", "(":")", "<":">", "≤":"≥"}
    command_index = {"(":0, "[":1, "{":2, "<":3, "≤":4}
    def __init__(self, program):
        self.program = [i.replace("\n","") for i in open(program).readlines()]
        self.expand()
        for i in range(len(self.program)):
            if self.program[i]:
                self.program[i] = self.lispify(self.slim(self.program[i]), self.command_index["<"])
            else:
                self.program[i] = None
        self.stacks = TwinStacks()

        import argparse
        parser = argparse.ArgumentParser(description="Interpret the Sadflak language")
        parser.add_argument(
        "-A", "--ascii_output", action="store_true",
        help="ascii output"
        )
        argv = parser.parse_args()
        self.ascii_output = argv.ascii_output


    def slim(self,line):
        return ''.join(i for i in line if i in "()[]{}<>≤≥")

    def expand(self):
        i = 0
        while i < len(self.program):  # using while because list is modified
            if self.program[i].isnumeric():  # lines of numbers need to be only numbers.
                lines = int(self.program.pop(i))
                for j in range(lines):
                    self.program.insert(i,"")
                i += lines
            else:
                i += 1


    def lispify(self, prog_string, command):  # lispify because it turns it into a list of lists to better interpret it,
        # with the command at the front
        open_index = 0  # where is the open paren?
        close_index = 1  # where is the close paren?
        finished = False
        command_list = [command]
        while open_index+1<len(prog_string):
            paren_scope = 1  # how many parens inside are we, hence how many matching parens need to be skipped
            open_paren = prog_string[open_index]  # What is the open paren?
            while paren_scope > 0:
                if prog_string[close_index] == self.close_paren[open_paren]:
                    paren_scope -= 1
                elif prog_string[close_index] == open_paren:
                    paren_scope += 1
                close_index += 1
            command_list.append(self.lispify(prog_string[open_index+1:close_index-1],
                                             self.command_index[prog_string[open_index]]))
            open_index = close_index
            close_index += 1
        if len(command_list) > 1:
            command_list.insert(1,command_list.count([0]))
            command_list[:] = [x for x in command_list if x != [0]]
            i=2
            while i < len(command_list):  # using while instead of for, because command_list is modified.
                item=command_list[i]
                if len(item) == 2 and item[0] == self.command_index["["] and type(item[1]) == int:
                    command_list[1] -= item[1]
                    command_list.remove(item)
                else:
                    i += 1
            if [4] in command_list:
                command_list = command_list[:command_list.index([4])+1]
            i = 2
            while i < len(command_list):
                if command_list[i][~0] == [4]:
                    deleted_list = command_list[i]
                    del command_list[i]
                    for j in deleted_list[2:deleted_list.index([4])+1]:
                        command_list.insert(i,j)
                        i += 1
                else:
                    i += 1

        return command_list

    def run(self, inputted):
        self.command_pointer = 0
        self.halted = False
        if inputted:
            if inputted[0] == '"':
                inputted = list(inputted)
                i = 1
                while i < len(inputted):  # using while because the variable is changed.
                    if inputted[i] == "\\":
                        if inputted[i+1]=="n":
                            del inputted[i+1]
                            inputted[i] = "\n"
                        elif inputted[i+1] == "\\":
                            del inputted[i+1]
                    i+=1
                for i in inputted[:0:-1]:
                    self.stacks.push(0, ord(i))

            else:
                inputted = [int(i) for i in inputted.split()]
                for i in inputted[::-1]:
                    self.stacks.push(0, i)
        while not self.halted:
            temp_pointer = self.command_pointer
            while self.program[temp_pointer] is None:
                temp_pointer += 1
                temp_pointer %= len(self.program)
            self.execute_command(self.program[temp_pointer])
        if self.ascii_output:
            print(''.join(chr(i) for i in self.stacks.stacks[0][::-1]))
        else:
            print('\n'.join(str(i) for i in self.stacks.stacks[0][::-1]))

    def execute_command(self, program_list):
        if len(program_list) > 1:
            command_arg = program_list[1]
            for i in program_list[2:]:
                command_arg += self.execute_command(i)
            if program_list[0] == 0:  # (...)
                self.stacks.push(0, command_arg)
                return command_arg
            if program_list[0] == 1:  # [...]
                return -command_arg
            elif program_list[0] == 2:  # {...}
                return self.stacks.pop(1)*command_arg
            elif program_list[0] == 3:  # <...>
                return 0
            elif program_list[0] == 4:  # ≤...≥
                self.command_pointer += command_arg
                self.command_pointer %= len(self.program)
                return command_arg
        else:
            if program_list[0] == 1:  # []
                return int(bool(self.stacks.pop(0)))
            elif program_list[0] == 2:  # {}
                return self.stacks.pop(0)
            elif program_list[0] == 3:  # <>
                ToS = self.stacks.pop(0)
                self.stacks.push(1,ToS)
                return ToS
            elif program_list[0] == 4:  # ≤≥
                self.halted = True
                return 0




if __name__ == "__main__":
    SadflakInterpreter(input()).run(input())
