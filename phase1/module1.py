from visualization import visualizer
from utils import utils
from utils.utils import imageType
from phase0.FA_class import DFA, State

def solve(image: imageType) -> 'DFA':
    # Initialization
    i = j = 0
    u = {0: image}
    dfa = DFA()
    initial_state = dfa.add_state(0)
    dfa.assign_initial_state(initial_state)
    state_dict = {0: initial_state}

    while i <= j:
        for k in range(4):
            new_prefix = get_zoomed_part(u[i], k)
            if new_prefix in u.values():
                q = list(u.keys())[list(u.values()).index(new_prefix)]
            else:
                j += 1
                u[j] = new_prefix
                q = j

            if str(k) not in state_dict[i].transitions:
                new_state = state_dict.get(q, dfa.add_state(q))
                state_dict[i].add_transition(str(k), new_state)
                state_dict[q] = new_state

        i += 1

    for state_id, image_part in u.items():
        if is_final(image_part):
            dfa.add_final_state(state_dict[state_id])

    return dfa


def get_zoomed_part(image, part):
    size = len(image) // 2
    if part == 0:
        return [row[:size] for row in image[:size]]
    elif part == 1:
        return [row[size:] for row in image[:size]]
    elif part == 2:
        return [row[:size] for row in image[size:]]
    elif part == 3:
        return [row[size:] for row in image[size:]]


def is_final(image_part):
    return all(pixel == 1 for row in image_part for pixel in row)

if __name__ == "__main__":
    image = [[1, 1, 1, 1],
             [1, 0, 1, 0],
             [0, 1, 0, 1],
             [1, 1, 1, 1]]

    utils.save_image(image)
    fa = solve(image)
    print(fa.serialize_json())

