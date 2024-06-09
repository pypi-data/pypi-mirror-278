"""
File in charge of launching a demo when called
"""
from .colourise_output import ColouriseOutput

if __name__ == '__main__':
    CI = ColouriseOutput()
    CI.init_pallet()
    CI.test_colours()
    CI.display("0A", (), "Hello World !\n")
    CI.display("rr", "")
    CI.unload_ressources()
    print(f"Created by {CI.author}")
