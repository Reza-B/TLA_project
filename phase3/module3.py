# from utils.utils import imageType
# from phase0.FA_class import DFA
# from phase2 import module2
#
#
# def solve(json_fa_list: list[str], images: list[imageType]) -> list[int]:
#     ...
#
#
# if __name__ == "__main__":
#     ...


from utils.utils import imageType
from phase0.FA_class import DFA
from phase2 import module2


def solve(json_fa_list: list[str], images: list[imageType]) -> list[int]:
    results = []

    for image in images:
        max_acceptance = -1
        best_fa_index = -1

        for i, json_fa in enumerate(json_fa_list):
            fa = DFA.deserialize_json(json_fa)
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

            if total_count > 0:
                acceptance_ratio = accepted_count / total_count
            else:
                acceptance_ratio = 0

            if acceptance_ratio > max_acceptance:
                max_acceptance = acceptance_ratio
                best_fa_index = i

        results.append(best_fa_index)

    return results


if __name__ == "__main__":
    pass
