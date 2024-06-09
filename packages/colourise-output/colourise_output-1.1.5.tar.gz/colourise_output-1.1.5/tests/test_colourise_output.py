# tests/test_ask_question.py
from sys import stderr


def print_debug(string: str = "") -> None:
    """ Print debug messages """
    debug = False
    if debug is True:
        print(f"DEBUG: {string}", file=stderr)


def test_load() -> None:
    """ Test if the library loads  """
    try:
        from colourise_output import ColouriseOutput
    except ImportError:
        pass  # Handle the ImportError gracefully if running tests
    else:
        CO = ColouriseOutput()
        response = CO.init_pallet()
        print_debug(f"response = {response}")
        assert response == 0


def test_unload() -> None:
    """ Test if the library loads  """
    try:
        from colourise_output import ColouriseOutput
    except ImportError:
        pass  # Handle the ImportError gracefully if running tests
    else:
        CO = ColouriseOutput()
        response = CO.init_pallet()
        print_debug(f"response = {response}")
        response2 = CO.unload_ressources()
        print_debug(f"response = {response2}")
        assert response == 0
        assert response2 == 0


def test() -> None:
    """ This is a dummy test function """
    print("Hello World")
    assert 2 == 2
