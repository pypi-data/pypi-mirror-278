# colourise_output

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/colourise_output)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/colourise_output)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/colourise_output)
![PyPI - Version](https://img.shields.io/pypi/v/colourise_output?label=pypi%20package:%20colourise_output)
![PyPI - Downloads](https://img.shields.io/pypi/dm/colourise_output)
![PyPI - License](https://img.shields.io/pypi/l/colourise_output)
![Execution status](https://github.com/Hanra-s-work/colourise_output/actions/workflows/python-package.yml/badge.svg)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/Hanra-s-work/colourise_output/python-package.yml)
![GitHub repo size](https://img.shields.io/github/repo-size/Hanra-s-work/colourise_output)
![GitHub Repo stars](https://img.shields.io/github/stars/Hanra-s-work/colourise_output)
![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/m/Hanra-s-work/colourise_output)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/Hanra-s-work/colourise_output/main)

[![Static Badge](https://img.shields.io/badge/Buy_me_a_tea-Hanra-%235F7FFF?style=flat-square&logo=buymeacoffee&label=Buy%20me%20a%20coffee&labelColor=%235F7FFF&color=%23FFDD00&link=https%3A%2F%2Fwww.buymeacoffee.com%2Fhanra)](https://www.buymeacoffee.com/hanra)

## Description

This is a module that allows you the change the colour of the terminal using the batch colour syntax.
It works on all known platforms.

## Table of Content

1. [colourise_output](#colouriseoutput)
2. [Description](#description)
3. [Table of Content](#table-of-content)
4. [Installation](#installation)
    1. [Using pip](#using-pip)
    2. [Using python](#using-python)
5. [Usage](#usage)
    1. [Importing](#importing)
    2. [Initialising](#initialising)
    3. [Calling the test_colours function](#calling-the-testcolours-function)
        1. [Epilepsy warning](#epilepsy-warning)
    4. [Changing the colour](#changing-the-colour)
        1. [Displaying text and the colour](#displaying-text-and-the-colour)
        2. [Only changing the colour](#only-changing-the-colour)
6. [Available colours](#available-colours)
7. [Change the initialisation content](#change-the-initialisation-content)
    1. [Changing the forbidden characters](#changing-the-forbidden-characters)
    2. [Changing the description](#changing-the-descriptions)
    3. [Changing both](#changing-both)
8. [Author](#author)
9. [Version](#version)

## Installation

### Using pip

```sh
pip install -U colorama
pip install -U colourise-output
```

### Using python

Under windows:

```bat
py -m pip install -U colorama
py -m pip install -U colourise-output
```

Under Linux/Mac OS:

```sh
python3 -m pip install -U colorama
python3 -m pip install -U colourise-output
```

## Usage

### Importing

```py
import colourise_output as co
```

### Initialising

The generic class is: `ColouriseOutput()`
The generic loading function is: `init_ressources(self)`
The output is: None

```py
COI = co.ColouriseOutput()
COI.init_ressources()
```

### Calling the test_colours function

The generic function is:

```py
test_colours(self, delay:int=0)
```

The output is: None

```py
COI.test_colours()
```

Calling this function will result in the function displaying all the available colours as well as their colour code (what you use to call them).

#### Epilepsy warning

Warning: Avoid this function if you are epileptic or set the delay to 1

```py
COI.test_colours(1)
```

### Changing the colour

The generic function to ask a question is:

```py
display(self, colour:str, attributes:tuple=(), text:str="")
```

The outputs of this function is: None
The terminal will display the next lines in the desired colour.

#### Displaying text and the colour

```py
COI.display("0A", (), "Hello World !\n")
```

The text "Hello World" will be displayed in green (A) on a black background (0).

#### Only changing the colour

```py
answer = AQI.ask_question("How old are you?", "uint")
ADD_S = ""
if answer > 1:
    ADD_S = "s"
print(f"You are {answer} year{ADD_S} old !")
```

## Available colours

Here is the windows colour pallet and how to use it:

### Windows colour pallet

* 0: Black
* 1: Blue
* 2: Green
* 3: Aqua
* 4: Red
* 5: Purple
* 6: Yellow
* 7: White
* 8: Gray
* 9: Light Blue
* A: Light Green
* B: Light Aqua
* C: Light Red
* D: Light Purple
* E: Light Yellow
* F: Bright White

### Using the Windows colour pallet

## Change the initialisation content

When initialising the class it is possible to change the forbidden characters and/or the descriptions of the available types.

### changing the forbidden characters

```py
import ask_question as aq
illegal_characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \\t\\n\\r\\x0b\\x0c"
illegal_characters = illegal_characters.replace("0123456789","")
AQI = aq.AskQuestion(dict(), illegal_characters)
```

This initialisation has changed the characters that will be allowed for the number conversion in the 'int' and 'float' options.

### Changing the descriptions

```py
import ask_question as aq
human_type = {
    "int":"whole number (-1, 0, 1, 2, 3, etc...)",
    "float":"floating number (-1.2, 0.1, 1.2, etc...)",
    "uint":"whole positive number (0, 1, 2, etc...)",
    "ufloat":"whole positive floating number (0.1, 1.2, etc ...)",
    "num":"numeric (numbers from 0 onwards)",
    "alnum":"alphanumeric (only numbers and the alphabet)",
    "isalpha":"alphabet (from a to z and A to Z)",
    "char":"alphabet (from a to z and A to Z)",
    "ascii":"ascii Table",
    "str":"string (any character you can type)",
    "version":"version (numbers seperated by '.' characters)",
    "ver":"version (numbers seperated by '.' characters)",
    "bool":"boolean (yes/True/1 or no/False/0 answer type)",
}
AQI = aq.AskQuestion(human_type)
```

This initialisation has changed the descriptions for the types.
When the user will enter a wrong answer, the description displayed for the type you were expecting will be taken from the human_type dictionnary you have entered.

### Changing both

```py
import ask_question as aq
illegal_characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \\t\\n\\r\\x0b\\x0c"
illegal_characters = illegal_characters.replace("0123456789","")
human_type = {
    "int":"whole number (-1, 0, 1, 2, 3, etc...)",
    "float":"floating number (-1.2, 0.1, 1.2, etc...)",
    "uint":"whole positive number (0, 1, 2, etc...)",
    "ufloat":"whole positive floating number (0.1, 1.2, etc ...)",
    "num":"numeric (numbers from 0 onwards)",
    "alnum":"alphanumeric (only numbers and the alphabet)",
    "isalpha":"alphabet (from a to z and A to Z)",
    "char":"alphabet (from a to z and A to Z)",
    "ascii":"ascii Table",
    "str":"string (any character you can type)",
    "version":"version (numbers seperated by '.' characters)",
    "ver":"version (numbers seperated by '.' characters)",
    "bool":"boolean (yes/True/1 or no/False/0 answer type)",
}
AQI = aq.AskQuestion(human_type)
```

You have now impacted the int and float typing as well as the 'type' descriptions.

## Author

This module was written by (c) Henry Letellier
Attributions are appreciated.

Quick way (I assume you have already initialised the class):

```py
print(f"AskQuestion is written by {AQI.author}")
```

## Version

The current version is 1.0.0

An easy way to display the version is:

```py
import ask_question as aq
print(f"Version : {aq.__Version__}")
```
