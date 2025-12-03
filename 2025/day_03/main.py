
def process_line(line, joltage_len=12):
    val_list = []
    idx = -1
    for digit in range(joltage_len, 0, -1):
        val = max(line[:-digit+1]) if digit > 1 else max(line)
        idx = line[:-digit+1].index(val) if digit > 1 else idx + line.index(val)
        line = line[idx+1:]
        val_list.append(str(val))
    assert len(val_list) == joltage_len
    return int("".join(val_list))

if __name__ == "__main__":
    with open("input", "r") as f:
        current_line = []
        sum_total = 0
        sum_total_2 = 0
        for char in f.read():
            match char:
                case '\n':
                    line_val = process_line(current_line, 2)
                    line_val_2 = process_line(current_line, 12)
                    sum_total += line_val
                    sum_total_2 += line_val_2
                    current_line = []
                case _:
                    current_line.append(int(char))

    print(sum_total)
    print(sum_total_2)