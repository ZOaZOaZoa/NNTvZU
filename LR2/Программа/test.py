from Gen import Gen

def genTest1():
    gen = Gen(5, x=5)
    assert gen.code == [0, 0, 1, 0, 1], gen.code
    assert str(gen) == '00101', str(gen)

    code = '00101'
    gen.mutate()
    diff_count = 0
    for i, elem in enumerate(str(gen)):
        if code[i] != elem:
            diff_count += 1
    
    assert diff_count == 1, f'Неудачная мутация. Было {code}, стало {gen}'




def main():
    genTest1()
    print('genTest1 пройден')

if __name__ == '__main__':
    main()

