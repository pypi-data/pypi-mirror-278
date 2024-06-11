def reverse(data:str):
    """ Reverse a given string

    Parameters
    ----------
    data:str
        The data takes in a string
    Returns
    -------
    str
        The data returns the string reversed
    """
    flip = []
    for i in range(len(data) - 1, -1, -1):
        flip.append(data[i])

    return(''.join(flip))

        
