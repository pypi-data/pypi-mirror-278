def addition(number_one, number_two):
    """
    Function to add two numbers together.

    Args:
        number_one (float or int): first number.
        number_two (float or int): Second number.

    Returns:
        float: Result of the addition.
    """
    return number_one + number_two


def subtraction(number_one, number_two):
    """
    Function to subtract two numbers together.

    Args:
        number_one (float or int): first number.
        number_two (float or int): Second number.

    Returns:
        float: Result of the subtraction.
    """
    return number_one - number_two


def multiplication(number_one, number_two):
    """
    Function to multiply two numbers together.

    Args:
        number_one (float or int): first number.
        number_two (float or int): Second number.

    Returns:
        float: Result of the multiplication.
    """
    return number_one * number_two


def division(number_one, number_two):
    """
    Function to divide two numbers together.

    Args:
        number_one (float or int): first number.
        number_two (float or int): Second number (not zero).

    Returns:
        float: Result of the division.
    """
    if number_two == 0:
        raise ZeroDivisionError("Zero is not allowed")
    return number_one / number_two