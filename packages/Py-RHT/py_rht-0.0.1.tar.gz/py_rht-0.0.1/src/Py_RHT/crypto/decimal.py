def toDecimal(input:str) -> list:
    dec = []
    for char in input:
        dec.append(ord(char))

    return dec

def fromDecimal(input:list[int]) -> str:
    if type(input) == list:
        output = []
        for char in input:
            output.append(chr(char))

        return "".join(output)
    else:raise TypeError(f"Incorrect type for decoding {type(input)}")