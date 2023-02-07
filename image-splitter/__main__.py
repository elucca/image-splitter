from PIL import Image
from PIL.ImageChops import invert
from PIL import UnidentifiedImageError
import argparse
import os

parser = argparse.ArgumentParser(
    description="Current features: Split images in given folders into constituent channels. Invert image green channels."
)
parser.add_argument(
    "--mode",
    help="Use 's' for split and 'g' for inverting green channels.",
    required=True,
)
parser.add_argument(
    "--input_paths",
    nargs="+",
    help="Absolute paths to folders containing images. Not recursive, so input subfolders separately.",
    required=True,
)
parser.add_argument(
    "--output_paths",
    nargs="+",
    help="Absolute paths to output folders. Must have one for each input path.",
    required=True,
)

args = parser.parse_args()

if args.mode != "s" and args.mode != "g":
    raise argparse.ArgumentError(None, 'Error: Mode must be "s" or "g".')


def split_image(image, output_path):
    channels = []

    channels.append(("R", image.getchannel("R")))
    channels.append(("G", image.getchannel("G")))
    channels.append(("B", image.getchannel("B")))
    if image.mode == "RGBA":
        channels.append(("A", image.getchannel("A")))

    orig_name = os.path.splitext(os.path.split(image.filename)[1])[0]

    for channel in channels:
        name = orig_name + "_" + channel[0] + ".png"
        save_path = os.path.join(output_path, name)
        channel[1].save(save_path, "png")


def invert_green(image, output_path):
    orig_name = os.path.splitext(os.path.split(image.filename)[1])[0]

    if image.mode == "RGB":
        r, g, b = image.split()
        inv_g_image = Image.merge("RGB", (r, invert(g), b))

        name = orig_name + "_invg.png"
        save_path = os.path.join(output_path, name)
        inv_g_image.save(save_path, "png")

    if image.mode == "RGBA":
        r, g, b, a = image.split()
        inv_g_image = Image.merge("RGBA", (r, invert(g), b, a))

        name = orig_name + "_invg.png"
        save_path = os.path.join(output_path, name)
        inv_g_image.save(save_path, "png")


def full_paths(folder):
    return [os.path.join(folder, file) for file in os.listdir(folder)]


if len(args.input_paths) != len(args.output_paths):
    print("Error: Unequal number of input and output paths.")
    quit()

for i, folder in enumerate(args.input_paths):
    for file in full_paths(folder):
        file_path = os.path.abspath(file)
        if os.path.isdir(file_path):
            continue

        try:
            image = Image.open(file_path)
            if args.mode == "s":
                split_image(image, args.output_paths[i])
            if args.mode == "g":
                invert_green(image, args.output_paths[i])
        except UnidentifiedImageError:
            print("Passing over unrecognized file...")
