

if __name__ == "__main__":
    pos = 50
    count = 0
    count_2 = 0
    with open("input", "r") as f:
        for line in f.readlines():
            last_pos = pos
            direction = line[0]
            value = int(line[1:])
            if direction == "R":
                value *= -1
            pos += value
            if pos % 100 == 0:
                count += 1

            diff = last_pos - pos
            sign = 1 if diff > 0 else -1
            for val in range(pos, last_pos, sign):
                if val % 100 == 0:
                    count_2 += 1
    print(count)
    print(count_2)
