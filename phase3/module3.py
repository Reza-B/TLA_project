from utils.utils import imageType
from phase0.FA_class import DFA
from phase2 import module2


def solve(json_fa_list: list[str], images: list[imageType]) -> list[int]:
    accepted_indices = []

    for index, (json_fa, image) in enumerate(zip(json_fa_list, images)):
        if module2.solve(json_fa, image):
            accepted_indices.append(index)

    return accepted_indices


if __name__ == "__main__":
    json_fa_list = [
        '{"states": ["q_0", "q_1", "q_2", "q_3", "q_4"], "initial_state": "q_0", "final_states": ["q_3"], '
        '"alphabet": ["0", "1", "2", "3"], "q_0": {"0": "q_1", "1": "q_1", "2": "q_2", "3": "q_2"}, "q_1": {"0": '
        '"q_3", "1": "q_3", "2": "q_3", "3": "q_4"}, "q_2": {"0": "q_4", "1": "q_3", "2": "q_3", "3": "q_3"}, '
        '"q_3": {"0": "q_3", "1": "q_3", "2": "q_3", "3": "q_3"}, "q_4": {"0": "q_4", "1": "q_4", "2": "q_4", '
        '"3": "q_4"}}',
        # Add more JSON DFA strings as needed
    ]

    images = [
        [[1, 1, 1, 1],
         [1, 0, 1, 0],
         [0, 1, 0, 1],
         [1, 1, 1, 1]],
        # Add more images as needed
    ]

    accepted_indices = solve(json_fa_list, images)
    print(accepted_indices)
