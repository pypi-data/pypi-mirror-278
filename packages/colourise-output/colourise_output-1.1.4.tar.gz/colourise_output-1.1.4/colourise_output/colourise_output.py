##
# EPITECH PROJECT, 2022
# Desktop_pet (Workspace)
# File description:
# colourise_output.py
##

"""
The file containing the code in charge of outputting
coloured text into the terminal.
This class follows the batch colour coding rules (from 0 to F for foreground and background)
"""

import os
import platform
import colorama as COC


class ColouriseOutput:
    """
    The class in charge of adding colour to text 
    This class follows the batch colour coding rules (from 0 to F for foreground and background)
"""

    def __init__(self) -> None:
        self.__version__ = "1.0.0"
        self.author = "Henry Letellier"
        self.colour_pallet = {}
        self.unix_colour_pallet = dict()
        self.colourise_output = True
        self.wich_system = platform.system()

    def process_attributes(self, attributes: tuple = ()) -> list:
        """ Convert the inputted tuple to a list containing the options """
        finall_attributes = ""
        attributes_length = len(attributes)
        if attributes_length > 0 and attributes[0] is True:
            finall_attributes += "\033[01m"  # bold
        # if attributes_length > 1 and attributes[1] is True:
        #     finall_attributes.append("dark")
        if attributes_length > 2 and attributes[2] is True:
            finall_attributes += "\033[04m"  # underline
        if attributes_length > 3 and attributes[3] is True:
            finall_attributes += "\033[05m"  # blink
        # if attributes_length > 4 and attributes[4] is True:
            # finall_attributes.append("reverse")
        # if attributes_length > 5 and attributes[5] is True:
            # finall_attributes.append("concealed")
        return finall_attributes

    def display(self, colour: str, attributes: tuple = (), text: str = "") -> None:
        """ Depending on the system, change the command used to output colour """
        processed_attributes = self.process_attributes(attributes)
        if self.colourise_output is True:
            try:
                print(
                    f"{self.unix_colour_pallet[colour]}{processed_attributes}{text}",
                    end=""
                )
            except IOError:
                if self.wich_system == "Windows":
                    os.system(f"{self.colour_pallet[colour]}")
                    if len(text) > 0:
                        print(f"{text}", end="")
                else:
                    os.system(
                        f"echo -e \"{self.colour_pallet[colour]}{processed_attributes}{text}\""
                    )

    def load_for_windows(self) -> None:
        """ Prepare the Windows colour pallet """
        for i in "0123456789ABCDEFr":
            for j in "0123456789ABCDEFr":
                if i == 'r':
                    if j == 'r':
                        self.colour_pallet[f"{i}{j}"] = "color 0A"
                    else:
                        self.colour_pallet[f"{i}{j}"] = f"color 0{j}"
                elif j == 'r':
                    self.colour_pallet[f"{i}{j}"] = f"color {i}A"
                else:
                    self.colour_pallet[f"{i}{j}"] = f"color {i}{j}"

    def load_for_non_windows(self) -> None:
        """ Prepare the non Windows colour pallet """
        color_list = [
            "0 = 30", "1 = 34", "2 = 32", "3 = 36", "4 = 31", "5 = 35", "6 = 33", "7 = 37",
            "8 = 90", "9 = 94", "a = 92", "b = 96", "c = 91", "d = 95", "e = 93", "f = 97", "0"
        ]
        color_list = [
            "30", "34", "32", "36", "31", "35", "33", "37",
            "90", "94", "92", "96", "91", "95", "93", "97", "0"
        ]
        i = j = 0
        for foreground in "0123456789ABCDEFr":
            j = 0
            for background in "0123456789ABCDEFr":
                self.colour_pallet[
                    f"{background}{foreground}"
                ] = f"\\e[{int(color_list[j])+10}m\\e[{color_list[i]}m"
                self.unix_colour_pallet[
                    f"{background}{foreground}"
                ] = f"\033[{int(color_list[j])+10}m\033[{color_list[i]}m"
                j += 1
            i += 1

    def init_pallet(self) -> int:
        """ Prepare and load an intersystem pallet based on the Windows colour format """
        try:
            COC.reinit()
            self.load_for_non_windows()
            if self.wich_system == "Windows":
                self.load_for_windows()
            return 0
        except IOError:
            return 84

    def unload_ressources(self) -> int:
        """ Free the ressources that can be freed """
        try:
            COC.deinit()
            return 0
        except IOError:
            return 84

    def test_colours(self) -> None:
        """ Display all the available colours and their code """
        print("Displaying all available colours:")
        counter = 0
        for background in "0123456789ABCDEFr":
            for foreground in "0123456789ABCDEFr":
                counter += 1
                self.display("rr", (), "\n")
                self.display(
                    f"{background}{foreground}",
                    (),
                    f"Current colour: '{background}{foreground}'"
                )
        self.display(
            "rr", (), f"\n{counter} Colours displayed.\n"
        )


if __name__ == '__main__':
    CI = ColouriseOutput()
    CI.init_pallet()
    CI.test_colours()
    CI.display("0A", (), "Hello World !\n")
    CI.display("rr", "")
    CI.unload_ressources()
    print(f"Created by {CI.author}")
