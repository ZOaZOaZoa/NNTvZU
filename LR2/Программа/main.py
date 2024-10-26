from Gen import Gen
import random
import numpy as np

def f(x):
    return 2 * (x ** 2) + 1

def selection(gens, relative_adapt, generation_size, method: str):
    valid_methods = {
        'classic',
        'rank'
    }
    if method not in valid_methods:
        raise ValueError(f'Указан несуществующий метод {method}. Возможные варианты: {repr(valid_methods)}')
    
    if method == 'classic':
        result = [ random.choices(gens, relative_adapt, k=1)[0] for _ in range(generation_size) ]

    select_distribution = {
        4: [2, 1, 1],
        6: [3, 2, 1],
        8: [3, 2, 2, 1]
    }
    if method == 'rank':
        if generation_size not in select_distribution:
            raise ValueError(f'Не определено распределение для выбора по ранговому методу для размера выборки {generation_size}')
        
        gens_ranked = np.array([gens, relative_adapt])
        gens_ranked = gens_ranked[:, gens_ranked[1,:].argsort()[::-1] ]

        result = []
        select_counts = select_distribution[generation_size]
        for i in range(len(select_counts)):
            
            result += [gens_ranked[0,i], ] * select_counts[i]
        
    return result


def generate_population(x_min, x_max, count, length):
    population = []
    sum_adapt = 0
    for _ in range(count):
        x = random.randint(x_min, x_max)
        gen = Gen(length, x=x)
        adapt = f(x)
        sum_adapt += adapt
        info = {
            'gen': gen,
            'adapt': adapt
        }
        population.append(info)
    return (population, sum_adapt)

def mutate_population(gens, p_mutation):
    for i, gen in enumerate(gens):
        if random.random() < p_mutation:
            gen.mutate()

def print_stats(gens, best_gen, best_adapt, relative_adapt, step, descriptive_log):
    print(f'Поколение {step:>4}: ', end='')
    [ print(gen, end=' ') for gen in gens ]
    print(f'\tЛучший ген {best_gen}. Лучшая приспособленность {best_adapt}')
    if descriptive_log:
        print('\t\t', end='')
        [ print(f'{r_adapt:>3.0f}%', end=' ') for r_adapt in relative_adapt ]
        print()

def print_gens(text, gens):
    print(f'{text}', end='')
    [ print(gen, end=' ') for gen in gens ]
    print()



def main():
    #Общие параметры
    p_mutation = 0.1
    gen_length = 4
    generation_size = 4
    selection_method = 'rank'
    max_steps = 10
    descriptive_log = True
    
    #Параметры генерации
    x_min = 0
    x_max = 15
    
    population, sum_adapt = generate_population(x_min, x_max, generation_size, gen_length)
    relative_adapt = [ 100*gen_info['adapt']/sum_adapt for gen_info in population ]
    gens = [ gen_info['gen'] for gen_info in population ]

    max_ind = relative_adapt.index(max(relative_adapt))
    best_gen = str(gens[max_ind])
    best_adapt = gens[max_ind].apply(f)

    step = 1
    print_stats(gens, best_gen, best_adapt, relative_adapt, 1, descriptive_log)
    while step <= max_steps:
        #Селекция
        gens_to_cross = selection(gens, relative_adapt, generation_size, selection_method)
        if descriptive_log:
            print_gens('\tВыбраны для скрещивания: ', gens_to_cross)
    
        #Мутация
        mutate_population(gens_to_cross, p_mutation)
        if descriptive_log:
            print_gens('\tГены после мутации: ', gens_to_cross)

        #Скрещивание
        new_gens = []
        sum_adapt = 0
        for i in range(int(generation_size / 2)):
            gens_to_add = gens_to_cross[2*i].cross(gens_to_cross[2*i+1])
            sum_adapt += gens_to_add[0].apply(f) + gens_to_add[1].apply(f)
            new_gens += gens_to_add
        gens = new_gens
        relative_adapt = [ 100*gen.apply(f)/sum_adapt for gen in gens ]
        if descriptive_log:
            print_gens('\tРезультат скрещивания: ', gens)

        #Выбор лучшего
        max_ind = relative_adapt.index(max(relative_adapt))
        max_gen = gens[max_ind]
        max_adapt = gens[max_ind].apply(f)

        if max_adapt > best_adapt:
            best_gen = str(max_gen)
            best_adapt = max_adapt

            if descriptive_log:
                print(f'\tГен {max_gen} лучше {best_gen}, потому что {max_adapt} > {best_adapt}')
        
        #Печать поколения
        if descriptive_log:
            print()
        print_stats(gens, best_gen, best_adapt, relative_adapt, step+1, descriptive_log)
        
        step += 1
    

if __name__ == '__main__':
    main()