import random

# Parámetros del algoritmo
TARGET = "INTELIGENCIA"  # Palabra objetivo
POPULATION_SIZE = 100    # Tamaño de la población
MUTATION_RATE = 0.1      # Probabilidad de mutación
GENERATIONS = 1000       # Número máximo de generaciones

# Generar una cadena aleatoria
def random_string(length):
    return ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ ") for _ in range(length))

# Función de aptitud: cuenta caracteres correctos en posición correcta
def fitness(individual):
    return sum(1 for i, char in enumerate(individual) if char == TARGET[i])

# Selección por ruleta
def roulette_selection(population, fitnesses):
    total_fitness = sum(fitnesses)
    pick = random.uniform(0, total_fitness)
    current = 0
    for individual, fit in zip(population, fitnesses):
        current += fit
        if current > pick:
            return individual

# Cruza entre dos padres
def crossover(parent1, parent2):
    point = random.randint(0, len(TARGET) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

# Mutación de un individuo
def mutate(individual):
    if random.random() < MUTATION_RATE:
        idx = random.randint(0, len(individual) - 1)
        new_char = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ ")
        individual = individual[:idx] + new_char + individual[idx+1:]
    return individual

# Algoritmo genético
def genetic_algorithm():
    population = [random_string(len(TARGET)) for _ in range(POPULATION_SIZE)]

    for generation in range(GENERATIONS):
        fitnesses = [fitness(ind) for ind in population]
        
        # Verificar si se encontró la solución
        if TARGET in population:
            print(f"Solución encontrada en generación {generation}")
            return population[population.index(TARGET)]

        # Crear la nueva generación
        new_population = []
        while len(new_population) < POPULATION_SIZE:
            parent1 = roulette_selection(population, fitnesses)
            parent2 = roulette_selection(population, fitnesses)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1))
            if len(new_population) < POPULATION_SIZE:
                new_population.append(mutate(child2))

        population = new_population

    print("No se encontró solución dentro del límite de generaciones.")
    return None

# Ejecutar el algoritmo
best_solution = genetic_algorithm()
if best_solution:
    print("Mejor solución:", best_solution)
else:
    print("No se encontró una solución.")
