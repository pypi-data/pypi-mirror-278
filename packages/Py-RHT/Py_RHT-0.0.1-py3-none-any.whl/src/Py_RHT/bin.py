class bin(object):
    """ 
    Binary datatype

    """

    def __init__(self,obj) -> None:
        """
        Constructs binary datatype

        Paramaters
        ----------

        obj : str[1] | int < 256 | bytes
            The object to turn into a binary representation
        """

        #default values
        self.values = {
            128 : 0,
            64 : 0,
            32 : 0,
            16 : 0,
            8 : 0,
            4 : 0,
            2 : 0,
            1 : 0
        }

        #type matching to the specific object type TODO add support for more cases later
        match obj:
            case str():
                if len(obj) == 1:
                    self.__inttodata(int.from_bytes(bytes(obj,'ascii')))
                else:
                    raise TypeError(f"String provided {obj} is longer than char(1 byte)")
            case int():
                if obj < 255:
                    if obj >= 0:
                        self.__inttodata(obj)
                    else:
                        raise NotImplementedError("cannot handle negative integers (lower than 0)")
                else:
                    raise TypeError(f"too large integer {obj} (larger than 255)")
            case bytes():
                self.__inttodata(int.from_bytes(obj))
            case _:
                raise TypeError(f"Object provided {type(obj)} is invalid")
    
    def __inttodata(self,obj:int):
        if obj - 128 >= 0: obj -= 128;self.values[128] = 1
        if obj - 64 >= 0: obj -= 64;self.values[64] = 1
        if obj - 32 >= 0: obj -= 32;self.values[32] = 1
        if obj - 16 >= 0: obj -= 16;self.values[16] = 1
        if obj - 8 >= 0: obj -= 8;self.values[8] = 1
        if obj - 4 >= 0: obj -= 4;self.values[4] = 1
        if obj - 2 >= 0: obj -= 2;self.values[2] = 1
        if obj - 1 >= 0: obj -= 1;self.values[1] = 1


    def __str__(self) -> str: 
        return f"{self.values[128]}{self.values[64]}{self.values[32]}{self.values[16]}{self.values[8]}{self.values[4]}{self.values[2]}{self.values[1]}"

    def __len__(self) -> int: #TODO if in future more is added to the binary capabilities it needs to be actually calculated
        return 1