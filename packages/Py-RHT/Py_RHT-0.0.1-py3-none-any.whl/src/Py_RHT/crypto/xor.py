def xor(data:bytes, key:bytes) -> bytearray:
    """ Simple xor with variable length input

    Built to run xor on any length of data and key as long as the key is shorter than the data being xor'd against

    Parameters
    ----------
    data : bytes
        The data to be xor'd
    key : bytes
        The key that is xor'd against the data, has to be smaller than the data

    Returns
    -------
    bytearray
        a bytearray that contains the result of the xor
    """
    if type(data) != bytes:
        raise TypeError(f"Invalid input data type: {type(data)}")
    elif type(key) != bytes:
        raise TypeError(f"Invalid input data type: {type(key)}") 
    output = []
    i = 0
    while i < len(data):
        output.append(data[i]^key[i % len(key)])
        i += 1
    return bytearray(output)

def bruteforce(data:bytes) -> None:
    '''
    Perform a brute force XOR operation on the given data with single-byte keys.

    This function attempts to decrypt or transform the input data by XORing it with every possible
    single-byte key from 0x01 to 0xFF (1 to 255 in decimal).

    Parameters
    ----------
    data : bytes
        The data to be XOR'd. This is typically encrypted or obfuscated data that you want to decrypt or analyze.
        
    Returns
    -------
    None
        This function does not return any value. It prints the results of each XOR operation directly.
    '''
    for key in range(1, 256):
        key_bytes = bytes([key])
        output = xor(data, key_bytes)

        output_str = output.decode('latin1')  
        
        print(f"Key = {key:02x}: {output_str}")
