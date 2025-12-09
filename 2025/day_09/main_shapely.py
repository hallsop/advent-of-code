from tqdm import tqdm
import shapely

def calc_area(coord1, coord2):
    return (abs(coord1[0] - coord2[0])+1) * (abs(coord1[1] - coord2[1])+1)

def max_idx(_list):
    return max(range(len(_list)), key=_list.__getitem__)

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

    poly = shapely.Polygon(coords)
    with tqdm(total=len(areas[0])*len(areas)) as pbar:
        while True:
            max_i = max_idx([max(area) for area in areas])
            max_j = max_idx(areas[max_i])
            if areas[max_i][max_j] == -1:
                raise Exception
            x_1, y_1 = coords[max_i][0], coords[max_i][1]
            x_2, y_2 = coords[max_j][0], coords[max_j][1]
            rect = shapely.Polygon(((x_1, y_1), (x_2, y_1), (x_2, y_2), (x_1, y_2), (x_1, y_1)))
            if rect.within(poly):
                break

            areas[max_i][max_j] = -1
            pbar.update(1)
    print(areas[max_i][max_j])