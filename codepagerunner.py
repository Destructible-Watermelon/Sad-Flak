import argparse
import sadflak
class SpecialCodePageSadFlak(sadflak.SadflakInterpreter):
    def __init__(self,program):
        self.program = [i.replace("\n","").translate(str.maketrans("`~≤≥","≤≥`~")) for i in open(program).readlines()]
        self.expand()
        for i in range(len(self.program)):
            if self.program[i]:
                self.program[i] = self.lispify(self.slim(self.program[i]), self.command_index["<"])
            else:
                self.program[i] = None
        self.stacks = sadflak.TwinStacks()

        import argparse
        parser = argparse.ArgumentParser(description="Interpret the Sadflak language")
        parser.add_argument(
        "-A", "--ascii_output", action="store_true",
        help="ascii output"
        )
        argv = parser.parse_args()
        self.ascii_output = argv.ascii_output

if __name__ == "__main__":
    SpecialCodePageSadFlak(input()).run(input())

