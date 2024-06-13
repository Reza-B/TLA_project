from phase0.FA_class import DFA
from utils import utils
from utils.utils import imageType


# def solve(json_str: str, image: imageType) -> bool:
#     fa = DFA.deserialize_json(json_str)
#     ...


def solve(json_str: str, image: imageType) -> bool:
    fa = DFA.deserialize_json(json_str)
    accepted_count = 0
    total_count = 0

    size = len(image)
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
            if image[i][j] == 0:  # Check for black pixels (assuming 0 is black)
                total_count += 1
                bit_address = get_bit_address(i, j, size)
                state = fa.init_state
                for char in bit_address:
                    state = state.transitions.get(char)
                    if state is None:
                        break

                if state and fa.is_final(state):
                    accepted_count += 1

    if total_count == 0:
        return False

    acceptance_ratio = accepted_count / total_count
    return acceptance_ratio == 1.0

if __name__ == "__main__":
    print(
        solve(
            '{"states": ["q_0", "q_1", "q_2", "q_3", "q_4"], "initial_state": "q_0", "final_states": ["q_3"], '
            '"alphabet": ["0", "1", "2", "3"], "q_0": {"0": "q_1", "1": "q_1", "2": "q_2", "3": "q_2"}, "q_1": {"0": '
            '"q_3", "1": "q_3", "2": "q_3", "3": "q_4"}, "q_2": {"0": "q_4", "1": "q_3", "2": "q_3", "3": "q_3"}, '
            '"q_3": {"0": "q_3", "1": "q_3", "2": "q_3", "3": "q_3"}, "q_4": {"0": "q_4", "1": "q_4", "2": "q_4", '
            '"3": "q_4"}}',
            [[1, 1, 1, 1],
             [1, 0, 1, 0],
             [0, 1, 0, 1],
             [1, 1, 1, 1]]
        )
    )
