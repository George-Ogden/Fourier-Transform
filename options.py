from argparse import ArgumentParser
from manim import config

config.disable_caching = True
config.verbosity = "ERROR"
config.frame_rate = 30


def parse_args() -> dict[dict, ...]:
    parser = ArgumentParser(
        description="Transform an image or a polygon into a series of rotating circles")

    # arguments for inputs
    input_options = parser.add_subparsers(
        title="Input Options", description="Select different input formats", dest="format")
    vector = input_options.add_parser(
        "vector", help="transform an SVG file", description="vector")
    vector.add_argument("-v", "--vector", help="SVG file")
    image = input_options.add_parser(
        "image", help="transform an image file", description="image")
    image.add_argument("-i", "--image", help="image file")
    sides = input_options.add_parser(
        "polygon", help="transform a polygon", description="polygon")
    sides.add_argument("-s", "--sides", type=int, help="number of sides")
    text = input_options.add_parser(
        "text", help="transform text", description="text")
    text.add_argument("-t", "--text", help="text")
    text.add_argument("--font", default="example/fonts/georgia/ttf",
                      help="specify text font (default : examples/fonts/georgia.ttf")

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
        args_dict[group.title] = {}
        for arg in group._group_actions:
            if hasattr(args, arg.dest):
                args_dict[group.title][arg.dest] = getattr(args, arg.dest)
                delattr(args, arg.dest)
    # add remaining items into input options
    args_dict["Input Options"] |= vars(args)
    return args_dict
