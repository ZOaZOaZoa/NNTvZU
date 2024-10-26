import random

class Gen():
    @staticmethod
    def intToBin(x: int):
        return bin(x)[2:]
    
    @staticmethod
    def binToInt(code: str):
        return int(code, 2)
    
    def __init__(self, length, code: list = None, x = None, binarizator = None):
        if binarizator:
            self.binarizator = binarizator
        else:
            self.binarizator = Gen.intToBin

        if x is not None:
            #Создание из изначального целочисленного объекта
            code = self.binarizator(x)
            if len(code) > length:
                raise ValueError(f'Длина полученного кода ({len(code)}) больше заданной длины хромосом ({length}).')
            
            if len(code) < length:
                code = '0' * (length - len(code)) + code
            code = [ int(char) for char in code ]
            self.code = code
        elif code is not None:
            #Создание из изначального кода
            self.code = code
        
        if len(code) != length:
                raise ValueError(f'Длина полученного кода ({len(code)}) больше заданной длины хромосом ({length}).')
        
        self.code_length = length

    def __str__(self):
        res = ''
        for elem in self.code:
            res += str(elem)
        return res

    def mutate(self):
        place = random.randint(0, self.code_length-1)
        self.code[place] = int(not self.code[place])
    
    def cross(self, otherGen: 'Gen') -> list:
        #Скрещивание
        if self.code_length != otherGen.code_length:
            raise ValueError('Длины кодов хромосом не совпадают')
        
        point = random.randint(1, self.code_length-1)
        code1 = self.code[:point] + otherGen.code[point:]
        gen1 = Gen(self.code_length, code=code1)
        code2 = otherGen.code[:point] + self.code[point:]
        gen2 = Gen(self.code_length, code=code2)
        return [gen1, gen2]

    def apply(self, func):
        value = Gen.binToInt(str(self))
        return func(value)
    