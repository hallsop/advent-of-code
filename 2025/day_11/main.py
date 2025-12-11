from functools import cache
from collections import deque

def bfs(nodes, initial, end, must_have: list = []):
    queue = deque()
    path = []
    path.append(initial)
    queue.append(path.copy())

    all_paths = []
    i = 0
    while queue:
        i += 1
        path = queue.popleft()
        last = path[-1]
        if last == end:
            is_valid = True
            for item in must_have:
                if item not in path:
                    is_valid = False
            if is_valid:
                all_paths.append(path)
            continue
        if last in nodes:
            for dest in nodes[last]:
                if dest not in path:
                    new_path = path.copy()
                    new_path.append(dest)
                    queue.append(new_path)
    return all_paths

if __name__ == '__main__':
    nodes = {}
    with open('input', 'r') as f:
        for line in f.readlines():
            line_str = line.strip()
            key = line_str.split(':')[0]
            vals = line_str.split(':')[1].strip().split(' ')
            nodes[key] = vals

    print(len(bfs(nodes, initial='you', end='out')))


    @cache
    def dfs(initial, end, dac=False, fft=False):
        if initial == 'dac':
            dac = True
        if initial == 'fft':
            fft = True
        if end == initial:
            return 1 if dac and fft else 0
        return sum([dfs(dest, end, dac, fft) for dest in nodes[initial]])


    num_paths = dfs(initial='svr', end='out')

    print(num_paths)