

if __name__ == '__main__':
    lines = []
    with open('input', 'r') as f:
        for line in f.readlines():
            lines.append(line.strip())

    last_indicies = {lines[0].index('S')}
    count = 0
    num_paths = [0] * len(lines[0])
    num_paths[lines[0].index('S')] = 1
    for i in range(1, len(lines)):
        indices_to_check = last_indicies.copy()
        for j in indices_to_check:
            match lines[i][j]:
                case '.':
                    lines[i] = lines[i][:j] + "|" + lines[i][j+1:]
                case '^':
                    count += 1
                    num_paths[j-1] += num_paths[j]
                    num_paths[j+1] += num_paths[j]
                    num_paths[j] = 0
                    last_indicies.remove(j)
                    last_indicies.add(j-1)
                    last_indicies.add(j+1)
                    lines[i] = lines[i][:j-1] + "|" + lines[i][j] + "|" + lines[i][j+2:]
        print(lines[i])
    print(count)
    print(sum(num_paths))