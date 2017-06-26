import argparse
import sadflak
class SpecialCodePageSadFlak(sadflak.SadflakInterpreter):
    def __init__(self,arguments):
        self.program = [i.replace("\n","").translate(str.maketrans("`~≤≥","≤≥`~")) for i in open(arguments.program).readlines()]
        self.expand()
        for i in range(len(self.program)):
            if self.program[i]:
                self.program[i] = self.lispify(self.slim(self.program[i]), self.command_index["<"])
            else:
                self.program[i] = None
        self.stacks = sadflak.TwinStacks()

        self.ascii_output = arguments.ascii_output

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Interpret the Sadflak language with special codepage")
    parser.add_argument("program", metavar="program", type=str, help="path to the program")
    parser.add_argument("-A", "--ascii_output", action="store_true", help="ascii output")

    import os, sys
    the_input = '' if os.isatty(0) else sys.stdin.read()
    SpecialCodePageSadFlak(parser.parse_args()).run(the_input)

