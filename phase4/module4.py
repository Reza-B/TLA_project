from math import log2
from phase0.FA_class import DFA, State
from utils.utils import imageType


# def solve(json_str: str, resolution: int) -> imageType:
#     ...

def solve(json_str: str, resolution: int) -> imageType:
    fa = DFA.deserialize_json(json_str)
    size = resolution
    image = [[1 for _ in range(size)] for _ in range(size)]

    def get_bit_address(x, y, size):
        address = ""
        while size > 1:
            size //= 2
            if x < size and y < size:
                address += "0"
            elif x < size <= y:
                address += "1"
                y -= size
            elif y < size <= x:
                address += "2"
                x -= size
            else:
                address += "3"
                x -= size
                y -= size
        return address

    for i in range(size):
        for j in range(size):
            bit_address = get_bit_address(i, j, size)
            state = fa.init_state
            for char in bit_address:
                state = state.transitions.get(char)
                if state is None:
                    break
            if state and fa.is_final(state):
                image[i][j] = 0  # Black pixel if the bit address is accepted by the DFA

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
    print(pic_arr)
