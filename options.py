from argparse import ArgumentParser
from manim import config

config.disable_caching = True
config.verbosity = "ERROR"
config.frame_rate = 30


def parse_args() -> dict[dict, ...]:
    parser = ArgumentParser(
        description="Transform an image (.svg) or a polygon into a series of rotating circles")

    # arguments for inputs
    input_options = parser.add_argument_group("Input Options")
    format = input_options.add_mutually_exclusive_group(required=True)
    format.add_argument("-v", "--vector", help="transform an SVG file")
    format.add_argument("-i", "--image", help="transform an image file")
    format.add_argument("-s", "--sides", type=int,
                        help="create a polygon with s sides")

    # arguments for outputs
    output_options = parser.add_argument_group("Output Options")
    output_options.add_argument("-o", "--output", "--output_file",
                                default="output.mp4", help="output file (default: output.mp4)")
    output_options.add_argument("-p", "--preview", action="store_true",
                                help="preview when complete")

    # arguments for animation
    anim_options = parser.add_argument_group("Animation Options")
    anim_options.add_argument(
        "-n", "--number", type=int, default=50, help="number of circles (default: 50)")
    anim_options.add_argument("-r", "--rotations", type=int,
                              default=3, help="number of complete rotations (default: 3)")
    anim_options.add_argument("-d", "--duration", type=float, default=10,
                              help="number of seconds for each rotation (default: 10)")
    anim_options.add_argument("-f", "--fade", type=float, default=0.005,
                              help="rate of exponential decay of path - higher means faster decay (default: 0.005)")

    # parse args
    args = parser.parse_args()
    args_dict = {}
    for group in parser._action_groups:
        # split into groups based on title
        args_dict[group.title] = {arg.dest: getattr(
            args, arg.dest, None) for arg in group._group_actions}
    return args_dict
