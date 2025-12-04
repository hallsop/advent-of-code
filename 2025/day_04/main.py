import shutil

def check_idx(idx_to_check, line):
    if idx_to_check < 0:
        return False
    try:
        match line[idx_to_check]:
            case "@":
                return True
            case ".":
                return False
            case "x":
                return False
    except IndexError:
        return False

def check_file(fname, part_2):
    count = 0
    all_data = []
    with open(fname, "r") as f:
        for line in f:
            all_data.append(list(line.strip()))
    for i, line in enumerate(all_data):
        for j, char in enumerate(line):
            if char == "@":
                left = check_idx(j-1, all_data[i])
                left_up = check_idx(j-1, all_data[i-1]) if i > 0 else False
                up = check_idx(j, all_data[i-1]) if i > 0 else False
                right_up = check_idx(j+1, all_data[i-1]) if i > 0 else False
                right = check_idx(j+1, all_data[i])
                down_right = check_idx(j+1, all_data[i+1]) if i < len(all_data)-1 else False
                down = check_idx(j, all_data[i+1]) if i < len(all_data)-1 else False
                down_left = check_idx(j-1, all_data[i+1]) if i < len(all_data)-1 else False

                if sum((left, left_up, up, right_up, right, down_right, down, down_left)) < 4:
                    if part_2:
                        all_data[i][j] = "x"
                    count += 1
    if part_2:
        with open(fname, "w") as f:
            for line in all_data:
                f.write("".join(line) + "\n")
    return count

if __name__ == "__main__":
    counts = []
    i = 0
    count = check_file("input", False)
    print(count)
    shutil.copyfile('input', 'output')
    while True:
        count = check_file("output", True)
        counts.append(count)
        if count == 0:
            break
        i += 1
    print(counts)
    print(sum(counts))
