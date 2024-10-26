from Gen import Gen
import random

#Ранговая селекция

def f(x):
    return 2 * (x ** 2) + 1

def generate_population(x_min, x_max, count, length):
    population = []
    sum_adapt = 0
    for i in range(count):
        x = random.randint(x_min, x_max)
        gen = Gen(length, x=x)
        adapt = f(x)
        sum_adapt += adapt
        info = {
            'gen': gen,
            'adapt': adapt
        }
        population.append(info)
    return (population, adapt)

def mutate_population(gens, p_mutation):
    for gen in gens:
        if random.random() < p_mutation:
            gen.mutate()

def main():
    p_mutation = 0.6
    length = 4
    count = 4
    x_min = 0
    x_max = 15
    population, sum_adapt = generate_population(x_min, x_max, count, length)
    step = 1
    max_steps = 100
    
    relative_adapt = [ 100*gen_info['adapt']/sum_adapt for gen_info in population ]
    gens = [ gen_info['gen'] for gen_info in population ]
    
    max_ind = relative_adapt.index(max(relative_adapt))
    best_gen = gens[max_ind]
    best_adapt = best_gen.apply(f)

    while step <= max_steps:
        gens_to_cross = [ random.choices(gens, relative_adapt, k=1)[0] for _ in range(count) ]
        mutate_population(gens_to_cross, p_mutation)
        new_gens = []
        sum_adapt = 0
        for i in range(int(count / 2)):
            gens_to_add = gens_to_cross[2*i].cross(gens_to_cross[2*i+1])
            sum_adapt += gens_to_add[0].apply(f) + gens_to_add[1].apply(f)
            new_gens += gens_to_add

        gens = new_gens
        relative_adapt = [ 100*gen.apply(f)/sum_adapt for gen in gens ]
        max_ind = relative_adapt.index(max(relative_adapt))
        max_gen = gens[max_ind]
        max_adapt = best_gen.apply(f)
        if max_adapt > best_adapt:
            best_gen = max_gen
            best_adapt = max_adapt
        

        print(f'Поколение {step:>4}: ', end='')
        [ print(gen, end=' ') for gen in gens ]
        print(f'\tЛучший ген {best_gen}. Лучшая приспособленность {best_adapt}')
        print('\t\t', end='')
        [ print(f'{r_adapt:.0f}', end=' ') for r_adapt in relative_adapt ]
        print()
        step += 1
    



if __name__ == '__main__':
    main()