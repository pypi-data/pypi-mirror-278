def bitshift(num:int, amount:int, direction:str = "left"):
    """ Bitshift an integer right or left with specified amount

    Parameters
    ----------
    num:int, amount:int, direction:str = "left"
        The data takes in integer values
    Returns
    -------
    int
        The data returns a decimal value
    """
    if direction == 'left':
        shifted = num << amount
    elif direction == 'right':
        shifted = num >> amount
    
    return shifted