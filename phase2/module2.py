from phase0.FA_class import DFA
from utils import utils
from utils.utils import imageType

def solve(json_str: str, image: imageType) -> bool:
    fa = DFA.deserialize_json(json_str)
    black_pixel_addresses = get_black_pixel_addresses(image)
    accepted_count = 0

    for address in black_pixel_addresses:
        if is_accepted_by_dfa(fa, address):
            accepted_count += 1

    acceptance_ratio = accepted_count / len(black_pixel_addresses) if black_pixel_addresses else 0
    print(f"Acceptance Ratio: {acceptance_ratio * 100:.2f}%")
    return acceptance_ratio == 1

def get_black_pixel_addresses(image: imageType) -> list[str]:
    addresses = []
    for i in range(len(image)):
        for j in range(len(image[i])):
            if image[i][j] == 1:
                addresses.append(get_bit_address(i, j, len(image)))
    return addresses

def get_bit_address(row: int, col: int, size: int) -> str:
    address = []
    while size > 1:
        half = size // 2
        if row < half:
            if col < half:
                address.append('0')
            else:
                address.append('1')
                col -= half
        else:
            if col < half:
                address.append('2')
            else:
                address.append('3')
                col -= half
            row -= half
        size = half
    return ''.join(address)

def is_accepted_by_dfa(fa: DFA, address: str) -> bool:
    current_state = fa.init_state
    for symbol in address:
        if symbol in current_state.transitions:
            current_state = current_state.transitions[symbol]
        else:
            return False
    return fa.is_final(current_state)

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
