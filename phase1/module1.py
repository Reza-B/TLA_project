from phase0.FA_class import DFA, State
from visualization import visualizer
from utils import utils
from utils.utils import imageType


def solve(image: imageType) -> 'DFA':
    ...


if __name__ == "__main__":
    image = [[1, 1, 1, 1],
             [1, 0, 1, 0],
             [0, 1, 0, 1],
             [1, 1, 1, 1]]

    utils.save_image(image)
    fa = solve(image)
    print(fa.serialize_json())
