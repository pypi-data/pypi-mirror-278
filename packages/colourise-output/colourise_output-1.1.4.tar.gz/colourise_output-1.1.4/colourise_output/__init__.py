"""
File in charge of adding colour to the terminal while respecting the windows colour norm
"""

from .colourise_output import ColouriseOutput


class colourise_output(ColouriseOutput):
    """ The class in charge of adding colour to the terminal while respecting the windows colour norm """
    pass


class colouriseoutput(ColouriseOutput):
    """ The class in charge of adding colour to the terminal while respecting the windows colour norm """
    pass


class Colourise_Output(ColouriseOutput):
    """ The class in charge of adding colour to the terminal while respecting the windows colour norm """
    pass


class COLOURISE_OUTPUT(ColouriseOutput):
    """ The class in charge of adding colour to the terminal while respecting the windows colour norm """
    pass


class COLOURISEOUTPUT(ColouriseOutput):
    """ The class in charge of adding colour to the terminal while respecting the windows colour norm """
    pass


class co(ColouriseOutput):
    """ The class in charge of adding colour to the terminal while respecting the windows colour norm """
    pass


class c_o(ColouriseOutput):
    """ The class in charge of adding colour to the terminal while respecting the windows colour norm """
    pass


class CO(ColouriseOutput):
    """ The class in charge of adding colour to the terminal while respecting the windows colour norm """
    pass


class C_O(ColouriseOutput):
    """ The class in charge of adding colour to the terminal while respecting the windows colour norm """
    pass


if __name__ == '__main__':
    CI = ColouriseOutput()
    CI.init_pallet()
    CI.test_colours()
    CI.display("0A", (), "Hello World !\n")
    CI.display("rr", "")
    CI.unload_ressources()
    print(f"Created by {CI.author}")
