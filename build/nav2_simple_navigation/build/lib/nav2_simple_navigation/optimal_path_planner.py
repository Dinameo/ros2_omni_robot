import random
import math


class OptimalPathPlanner:
    def __init__(self, room_data):
        self.room_data = room_data
        self.distances = {}

    def calculate_distances(self, room_names):


        point = {
            name: [self.room_data[name]['x'], self.room_data[name]['y']]

            for name in room_names
        }

        for i, name_i in enumerate(room_names):
            for j, name_j in enumerate(room_names):


                if i != j:
                    p1 = point[name_i]
                    p2 = point[name_j]
                    dist = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
                    self.distances[(name_i, name_j)] = dist
    def distance_between(self, room1, room2):
        return self.distances.get((room1, room2), 0)
    
    def calculate_route_cost(self, route):
        cost = 0
        for i in range(len(route)):
            cost += self.distance_between(route[i], route[(i + 1) % len(route)])
        return cost

    def crossover(self, parent1, parent2):
        chromosome_len = len(parent1)
        a, b = sorted(random.sample(range(chromosome_len), 2))
        child = [-1] * chromosome_len
        child[a:b] = parent1[a:b]

        fill = [gene for gene in parent2 if gene not in child]
        idx = 0
        for i in range(chromosome_len):
            if child[i] == -1:
                child[i] = fill[idx]
                idx += 1
        return child
    def mutate(self, route):

        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]
        return route
    def find_optimal_route(self, room_names, generations=50, pop_size=50):
        self.calculate_distances(room_names)
        population = [room_names.copy() for _ in range(pop_size)]
        for p in population:
            random.shuffle(p)
        best_costs = []

        for gen in range(generations):
            population.sort(key=lambda r: self.calculate_route_cost(r))
            best_cost = self.calculate_route_cost(population[0])
            best_costs.append(best_cost)

            new_pop = population[:10]  # Elitism

            for _ in range(32):
                p1, p2 = random.sample(population[:25], 2)
                new_pop.append(self.crossover(p1.copy(), p2.copy()))

            for _ in range(14):
                p = random.choice(population[:20])
                new_pop.append(self.mutate(p.copy()))
            for _ in range(4):
                route = room_names.copy()
                random.shuffle(route)
                new_pop.append(route)
            population = new_pop
        best_route = min(population, key=lambda r: self.calculate_route_cost(r))
        return best_route