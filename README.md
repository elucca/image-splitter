# image-splitter
or, random image utilities I've had a need for


Two features; Splits image RGBA channels into separate pngs, or inverts their green channel.

Makes the somewhat inconvenient assumption that the images are pngs.

## Usage
Run the program as a module with `python -m image-splitter -- mode <mode> --input_paths <paths separated by spaces> --output_paths <paths separated by spaces>` from the project root folder.

Mode is either s for splitting the image or g for inverting the green channel. Both will create new images rather than overwriting anything.

Multiple folder paths may be given. Input and output paths must match, e.g. images in the third input folder are decomposed into the third output folder.
