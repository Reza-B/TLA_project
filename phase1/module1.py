from visualization import visualizer
from utils import utils
from utils.utils import imageType
from phase0.FA_class import DFA, State

# def solve(image: imageType) -> 'DFA':
#     ...
def bit_addressing(image, x, y, size, prefix):
    if size == 1:
        return {prefix: image[x][y]}

    half = size // 2
    addresses = {}
    addresses.update(bit_addressing(image, x, y, half, prefix + '0'))
    addresses.update(bit_addressing(image, x, y + half, half, prefix + '1'))
    addresses.update(bit_addressing(image, x + half, y, half, prefix + '2'))
    addresses.update(bit_addressing(image, x + half, y + half, half, prefix + '3'))
    return addresses

def solve(image: imageType) -> 'DFA':
    size = len(image)
    addresses = bit_addressing(image, 0, 0, size, '')

    # Initialize variables
    i = j = 0
    states = {}
    u = {}

    # Create initial state and assign u_0
    dfa = DFA()
    initial_state = dfa.add_state(id=0)
    dfa.assign_initial_state(initial_state)
    states[0] = initial_state
    u[0] = ''

    while i <= j:
        current_state = states[i]
        current_prefix = u[i]
        for k in '0123':
            new_prefix = current_prefix + k
            found = False
            for q in u:
                if u[q] == new_prefix:
                    dfa.add_transition(current_state, states[q], k)
                    found = True
                    break
            if not found:
                j += 1
                new_state = dfa.add_state(id=j)
                states[j] = new_state
                u[j] = new_prefix
                dfa.add_transition(current_state, new_state, k)

        if i == j:
            break
        i += 1

    # Set final states based on addresses
    for prefix, value in addresses.items():
        for state_id, state_prefix in u.items():
            if state_prefix == prefix:
                if value == 1:
                    dfa.add_final_state(states[state_id])
                break

    return dfa


if __name__ == "__main__":
    image = [[1, 1, 1, 1],
             [1, 0, 1, 0],
             [0, 1, 0, 1],
             [1, 1, 1, 1]]

    utils.save_image(image)
    fa = solve(image)
    print(fa.serialize_json())

