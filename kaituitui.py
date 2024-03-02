import os
import turtle
import argparse
from tqdm import tqdm
from PIL import Image

# Attempt to import PIL; set a flag to indicate its availability
try:
    from PIL import Image

    pil_available = True
except ImportError:
    pil_available = False

gif_dir = "gif/"

colour_dict = dict(
    b="blue",
    y="yellow",
    o="orange",
    k="black",
    w="white",
    G="#006400",  # Dark green
    p="#FD4659",  # Watermelon pink
    r="red",
    g="#8FBC8F",  # Light green
)


def split_string_in_pairs(s):
    """
    Splits a string into pairs of characters. Used to interpret the design files.

    :param s: String to be split.
    :return: List of character pairs.
    """
    # Initialize an empty list to store the substrings
    substrings = []

    # Iterate over the string with step size of 2
    for i in range(0, len(s) - 1, 2):
        # Append the substring of length 2 to the list
        substrings.append(s[i : i + 2])

    return substrings


def draw_square(t, fill, pixel_size, screen, frame_writer=None):
    """
    Draws a colored square using turtle graphics and optionally saves each movement as a frame.

    :param t: Turtle object for drawing.
    :param fill: Color to fill the square.
    :param pixel_size: Size of the square side.
    :param frame_writer: GifFrameWriter instance for saving frames, or None to skip saving.
    """
    t.fillcolor(fill)
    t.begin_fill()

    for _ in range(4):
        t.forward(pixel_size)
        t.left(90)
        if frame_writer:
            frame_writer.save_frame(screen)

    t.end_fill()
    if frame_writer:
        frame_writer.save_frame(screen)


def load_design(path):
    """
    Loads a design from a text file, creating a matrix representation.

    :param path: Path to the design file.
    :return: Design matrix where each element represents a color in a pixel.
    """
    design = []
    with open(path, "r") as f:
        for line in f.readlines():
            row = []
            for substring in split_string_in_pairs(line):
                colour, count = substring
                row += [colour] * int(count)
            design.append(row)
    return design


class GifFrameWriter:
    def __init__(self, base_filename, directory="gif/"):
        self.base_filename = base_filename
        self.directory = directory
        self.frame_count = 0
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def save_frame(self, turtle_canvas):
        """
        Saves the current state of the turtle canvas as a frame.

        :param turtle_canvas: The turtle canvas to capture.
        """
        canvas = turtle_canvas.getcanvas()
        filename = (
            f"{self.directory}/{self.base_filename}_frame_{self.frame_count:04}.eps"
        )
        canvas.postscript(file=filename)
        self.frame_count += 1

    def create_gif(self, duration=50, loop=0):
        """
        Converts all saved frames into a single GIF file.

        :param duration: Duration between frames in milliseconds.
        :param loop: Number of loops for the GIF; 0 means infinite.
        """
        gif_filenames = []
        for i in tqdm(range(self.frame_count)):
            eps_path = f"{self.directory}/{self.base_filename}_frame_{i:04}.eps"
            with Image.open(eps_path) as frame:
                frame = frame.convert("RGBA")
                gif_filename = f"{self.directory}/{self.base_filename}_frame_{i:04}.gif"
                frame.save(gif_filename, "gif")
                gif_filenames.append(gif_filename)

        # Later, when compiling the GIF, open each frame only long enough to load it into memory:
        with Image.open(gif_filenames[0]) as first_frame:
            first_frame = first_frame.convert("RGBA")
            first_frame.save(
                f"{self.directory}/{self.base_filename}.gif",
                save_all=True,
                append_images=[Image.open(filename).convert("RGBA") for filename in gif_filenames[1:]],
                optimize=False,
                duration=duration,
                loop=loop
            )

        # Cleanup temporary files
        for filename in gif_filenames:
            os.remove(filename)


# Modified main function
def main():
    parser = argparse.ArgumentParser(
        description="Draw a specified design with turtle graphics."
    )
    parser.add_argument(
        "--width", type=int, default=800, help="Width of the turtle screen."
    )
    parser.add_argument(
        "--repeats", type=int, default=2, help="Number of horizontal repeats"
    )
    parser.add_argument(
        "--speed", choices=["fast", "slow"], default="fast", help="Speed of the turtle."
    )
    parser.add_argument(
        "--design",
        type=str,
        choices=["duck", "heart", "watermelon"],
        default="duck",
        help="Design name to draw.",
    )
    parser.add_argument(
        "--savegif",
        action="store_true",
        help="Save the drawing process as a GIF animation.",
    )

    args = parser.parse_args()

    if args.savegif:
        output = f"{args.design}-{args.speed}-x{args.repeats}"
    elif not pil_available:
        print(
            "PIL (Pillow) is not available. The animation will not be saved as a GIF."
        )
        args.savegif = False  # Disable GIF saving if PIL is not available

    # Read the design file
    path = f"designs/{args.design}.txt"
    design = load_design(path) * args.repeats

    # Calculate the width and height of the design
    design_width, design_height = len(design), max(len(d) for d in design)

    # Calculate the pixel size
    # This is chosen so that there is 1 pixel width on either side of the design
    pixel_size = args.width / (design_width + 2)

    # Calculate the size of the image
    image_width = design_width * pixel_size
    image_height = design_height * pixel_size

    screen_height = pixel_size * (design_height + 2)

    # Set up the screen instance
    screen = turtle.Screen()
    screen.setup(width=args.width, height=screen_height)
    screen.title(f"Turtle Drawing - {args.design.capitalize()}")

    # Make the turtle
    t = turtle.Turtle(shape="turtle")
    t.speed(0)

    # Calculate the width and height of the screen
    start_x = -args.width // 2 + pixel_size
    start_y = -image_height // 2

    # Start the turtle in the right place
    t.penup()
    t.goto(start_x, start_y)
    t.pendown()

    # Initialize the GifFrameWriter at the beginning of your drawing process
    frame_writer = GifFrameWriter(output) if args.savegif else None

    # Run the drawing process
    for row in design:
        for pixel in row:
            draw_square(t, colour_dict[pixel], pixel_size, screen, frame_writer)
            t.left(90)
            t.forward(pixel_size)
            t.right(90)

            # Save the frame using GifFrameWriter
            if frame_writer:
                frame_writer.save_frame(t.getscreen())

        t.right(90)
        t.forward(pixel_size * len(row))
        t.left(90)
        t.forward(pixel_size)

    

    # After completing the drawing process, create the GIF
    if frame_writer:
        frame_writer.create_gif(duration=30 if args.speed == "fast" else 100)


if __name__ == "__main__":
    main()
