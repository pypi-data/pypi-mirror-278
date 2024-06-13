def format_text(text):
    """
    Formats the text based on its type.

    - If the text is an integer, it will have no decimal places.
    - If the text is a decimal number, it will keep two decimal places.
    - If the text is a string, it will be kept as is.

    Args:
    text (str): The text to format.

    Returns:
    str: The formatted text.
    """
    try:
        # Try to convert the text to an integer
        int_value = int(text)
        return str(int_value)
    except ValueError:
        try:
            # Try to convert the text to a float
            float_value = float(text)
            return f"{float_value:.2f}"
        except ValueError:
            # If it's neither an int nor a float, return the original text
            return text
