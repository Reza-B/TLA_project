from math import log2
from phase0.FA_class import DFA, State
from utils.utils import imageType

def solve(json_str: str, resolution: int) -> imageType:
    fa = DFA.deserialize_json(json_str)
    image = [[0] * resolution for _ in range(resolution)]

    def fill_image(state: State, x: int, y: int, size: int):
        if size == 1:
            image[y][x] = 1 if fa.is_final(state) else 0
        else:
            half_size = size // 2
            for k in range(4):
                if str(k) in state.transitions:
                    next_state = state.transitions[str(k)]
                    if k == 0:
                        fill_image(next_state, x, y, half_size)
                    elif k == 1:
                        fill_image(next_state, x + half_size, y, half_size)
                    elif k == 2:
                        fill_image(next_state, x, y + half_size, half_size)
                    elif k == 3:
                        fill_image(next_state, x + half_size, y + half_size, half_size)

    fill_image(fa.init_state, 0, 0, resolution)
    return image


if __name__ == "__main__":
    pic_arr = solve(
        '{"states": ["q_0", "q_1", "q_2", "q_3", "q_4"], "initial_state": "q_0", "final_states": ["q_3"], '
        '"alphabet": ["0", "1", "2", "3"], "q_0": {"0": "q_1", "1": "q_1", "2": "q_2", "3": "q_2"}, "q_1": {"0": '
        '"q_3", "1": "q_3", "2": "q_3", "3": "q_4"}, "q_2": {"0": "q_4", "1": "q_3", "2": "q_3", "3": "q_3"}, '
        '"q_3": {"0": "q_3", "1": "q_3", "2": "q_3", "3": "q_3"}, "q_4": {"0": "q_4", "1": "q_4", "2": "q_4", '
        '"3": "q_4"}}',
        4
    )
    for row in pic_arr:
        print(row)
