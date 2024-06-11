import binascii
base64_encoding = {
    "000000" : "A",
    "000001" : "B",
    "000010" : "C",
    "000011" : "D",
    "000100" : "E",
    "000101" : "F",
    "000110" : "G",
    "000111" : "H",
    "001000" : "I",
    "001001" : "J",
    "001010" : "K",
    "001011" : "L",
    "001100" : "M",
    "001101" : "N",
    "001110" : "O",
    "001111" : "P",
    "010000" : "Q",
    "010001" : "R",
    "010010" : "S",
    "010011" : "T",
    "010100" : "U",
    "010101" : "V",
    "010110" : "W",
    "010111" : "X",
    "011000" : "Y",
    "011001" : "Z",
    "011010" : "a",
    "011011" : "b",
    "011100" : "c",
    "011101" : "d",
    "011110" : "e",
    "011111" : "f",
    "100000" : "g",
    "100001" : "h",
    "100010" : "i",
    "100011" : "j",
    "100100" : "k",
    "100101" : "l",
    "100110" : "m",
    "100111" : "n",
    "101000" : "o",
    "101001" : "p",
    "101010" : "q",
    "101011" : "r",
    "101100" : "s",
    "101101" : "t",
    "101110" : "u",
    "101111" : "v",
    "110000" : "w",
    "110001" : "x",
    "110010" : "y",
    "110011" : "z",
    "110100" : "0",
    "110101" : "1",
    "110110" : "2",
    "110111" : "3",
    "111000" : "4",
    "111001" : "5",
    "111010" : "6",
    "111011" : "7",
    "111100" : "8",
    "111101" : "9",
    "111110" : "+",
    "111111" : "/",
}

def b64_encode(data:bytes|str) -> str:
    """ Encode Base 64 with variable length input

    Made to base64 encoding standard to inclue \"=\" at the end

    Parameters
    ----------
    data : bytes | str
        The data to be turned into a b64 string

    Returns
    -------
    str
        resulting string from the encode
    """
    if type(data) == bytes:
        midstr = ""
        for char in data:
            char = bin(char)[2:]
            while  len(char) < 8:
                char = "0" + char
            midstr += char
        i = 0
        addafter = ""
        while len(midstr) % 6 != 0:
            i += 1
            midstr += "0"
            if i == 2:
                i = 0
                addafter += "="
        outstr = ""
        for x in range(int(len(midstr)/6)):outstr += base64_encoding[midstr[(x*6):(x*6)+6]]
        return outstr + addafter
    elif type(data) == str:return b64_encode(bytes(data,"ascii"))
    else:raise TypeError(f"Incorrect type for encoding {type(data)}")



def b64_decode(data:bytes|str):
    """ Decode Base 64 with variable length input

    Made to base64 encoding standard to inclue \"=\" at the end

    Parameters
    ----------
    data : bytes | str
        The data to be turned back into a ascii string

    Returns
    -------
    str
        resulting string from the decode
    """
    if type(data) == bytes:
        data = data.split(b"\x3d")[0]
        midstr = ""
        outstr = []
        for char in data:
            char = list(base64_encoding.keys())[list(base64_encoding.values()).index(str(int.to_bytes(char),'ascii'))]
            midstr += char
        while len(midstr) % 8 != 0:
            midstr = midstr[:-1]
        for char in range(int(len(midstr)/8)):
            outstr.append(chr(int(midstr[(char*8):(char*8)+8],2)))
        return "".join(outstr)
    elif type(data) == str:return b64_decode(bytes(data,'ascii'))
    else:raise TypeError(f"Incorrect type for decoding {type(data)}")

    

        

