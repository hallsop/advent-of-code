import math
import tqdm
from copy import deepcopy

def calc_dist(coord1, coord2):
    return (coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2 + (coord1[2] - coord2[2]) ** 2

def min_idx(_list):
    return min(range(len(_list)), key=_list.__getitem__)

def process_dist(min_i, min_j, circuits):
    existing_circuits = []
    for idx, circuit in enumerate(circuits):
        if min_i in circuit and min_j in circuit:
            return 1
        if min_i in circuit and min_j not in circuit:
            existing_circuits.append(idx)
        if min_j in circuit and min_i not in circuit:
            existing_circuits.append(idx)

    if len(existing_circuits) == 1:
        if min_i not in circuits[existing_circuits[0]]:
            circuits[existing_circuits[0]].append(min_i)
        elif min_j not in circuits[existing_circuits[0]]:
            circuits[existing_circuits[0]].append(min_j)
        else:
            raise Exception
        return 1
    elif len(existing_circuits) > 1:
        for i in range(1, len(existing_circuits)):
            circuits[existing_circuits[0]] += circuits[existing_circuits[i]]
            circuits[existing_circuits[i]] = []
        return 1

    circuits.append([min_i, min_j])
    return 1

def num_connections(circuits):
    num = 0
    for circuit in circuits:
        num += len(circuit)-1
    return num

if __name__ == "__main__":
    with open('input') as f:
        coords = []
        for line in f.readlines():
            coords.append([int(coord) for coord in line.strip().split(',')])


    distances = []
    for i in range(len(coords)):
        distances.append([])
        for j in range(len(coords)):
            if i != j:
                distances[i].append(calc_dist(coords[i], coords[j]))
            else:
                distances[i].append(99999999999999999)

    circuits = []
    circuit_dists = []
    connections_made = 0
    num_to_break = 1000
    with tqdm.tqdm(total=num_to_break) as pbar:
        while True:
            min_i = min_idx([min(dist) for dist in distances])
            min_j = min_idx(distances[min_i])
            if distances[min_i][min_j] == 99999999999999999:
                continue
            connection = process_dist(min_i, min_j, circuits)
            connections_made += connection
            distances[min_i][min_j] = 99999999999999999
            distances[min_j][min_i] = 99999999999999999
            if connections_made == num_to_break:
                circuits_part_1 = deepcopy(circuits)
            if len(circuits) > 0 and len(circuits[0]) == len(coords):
                break
            pbar.update(connection)

    circuits_part_1 = [set(circuit) for circuit in circuits_part_1]
    circuits_part_1.sort(key=lambda c: len(c), reverse=True)

    print(math.prod((len(circuits_part_1[0]), len(circuits_part_1[1]), len(circuits_part_1[2]))))

    print(coords[min_i][0] * coords[min_j][0])