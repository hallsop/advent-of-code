
def concat_ranges(ranges):
    concatted_ranges = []
    ranges_to_remove = []
    for fresh_range in ranges:
        temp_ranges = ranges.copy()
        temp_ranges.remove(fresh_range)
        for _other_fresh_range in reversed(temp_ranges):
            if (fresh_range[-1] in range(*_other_fresh_range) or fresh_range[1] == _other_fresh_range[1]) and fresh_range not in ranges_to_remove:
                concatted_ranges.append([fresh_range[0], _other_fresh_range[-1]])
                ranges_to_remove.append(_other_fresh_range)
                break
        else:
            if fresh_range not in ranges_to_remove:
                concatted_ranges.append(fresh_range)
    return concatted_ranges


if __name__ == "__main__":
    with open("input", "r") as f:
        ranges = []
        ids = []
        is_range = True
        for line in f.readlines():
            if line == "\n":
                is_range = False
            elif is_range:
                _range = [int(fresh_range.strip()) for fresh_range in line.split("-")]
                _range[1] +=1  # make inclusive
                ranges.append(_range)
            else:
                ids.append(int(line))
        ranges.sort()
        ids.sort()

        unique_fresh_ranges = ranges

        last_ranges = None
        while True:
            unique_fresh_ranges.sort()
            unique_fresh_ranges = concat_ranges(unique_fresh_ranges)
            if last_ranges == unique_fresh_ranges:
                break
            else:
                last_ranges = unique_fresh_ranges

        ranges = [range(a, b) for a, b in unique_fresh_ranges]
        count = 0
        for _id in ids:
            for fresh_range in ranges:
                if _id in fresh_range:
                    count += 1
                    break
        print(count)


        num_available_fresh_ids = 0

        for fresh_range in unique_fresh_ranges:
            num_available_fresh_ids += fresh_range[1] - fresh_range[0]

        print(num_available_fresh_ids)

