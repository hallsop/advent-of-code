from typing import List
from itertools import combinations_with_replacement
import time
import numpy as np
from scipy.optimize import linprog

class Button:
    def __init__(self, values: List[int]) -> None:
        self.values = values

    def press(self, state):
        for val in self.values:
            state[val] = not state[val]

    def press_joltage(self, joltages):
        for val in self.values:
            joltages[val] += 1

class Machine:
    def __init__(self, line):
        split_line = line.split(' ')
        self.target: List[bool] = self.get_target(split_line[0])
        self.state: List[bool] = [False] * len(self.target)
        self.buttons: List[Button] = self.get_buttons(split_line[1:-1])
        self.joltage_reqs: List[int] = self.get_joltage_reqs(split_line[-1])
        self.current_joltage: List[int] = [0] * len(self.joltage_reqs)
        self.valid_sequences: List[List[int]] = []

    def run_seq(self, idxs_to_press: List[int]) -> bool:
        res = None
        assert len(idxs_to_press) > 0
        for idx in idxs_to_press:
            res = self.press_button(idx)
        self.reset()
        return res

    def lowest_presses(self) -> int:
        presses = 1
        valid_seq = False
        while not valid_seq:
            idxs = list(range(len(self.buttons)))
            for seq in combinations_with_replacement(idxs, presses):
                res = self.run_seq(seq)
                if res:
                    valid_seq = True
                    break
            else:
                presses += 1
        return presses

    def run_seq_joltage(self, idxs_to_press: List[int]) -> bool:
        res = None
        assert len(idxs_to_press) > 0
        for idx in idxs_to_press:
            res = self.press_joltage(idx)
        self.reset()
        return res

    def lowest_presses_joltage(self, message_prefix):
        c = np.ones(len(self.buttons))
        A_eq = np.zeros((len(self.joltage_reqs), len(self.buttons)))
        for idx, button in enumerate(self.buttons):
            for val in button.values:
                A_eq[val, idx] = 1
        b_eq = np.array(self.joltage_reqs)

        result = linprog(c=c, b_eq=b_eq, A_eq=A_eq, integrality=1)
        presses = np.round(result.fun).astype(np.uint64)
        idx_count = result.x
        seq = []
        for i, count in enumerate(np.round(idx_count).astype(np.uint8)):
            seq.extend([i]*count)
        res = self.run_seq_joltage(seq)
        if res:
            print(f'SUCCESS: {message_prefix} completed {presses} presses with success')
        else:
            raise Exception(f'{message_prefix} failed {presses} presses')
        return presses

    def press_button(self, idx: int) -> bool:
        self.buttons[idx].press(self.state)
        return self.state == self.target

    def press_joltage(self, idx: int) -> bool:
        self.buttons[idx].press_joltage(self.current_joltage)
        return self.current_joltage == self.joltage_reqs

    def reset(self):
        self.state = [False] * len(self.target)
        self.current_joltage = [0] * len(self.joltage_reqs)

    @staticmethod
    def get_target(targets: str) -> List[bool]:
        targets = targets.replace('[', '').replace(']', '')
        return [char == '#' for char in targets]

    @staticmethod
    def get_buttons(button_strs: str) -> List[Button]:
        buttons = []
        for button_str in button_strs:
            vals = button_str.replace('(', '').replace(')', '').split(',')
            buttons.append(Button([int(val) for val in vals]))
        return buttons

    @staticmethod
    def get_joltage_reqs(joltage_str: str) -> List[int]:
        joltage_str = joltage_str.replace('{', '').replace('}', '')
        return [int(joltage) for joltage in joltage_str.split(',')]


def lowest_presses_joltage(idx, machine_str, output):
    machine = Machine(machine_str)
    output.put(machine.lowest_presses_joltage(f'Machine {idx}'))

if __name__ == "__main__":
    start = time.time()
    machine_strs = []
    total_presses = 0
    total_presses_joltage = 0
    with open('input', 'r') as f:
        for line in f.readlines():
            machine_strs.append(line.strip())

    for idx, machine_str in enumerate(machine_strs):
        machine = Machine(machine_str)
        total_presses += machine.lowest_presses()
        total_presses_joltage += machine.lowest_presses_joltage(f'Machine {idx}')

    print(total_presses)
    print(total_presses_joltage)

    elapsed_time = time.time() - start
    base_str = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
    timestr = f"{base_str}.{int((elapsed_time % 1) * 1000):03d}"
    print(f'Took {timestr}')