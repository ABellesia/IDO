import math
import time
from collections import deque
import random
import matplotlib.pyplot as plt

# 1. Leer las Coordenadas de las Ciudades
def read_coordinates(file_path):
    """
    Lee las coordenadas de las ciudades desde un archivo y las retorna como un diccionario.
    Cada entrada tiene la forma {ciudad_id: (x, y)}.
    """
    cities = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():  # Ignorar líneas vacías
                parts = line.split()
                if parts[0].isdigit():  # Verificar que la primera parte sea un número
                    city_id = int(parts[0])
                    x, y = map(float, parts[1:])
                    cities[city_id] = (x, y)
    return cities

# 2. Crear el Diccionario de Distancias
def create_distance_dictionary(cities):
    """
    Crea un diccionario de distancias basado en las coordenadas de las ciudades.
    Retorna un diccionario con claves como (ciudad1, ciudad2) y sus respectivas distancias.
    """
    distances = {}
    city_ids = list(cities.keys())
    for i in range(len(city_ids)):
        for j in range(i + 1, len(city_ids)):
            dist = math.sqrt((cities[city_ids[i]][0] - cities[city_ids[j]][0]) ** 2 +
                             (cities[city_ids[i]][1] - cities[city_ids[j]][1]) ** 2)
            distances[(city_ids[i], city_ids[j])] = dist
            distances[(city_ids[j], city_ids[i])] = dist  # Asegurar simetría
    return distances, city_ids

# 3. Heurística del Vecino Más Cercano
def nearest_neighbor_heuristic(distances, city_ids):
    """
    Genera una solución inicial al problema del TSP usando la heurística del vecino más cercano.
    
    Parameters:
        distances: Diccionario de distancias entre ciudades.
        city_ids: Lista de IDs de las ciudades.
    Returns:
        Una ruta inicial y su distancia total.
    """
    n = len(city_ids)
    visited = {city: False for city in city_ids}
    current_city = city_ids[0]  # Comenzar con la primera ciudad
    route = [current_city]
    visited[current_city] = True
    total_distance = 0

    for _ in range(n - 1):
        nearest_city = None
        min_distance = float('inf')
        for next_city in city_ids:
            if not visited[next_city]:
                dist = distances.get((current_city, next_city), float('inf'))
                if dist < min_distance:
                    nearest_city = next_city
                    min_distance = dist

        route.append(nearest_city)
        total_distance += min_distance
        visited[nearest_city] = True
        current_city = nearest_city

    # Volver a la ciudad inicial
    total_distance += distances.get((current_city, route[0]), float('inf'))
    route.append(route[0])

    return route, total_distance

# 4. Algoritmo 2-Opt
def two_opt_heuristic(distances, initial_route, max_iterations=1000):
    """
    Aplica la heurística 2-opt para mejorar una ruta inicial.
    
    Parameters:
        distances: Diccionario de distancias entre ciudades.
        initial_route: Ruta inicial a optimizar.
        max_iterations: Número máximo de iteraciones permitidas.
    Returns:
        Una ruta optimizada y su distancia total.
    """
    def calculate_total_distance(route):
        return sum(distances.get((route[i], route[i + 1]), float('inf')) for i in range(len(route) - 1))

    route = initial_route[:]
    best_distance = calculate_total_distance(route)
    improved = True
    iteration = 0

    while improved and iteration < max_iterations:
        improved = False
        iteration += 1
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route) - 1):
                # Generar una nueva ruta invirtiendo la sección entre i y j
                new_route = route[:i] + route[i:j + 1][::-1] + route[j + 1:]
                new_distance = calculate_total_distance(new_route)
                if new_distance < best_distance:
                    route = new_route
                    best_distance = new_distance
                    improved = True

        # Monitorear el progreso
        print(f"Iteración {iteration}: Mejor distancia = {best_distance}")

    return route, best_distance

# ****************************************************************************
# Algoritmo de búsqueda tabu
def tabu_search(distances, initial_route, max_iterations=1000, tabu_tenure=20, no_improvement_limit=50):
    """
    Aplica la Búsqueda Tabú para optimizar una ruta inicial.
    
    Parameters:
        distances: Diccionario de distancias entre ciudades.
        initial_route: Ruta inicial para optimizar.
        max_iterations: Número máximo de iteraciones.
        tabu_tenure: Tamaño de la lista tabú.
        no_improvement_limit: Límite de iteraciones sin mejora.
    Returns:
        Ruta optimizada y su distancia total.
    """
    def calculate_total_distance(route):
        return sum(distances.get((route[i], route[i + 1]), float('inf')) for i in range(len(route) - 1))

    def two_opt_swap(route, i, j):
        """
        Realiza un intercambio 2-opt entre los índices i y j.
        """
        new_route = route[:]
        new_route[i:j + 1] = reversed(new_route[i:j + 1])
        return new_route

    # Inicializar solución
    current_route = initial_route[:]
    best_route = initial_route[:]
    current_distance = calculate_total_distance(current_route)
    best_distance = current_distance
    tabu_list = deque(maxlen=tabu_tenure)
    iteration = 0
    no_improvement_counter = 0

    while iteration < max_iterations and no_improvement_counter < no_improvement_limit:
        iteration += 1
        neighbors = []

        # Generar vecinos con 2-opt
        for i in range(1, len(current_route) - 2):
            for j in range(i + 1, len(current_route) - 1):
                if (i, j) not in tabu_list:
                    neighbor = two_opt_swap(current_route, i, j)
                    neighbor_distance = calculate_total_distance(neighbor)
                    neighbors.append((neighbor, neighbor_distance, (i, j)))

        # Ordenar vecinos por distancia
        neighbors.sort(key=lambda x: x[1])

        # Seleccionar el mejor vecino que no esté en la lista tabú
        if neighbors:
            best_neighbor, best_neighbor_distance, move = neighbors[0]
            tabu_list.append(move)

            # Actualizar la solución actual
            current_route = best_neighbor
            current_distance = best_neighbor_distance

            # Actualizar la mejor solución encontrada
            if current_distance < best_distance:
                best_route = current_route[:]
                best_distance = current_distance
                no_improvement_counter = 0  # Reiniciar contador de no mejora
            else:
                no_improvement_counter += 1

        # Monitorear el progreso
        print(f"Iteración {iteration}: Mejor distancia = {best_distance} (Sin mejora: {no_improvement_counter})")

    return best_route, best_distance

#------------------------------------------------------------------------------

# 6. Función para Graficar

def plot_route(cities, route, title):
    """
    Grafica la ruta de las ciudades en un mapa.
    """
    x = [cities[city][0] for city in route]
    y = [cities[city][1] for city in route]

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker="o", color="b", linestyle="-", label="Ruta")
    for i, city in enumerate(route):
        plt.text(cities[city][0], cities[city][1], str(city), fontsize=9, color="red")

    plt.title(title)
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.grid(True)
    plt.legend()
    plt.show()


# 7 Método de recocido simulado 
def simulated_annealing(distances, initial_route, initial_temperature=1000, cooling_rate=0.995, max_iterations=1000):
    """
    Optimiza una ruta utilizando el algoritmo de Recocido Simulado.

    Parámetros:
    - distances: Diccionario de distancias entre las ciudades.
    - initial_route: Ruta inicial para iniciar la optimización.
    - initial_temperature: Temperatura inicial para el algoritmo.
    - cooling_rate: Factor de enfriamiento (debe ser menor a 1).
    - max_iterations: Número máximo de iteraciones.

    Retorna:
    - best_route: La mejor ruta encontrada.
    - best_distance: La distancia de la mejor ruta encontrada.
    """
    def calculate_total_distance(route):
        return sum(distances.get((route[i], route[i + 1]), float('inf')) for i in range(len(route) - 1))
    
    def swap_two_cities(route):
        """Genera un vecino al intercambiar dos ciudades aleatoriamente."""
        i, j = random.sample(range(1, len(route) - 1), 2)  # Evitar cambiar la primera y última ciudad
        new_route = route[:]
        new_route[i], new_route[j] = new_route[j], new_route[i]
        return new_route

    # Inicializar solución
    current_route = initial_route[:]
    current_distance = calculate_total_distance(current_route)
    best_route = current_route[:]
    best_distance = current_distance
    temperature = initial_temperature

    for iteration in range(max_iterations):
        # Generar un vecino
        new_route = swap_two_cities(current_route)
        new_distance = calculate_total_distance(new_route)
        
        # Decidir si aceptar el vecino
        if new_distance < current_distance or random.random() < math.exp((current_distance - new_distance) / temperature):
            current_route = new_route
            current_distance = new_distance

        # Actualizar la mejor solución encontrada
        if current_distance < best_distance:
            best_route = current_route[:]
            best_distance = current_distance

        # Enfriar la temperatura
        temperature *= cooling_rate

        # Monitorear progreso
        if iteration % 100 == 0 or iteration == max_iterations - 1:
            print(f"Iteración {iteration}: Mejor distancia = {best_distance}, Temperatura = {temperature:.2f}")

        # Finalizar si la temperatura es demasiado baja
        if temperature < 1e-8:
            break

    return best_route, best_distance

# Método para generar una tabla de comparación 
def generate_comparison_table(methods_results):
    """
    Genera una tabla comparativa con los resultados de cada método.
    
    Parameters:
        methods_results (list): Lista de tuplas con resultados de los métodos.
            Cada tupla contiene (nombre_método, distancia_optimizada, tiempo_ejecución).
    """
    # Imprimir encabezado
    print("\nComparación de Métodos")
    print(f"{'Método':<20} {'Distancia Optimizada':<20} {'Tiempo de Ejecución (s)':<20}")
    print("-" * 60)

    # Imprimir resultados de cada método
    for method_name, distance, execution_time in methods_results:
        print(f"{method_name:<20} {distance:<20.4f} {execution_time:<20.4f}")


# --------------------------------------------------------------------------
# 8 Función Principal
def main():
    file_path = "Qatar.txt"  # Cambia a la ruta de tu archivo
    cities = read_coordinates(file_path)

    # Crear el diccionario de distancias
    distances, city_ids = create_distance_dictionary(cities)

    # Generar ruta inicial con Vecino Más Cercano
    print("\nGenerando ruta inicial con Vecino Más Cercano:")
    start = time.time()
    initial_route, initial_distance = nearest_neighbor_heuristic(distances, city_ids)
    end = time.time()
    print("Ruta inicial:", initial_route)
    print("Distancia inicial:", initial_distance)
    print("Tiempo de ejecución:", end - start)
    
    # Lista para almacenar resultados
    methods_results = []

    # Mejorar la ruta con 2-Opt
    print("\nMejorando ruta con 2-Opt:")
    start = time.time()
    optimized_route, optimized_distance = two_opt_heuristic(distances, initial_route)
    end = time.time()
    print("Ruta optimizada:", optimized_route)
    print("Distancia optimizada:", optimized_distance)
    print("Tiempo de ejecución:", end - start)

    methods_results.append(("2-Opt", optimized_distance, end - start))
    
    plot_route(cities, optimized_route, title="Ruta Optimizada con 2-Opt")

    # Optimizar la ruta con Búsqueda Tabú
    print("\nOptimizando ruta con Búsqueda Tabú:")
    start = time.time()
    optimized_route_tabu, optimized_distance_tabu = tabu_search(
        distances, initial_route, max_iterations=10, tabu_tenure=30, no_improvement_limit=5
    )
    end = time.time()
    print("Ruta optimizada (Búsqueda Tabú):", optimized_route_tabu)
    print("Distancia optimizada (Búsqueda Tabú):", optimized_distance_tabu)
    print("Tiempo de ejecución:", end - start)
    
    methods_results.append(("Búsqueda Tabú", optimized_distance_tabu, end - start))
    
    
    plot_route(cities, optimized_route_tabu, title="Ruta Optimizada con Tabu")
    
    # Optimizar la ruta con Recocido Simulado
    print("\nOptimizando ruta con Recocido Simulado:")
    start = time.time()
    optimized_route_sa, optimized_distance_sa = simulated_annealing(
        distances, initial_route, initial_temperature=1000, cooling_rate=0.995, max_iterations=100
    )
    end = time.time()
    print("Ruta optimizada (Recocido Simulado):", optimized_route_sa)
    print("Distancia optimizada (Recocido Simulado):", optimized_distance_sa)
    print("Tiempo de ejecución:", end - start)
    
    plot_route(cities, optimized_route_sa, title="Ruta Optimizada con Recocido Simulado")
    
    methods_results.append(("Recocido Simulado", optimized_distance_sa, end - start))

    # Generar tabla comparativa
    generate_comparison_table(methods_results)

    

if __name__ == "__main__":
    main()
