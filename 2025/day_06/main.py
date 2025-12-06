import math
import re

def get_values(lines, idx):
    temp = []
    for j in range(len(lines)-1):
        temp.append(int(lines[j][idx].strip()))
    return temp

def get_values_2(lines, idx, num_digits):
    temp = []
    output = []
    for j in range(len(lines)-1):
        temp.append(lines[j][idx])

    i = num_digits-1
    while i >= 0:
        mini_total = ''
        for val in temp:
            if len(val) == 4:
                val = val[:3]
            str_val = val.replace(' ', '0')
            if str_val[i] != '0':
                mini_total = "".join([mini_total, str_val[i]])
        i -= 1
        if mini_total != '':
            output.append(int(mini_total))
    return output

if __name__ == "__main__":
    lines = []


    with open("input", "r") as f:
        for line in f.readlines():
            stripped = line.strip()
            # split = re.findall('.{1,4}', line)
            lines.append(line)

    # operator in last line indicates the start of each column
    operator_idx = len(lines) - 1
    lens = []
    count = 0
    for char in lines[operator_idx]:
        if char == '*' or char == '+':
            lens.append(count)
            count = 0
        count +=1
    # drop first 0
    del lens[0]

    parsed_lines = []
    for line in lines:
        temp_line = []
        for _len in lens:
            temp_line.append(line[:_len])
            line = line[_len:]
        temp_line.append(line)
        parsed_lines.append(temp_line)

    for i in range(len(parsed_lines)):
        assert len(parsed_lines[i]) == len(parsed_lines[0])

    total = 0
    total_2 = 0

    for i in range(len(parsed_lines[0])):
        match parsed_lines[operator_idx][i].strip():
            case '+':
                total += sum(get_values(parsed_lines, i))
                total_2 += sum(get_values_2(parsed_lines, i, len(parsed_lines[operator_idx][i])-1))
            case '*':
                total += math.prod(get_values(parsed_lines, i))
                total_2 += math.prod(get_values_2(parsed_lines, i, len(parsed_lines[operator_idx][i])-1))

    print(total)
    print(total_2)