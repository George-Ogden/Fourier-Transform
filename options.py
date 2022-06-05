from argparse import ArgumentParser
from manim import config

config.disable_caching = True
config.verbosity = "ERROR"


def parse_args() -> dict[dict, ...]:
    parser = ArgumentParser()

    # arguments for different input formats
    format = parser.add_mutually_exclusive_group(required=True)
    format.add_argument("-i", "--input", "--input_file",
                        dest="filename", help="file to transform")
    format.add_argument("-s", "--sides", type=int, help="sides of polygon")

    # general arguments
    parser.add_argument("-o", "--output", "--output_file",
                        required=True, help="file to save to")
    parser.add_argument("-p", "--preview", action="store_true",
                        help="preview when complete")

    # arguments for animation
    anim_options = parser.add_argument_group("Animation Options")
    anim_options.add_argument(
        "-n", "--number", type=int, default=50, help="number of circles")
    anim_options.add_argument(
        "-r", "--rotations", type=int, default=2, help="number of complete rotations")
    anim_options.add_argument(
        "-d", "--duration", type=float, default=10, help="duration of each rotation")
    anim_options.add_argument("--fade", type=float,
                              default=0.005, help="fading rate")

    # parse args
    args = parser.parse_args()
    args_dict = {}
    for group in parser._action_groups:
        # split into groups based on title
        args_dict[group.title] = {arg.dest: getattr(
            args, arg.dest, None) for arg in group._group_actions}
    return args_dict
