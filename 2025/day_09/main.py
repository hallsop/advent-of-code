from tqdm import tqdm
import numpy as np

# I am aware this is horrible, I gave up trying to make it look nice

def calc_area(coord1, coord2):
    return (abs(coord1[0] - coord2[0])+1) * (abs(coord1[1] - coord2[1])+1)

def max_idx(_list):
    return max(range(len(_list)), key=_list.__getitem__)

def get_red(coord1, coord2):
    return list(range(min(coord1[0], coord2[0]), max(coord1[0], coord2[0]) + 1)), \
            list(range(min(coord1[1], coord2[1]), max(coord1[1], coord2[1]) + 1)),


if __name__ == "__main__":
    coords = []
    with open("input", "r") as f:
        for line in f.readlines():
            coords.append(list(map(int, line.split(","))))

    areas = []
    for i in range(len(coords)):
        areas.append([])
        for j in range(len(coords)):
            if i != j:
                areas[i].append(calc_area(coords[i], coords[j]))
            else:
                areas[i].append(-1)



    max_i = max_idx([max(area) for area in areas])
    max_j = max_idx(areas[max_i])
    print(areas[max_i][max_j])


    size_x = max([coord[0] for coord in coords])
    size_y = max([coord[1] for coord in coords])

    is_red = np.zeros((size_y+1, size_x+1)).astype(np.bool)
    for i in tqdm(range(len(coords))):
        try:
            x, y = get_red(coords[i], coords[i-1])
        except IndexError:
            x, y = get_red(coords[i], coords[-1])
        for j, _ in enumerate(x):
            for k, _ in enumerate(y):
                is_red[y[k], x[j]] += 1

    with tqdm(total=len(areas[0])*len(areas)) as pbar:
        i = 0
        while True:

            max_i = max_idx([max(area) for area in areas])
            max_j = max_idx(areas[max_i])

            x_1, y_1 = coords[max_i][0], coords[max_i][1]
            x_2, y_2 = coords[max_j][0], coords[max_j][1]

            if areas[max_i][max_j] == -1:
                raise Exception

            valid = False
            if is_red[y_1, x_1] and is_red[y_2, x_2]:
                y1_x2_green = [True, True]
                left = is_red[y_1, x_2:x_1]
                right = is_red[y_1, x_1+1:x_2+1]
                up = is_red[y_2+1:y_1+1, x_2]
                down = is_red[y_1:y_2, x_2]
                if len(left) > 0:
                    arr = left
                    sign = -1
                if len(right) > 0:
                    arr = right
                    sign = 1
                if all(arr) or all(arr)*-1:
                    y1_x2_green[0] = True
                else:
                    if sign == -1:
                        arr = arr[::-1]
                    last = False
                    inside = False
                    for val in arr:
                        if not inside and not val:
                            inside = True
                        if inside and last and not val:
                            y1_x2_green[0] = False
                            break
                        last = val
                    if y1_x2_green[0]:
                        end = is_red.shape[1]
                        rest = is_red[y_1, 0:x_2-1] if sign == 1 else is_red[y_1, x_2+1:end]
                        if rest.sum() == 0:
                            y1_x2_green[0] = False
                if len(up) > 0:
                    arr = up
                    sign = -1
                if len(down) > 0:
                    arr = down
                    sign = 1
                if all(arr) or all(arr)*-1:
                    y1_x2_green[1] = True
                else:
                    if sign == -1:
                        arr = arr[::-1]
                    last = False
                    inside = False
                    for val in arr:
                        if not inside and not val:
                            inside = True
                        if last and not val:
                            y1_x2_green[1] = False
                            break
                        last = val
                    if y1_x2_green[1]:
                        end = is_red.shape[0]
                        rest = is_red[0:y_1-1, x_2] if sign == 1 else is_red[y_1+1:end, x_2]
                        if rest.sum() == 0:
                            y1_x2_green[1] = False

                y2_x1_green = [True, True]
                left = is_red[y_2, x_2+1:x_1+1]
                right = is_red[y_2, x_1:x_2]
                up = is_red[y_2:y_1, x_1]
                down = is_red[y_1+1:y_2+1, x_1]
                if len(left) > 0:
                    arr = left
                    sign = -1
                if len(right) > 0:
                    arr = right
                    sign = 1
                if all(arr) or all(arr) * -1:
                    y2_x1_green[0] = True
                else:
                    if sign == -1:
                        arr = arr[::-1]
                    last = False
                    inside = False
                    for val in arr:
                        if not inside and not val:
                            inside = True
                        if last and not val:
                            y2_x1_green[0] = False
                            break
                        last = val
                    if y2_x1_green[0]:
                        end = is_red.shape[1]
                        rest = is_red[y_2, 0:x_1-1] if sign == 1 else is_red[y_2, x_1+1:end]
                        if rest.sum() == 0:
                            y2_x1_green[0] = False
                if len(up) > 0:
                    arr = up
                    sign = -1
                if len(down) > 0:
                    arr = down
                    sign = 1
                if all(arr) or all(arr) * -1:
                    y2_x1_green[1] = True
                else:
                    if sign == -1:
                        arr = arr[::-1]
                    last = False
                    inside = False
                    for val in arr:
                        if not inside and not val:
                            inside = True
                        if last and not val:
                            y2_x1_green[1] = False
                            break
                        last = val
                    if y2_x1_green[1]:
                        end = is_red.shape[0]
                        rest = is_red[0:y_2-1, x_1] if sign == 1 else is_red[y_2+1:end, x_1]
                        if rest.sum() == 0:
                            y2_x1_green[1] = False

                if all(y1_x2_green) and all(y2_x1_green):
                    break
            areas[max_i][max_j] =  -1
            pbar.update(1)
    print(areas[max_i][max_j])