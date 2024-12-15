from flask import Flask, render_template, request
import random
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Funciones auxiliares
def random_string(length):
    return ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ ") for _ in range(length))

def fitness(individual, target):
    return sum(1 for i, char in enumerate(individual) if char == target[i])

def roulette_selection(population, fitnesses):
    total_fitness = sum(fitnesses)
    pick = random.uniform(0, total_fitness)
    current = 0
    for individual, fit in zip(population, fitnesses):
        current += fit
        if current > pick:
            return individual

def crossover(parent1, parent2, length):
    point = random.randint(0, length - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(individual, mutation_rate):
    if random.random() < mutation_rate:
        idx = random.randint(0, len(individual) - 1)
        new_char = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ ")
        individual = individual[:idx] + new_char + individual[idx+1:]
    return individual

# Algoritmo genético
def genetic_algorithm(target, population_size, mutation_rate, generations):
    population = [random_string(len(target)) for _ in range(population_size)]
    avg_fitness_history = []
    max_fitness_history = []
    best_solution = None
    best_generation = -1

    for generation in range(generations):
        fitnesses = [fitness(ind, target) for ind in population]
        
        # Registrar aptitud promedio y máxima
        avg_fitness_history.append(sum(fitnesses) / len(fitnesses))
        max_fitness_history.append(max(fitnesses))

        # Verificar si se encontró la solución
        if target in population:
            best_solution = target
            best_generation = generation
            break

        # Crear la nueva generación
        new_population = []
        while len(new_population) < population_size:
            parent1 = roulette_selection(population, fitnesses)
            parent2 = roulette_selection(population, fitnesses)
            child1, child2 = crossover(parent1, parent2, len(target))
            new_population.append(mutate(child1, mutation_rate))
            if len(new_population) < population_size:
                new_population.append(mutate(child2, mutation_rate))

        population = new_population

    return avg_fitness_history, max_fitness_history, best_solution, best_generation

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    graph_url = None
    if request.method == "POST":
        target = request.form["target"]
        population_size = int(request.form["population_size"])
        mutation_rate = float(request.form["mutation_rate"])
        generations = int(request.form["generations"])

        avg_fitness, max_fitness, best_solution, best_generation = genetic_algorithm(
            target, population_size, mutation_rate, generations
        )

        # Crear gráfica con fondo transparente
        plt.figure(figsize=(10, 6))
        plt.plot(avg_fitness, label="Aptitud promedio", color="#70a1ff", linewidth=2)
        plt.plot(max_fitness, label="Aptitud máxima", color="#ff7f50", linewidth=2)
        plt.xlabel("Generaciones", color="white")
        plt.ylabel("Aptitud", color="white")
        plt.title(f"Evolución de la aptitud hacia '{target}'", color="white")
        plt.legend(facecolor="black", edgecolor="white", labelcolor="white")
        plt.grid(color="gray", linestyle="--", linewidth=0.5)

        # Personalizar ejes y colores para fondo oscuro
        ax = plt.gca()
        ax.set_facecolor("none")  # Fondo interno del gráfico transparente
        ax.spines["bottom"].set_color("white")
        ax.spines["left"].set_color("white")
        ax.tick_params(axis="x", colors="white")
        ax.tick_params(axis="y", colors="white")

        # Guardar la gráfica con fondo completamente transparente
        buf = io.BytesIO()
        plt.savefig(buf, format="png", transparent=True)  # Aquí se define transparencia
        buf.seek(0)
        graph_url = base64.b64encode(buf.getvalue()).decode("utf-8")
        buf.close()

        # Resultados
        result = {
            "target": target,
            "best_solution": best_solution,
            "best_generation": best_generation,
            "population_size": population_size,
            "mutation_rate": mutation_rate,
            "generations": generations
        }

    return render_template("index.html", result=result, graph_url=graph_url)


if __name__ == "__main__":
    app.run(debug=True)
