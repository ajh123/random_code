from typing import Type

class Hole:
    def __init__(self, shape: str, takes: Type['Peg']):
        self.shape = shape
        self.takes = takes

    def putPeg(self, peg: 'Peg'):
        if isinstance(peg, self.takes):
            print(f"Putting a {peg.shape} peg into the {self.shape} hole")
        else:
            print(f"A {peg.shape} peg does not fit into a {self.shape} hole")

class Peg:
    def __init__(self, shape: str):
        self.shape = shape

class RoundHole(Hole):
    def __init__(self):
        super().__init__("round", RoundPeg)

class RoundPeg(Peg):
    def __init__(self):
        super().__init__("round")

class SquarePeg(Peg):
    def __init__(self):
        super().__init__("square")

class SqurareToRoundAdapter(RoundPeg):
    def __init__(self, takes: 'SquarePeg'):
        super().__init__()
        self.shape = f"{takes.shape} with round end"

rHole = RoundHole()
rPeg = RoundPeg()
rHole.putPeg(rPeg)

sPeg = SquarePeg()
rHole.putPeg(sPeg)

sToRA = SqurareToRoundAdapter(sPeg)
rHole.putPeg(sToRA)