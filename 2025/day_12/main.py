import numpy as np
from functools import cache, wraps
from itertools import combinations, product, combinations_with_replacement
from enum import Enum, auto
import time

class HashWrapper:
    def __init__(self, x: np.ndarray) -> None:
        self.values = x
        self.h = hash(x.tobytes())

    def __hash__(self) -> int:
        return hash(self.h)

    def __eq__(self, __value: object) -> bool:
        return __value.h == self.h


def memoizer(expensive_function):
    @cache
    def cached_wrapper(*args, **kwargs):
        unwrapped_args = tuple(
            arg.values if isinstance(arg, HashWrapper) else arg
            for arg in args
        )

        unwrapped_kwargs = {
            k: (v.values if isinstance(v, HashWrapper) else v)
            for k, v in kwargs.items()
        }

        return expensive_function(*unwrapped_args, **unwrapped_kwargs)

    @wraps(expensive_function)
    def wrapper(*args, **kwargs):
        new_args = tuple(
            HashWrapper(arg) if isinstance(arg, np.ndarray) else arg
            for arg in args
        )

        new_kwargs = {
            k: (HashWrapper(v) if isinstance(v, np.ndarray) else v)
            for k, v in kwargs.items()
        }

        return cached_wrapper(*new_args, **new_kwargs)

    return wrapper

class Transforms(Enum):
    NOTHING = auto()
    ROTATE_90 = auto()
    ROTATE_180 = auto()
    ROTATE_270 = auto()
    FLIP_HOR = auto()
    FLIP_VER = auto()
    ROT_90_FLIP_HOR = auto()
    ROT_90_FLIP_VER = auto()
    ROTATE_180_FLIP_HOR = auto()
    ROTATE_180_FLIP_VER = auto()
    ROTATE_270_FLIP_HOR = auto()
    ROTATE_270_FLIP_VER = auto()

def _do_transform(shape: np.ndarray, transform: Transforms):
    match transform:
        case Transforms.NOTHING:
            return shape
        case Transforms.ROTATE_90:
            return np.rot90(shape)
        case Transforms.ROTATE_180:
            return np.rot90(shape, k=2)
        case Transforms.ROTATE_270:
            return np.rot90(shape, k=3)
        case Transforms.FLIP_HOR:
            return np.fliplr(shape)
        case Transforms.FLIP_VER:
            return np.flipud(shape)
        case Transforms.ROT_90_FLIP_HOR:
            return do_transform(do_transform(shape, Transforms.ROTATE_90), Transforms.FLIP_HOR)
        case Transforms.ROT_90_FLIP_VER:
            return do_transform(do_transform(shape, Transforms.ROTATE_90), Transforms.FLIP_VER)
        case Transforms.ROTATE_180_FLIP_HOR:
            return do_transform(do_transform(shape, Transforms.ROTATE_180), Transforms.FLIP_HOR)
        case Transforms.ROTATE_180_FLIP_VER:
            return do_transform(do_transform(shape, Transforms.ROTATE_180), Transforms.FLIP_VER)
        case Transforms.ROTATE_270_FLIP_HOR:
            return do_transform(do_transform(shape, Transforms.ROTATE_270), Transforms.FLIP_HOR)
        case Transforms.ROTATE_270_FLIP_VER:
            return do_transform(do_transform(shape, Transforms.ROTATE_270), Transforms.FLIP_VER)

do_transform = memoizer(_do_transform)

def _check_shape_intersect(shape1, shape2):
    try:
        cannot_place = np.logical_and(
            shape1, shape2
        )
        if cannot_place.any():
            return False
        else:
            return True
    except ValueError:
        return False

check_shape_intersect = memoizer(_check_shape_intersect)

def _try_place(region_arr, shape, idx):
    stack = [idx]
    while stack:
        (row, col) = stack.pop()
        try:
            if row + 3 > region_arr.shape[0] or col + 3 > region_arr.shape[1]:
                continue
            can_place = check_shape_intersect(
                region_arr[row:row + 3, col:col + 3], shape
            )
            if not can_place:
                # Try next column, then next row
                stack.append((row, col + 1))
                stack.append((row + 1, col))
            else:
                return row, col
        except ValueError:
            continue
    return False

try_place = memoizer(_try_place)

def determine_if_fit(region, shapes):
    shapes_to_check = []
    shape_areas = []
    for shape_id, num in enumerate(region[1]):
        for _ in range(num):
            shapes_to_check.append(shapes[shape_id])
            shape_areas.append(shapes[shape_id].sum())
    if sum(shape_areas) > region[0][0] * region[0][1]:
        return False
    elif len(shapes_to_check) *9 <= region[0][0] * region[0][1]:
        return True
    # all the work i did below, and it never even gets called smh
    for combo in combinations_with_replacement(list(Transforms), len(shapes_to_check)):
        current_shapes = [do_transform(shape, transform) for transform, shape in zip(combo, shapes_to_check)]
        for shape_combo in combinations(current_shapes, len(shapes_to_check)):
            shape_combo = list(shape_combo)
            for region_or, orientation in product([region[0]], [0, 1]):
                if orientation == 1:
                    if region_or ==  region_or[::-1]:
                        break
                    region_or = region_or[::-1]
                region_arr = np.zeros(region_or, dtype=np.bool)
                region_arr[0:3, 0:3] = shape_combo.pop()
                for _idx, shape in enumerate(shape_combo):
                    idx = (0, 0)
                    idx = try_place(region_arr, shape, idx)
                    if idx:
                        region_arr[idx[0]:idx[0] + 3, idx[1]:idx[1] + 3] = np.logical_or(
                            region_arr[idx[0]:idx[0] + 3, idx[1]:idx[1] + 3], shape
                        )
                    else:
                        break
                else:
                    return True
    return False



if __name__ == '__main__':
    start = time.time()
    with open('input', 'r') as f:
        i = 0
        is_shapes = True
        shapes = {}
        regions = []
        for line in f.readlines():
            if i == 30:
                is_shapes = False
            if is_shapes:
                if i % 5 == 0:
                    key = int(line.split(':')[0])
                else:
                    if key not in shapes:
                        shapes[key] = np.zeros((3,3), np.bool)
                    if line != '\n':
                        shapes[key][i%5-1, :] = [char == '#' for char in line.strip()]
            if not is_shapes:
                size = tuple(int(char) for char in line.split(':')[0].split('x'))
                regions.append((size, [int(char) for char in line.strip().split(' ')[1:]]))
            i += 1
    count = 0
    for region in regions:
        if determine_if_fit(region, shapes):
            count += 1
    print(count)

    elapsed_time = time.time() - start
    base_str = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
    timestr = f"{base_str}.{int((elapsed_time % 1) * 1000):03d}"
    print(f'Took {timestr}')