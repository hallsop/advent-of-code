
def check_val(val):
    str_val = str(val)
    if len(str_val) % 2 == 0:
        mid = int(len(str_val) / 2)
        if str_val[0:mid] == str_val[mid:]:
            return val
    return 0

def check_val_2(val):
    str_val = str(val)
    for denominator in range(2, len(str_val)+1):
        if len(str_val) % denominator == 0:
            seg_len = int(len(str_val) / denominator)
            vals_to_compare = []
            for i in range(0, denominator):
                vals_to_compare.append(str_val[(i*seg_len):(i+1)*seg_len])
            if len(set(vals_to_compare)) == 1:
                print(val)
                return val
    return 0


if __name__ == "__main__":
    sum_total = 0
    sum_total_2 = 0
    final_it = False
    with open('input', newline='') as f:
        while not final_it:
            lower = ''
            char = ''
            final_it = False
            while char != '-':
                char = f.read(1)
                lower += char if char != '-' else ''
            higher = ''
            while char != ',' and char != '':
                char = f.read(1)
                higher += char if char != ',' else ''
            if char == '':
                final_it = True
            lower = int(lower)
            higher = int(higher)
            for val in range(lower, higher + 1):
                sum_total += check_val(val)
                sum_total_2 += check_val_2(val)



    print(sum_total)
    print(sum_total_2)

