from argparse import ArgumentParser
from manim import config

config.disable_caching = True
config.verbosity = "ERROR"


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", "--input_file",
                        dest="filename", required=True, help="file to transform")
    parser.add_argument("-o", "--output", "--output_file",
                        required=True, help="file to save to")
    parser.add_argument(
        "-p", "--preview", action="store_true", help="preview when complete")

    image_options = parser.add_argument_group("Display Options")
    image_options.add_argument(
        "-n", "--number", type=int, default=50, help="number of circles")
    image_options.add_argument(
        "-r", "--rotations", type=int, default=2, help="number of complete rotations")
    image_options.add_argument(
        "-d", "--duration", type=float, default=10, help="duration of each rotation")
    image_options.add_argument(
        "--fade", type=float, default=0.005, help="fading rate")

    args = parser.parse_args()
    args_dict = {}
    for group in parser._action_groups:
        args_dict[group.title] = {arg.dest: getattr(
            args, arg.dest, None) for arg in group._group_actions}
    return args_dict
