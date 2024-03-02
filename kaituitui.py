import os
import turtle
import argparse
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


def draw_square(t, fill, pixel_size):
    """
    Draws a colored square using turtle graphics.

    :param t: Turtle object for drawing.
    :param fill: Color to fill the square.
    :param pixel_size: Size of the square side.
    """
    # Set the fill color
    t.fillcolor(fill)

    t.begin_fill()

    # Draw a square
    for _ in range(4):
        t.forward(pixel_size)  # Move the turtle forward by pixel_size units
        t.left(90)  # Turn the turtle right by 90 degrees

    # End filling the color
    t.end_fill()


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


def draw_design(t, d, pixel_size):
    """
    Draws the entire design from a matrix representation.

    :param d: Design matrix.
    :param pixel_size: Size of each pixel square.
    """
    for row in d:
        for pixel in row:
            draw_square(t, colour_dict[pixel], pixel_size)

            # Move to the next location
            t.left(90)
            t.forward(pixel_size)
            t.right(90)

        # Move to the next location
        t.right(90)
        t.forward(pixel_size * len(row))
        t.left(90)
        t.forward(pixel_size)


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
    global screen
    screen = turtle.Screen()
    screen.setup(width=args.width, height=screen_height)
    screen.title(f"Turtle Drawing - {args.design.capitalize()}")

    # Make the turtle
    t = turtle.Turtle(shape="turtle")
    t.speed(0 if args.speed == "fast" else 10)

    # Calculate the width and height of the screen
    start_x = -args.width // 2 + pixel_size
    start_y = -image_height // 2

    # Start the turtle in the right place
    t.penup()
    t.goto(start_x, start_y)
    t.pendown()

    # Run the drawing process
    global frame_count
    frame_count = 0
    for row in design:
        for pixel in row:
            draw_square(t, colour_dict[pixel], pixel_size)
            t.left(90)
            t.forward(pixel_size)
            t.right(90)

            # Save the frame if GIF saving is enabled
            if args.savegif:
                canvas = screen.getcanvas()
                canvas.postscript(file=f"{gif_dir}/{output}_frame_{frame_count:04}.eps")
                frame_count += 1

        t.right(90)
        t.forward(pixel_size * len(row))
        t.left(90)
        t.forward(pixel_size)

    # Convert all frames to GIF and combine them if GIF saving is enabled
    if args.savegif:
        frames = []
        for i in range(frame_count):
            frame = Image.open(f"{gif_dir}/{output}_frame_{i:04}.eps")
            frame = frame.convert("RGBA")
            frame.save(f"{gif_dir}/{output}_frame_{i:04}.gif", "gif")
            frames.append(Image.open(f"{gif_dir}/{output}_frame_{i:04}.gif"))

        frames[0].save(
            f"{gif_dir}/{output}.gif",
            save_all=True,
            append_images=frames[1:],
            optimize=False,
            duration=100,
            loop=0,
        )

        # Cleanup: remove temporary files
        for i in range(frame_count):
            os.remove(f"{gif_dir}/{output}_frame_{i:04}.eps")
            os.remove(f"{gif_dir}/{output}_frame_{i:04}.gif")


if __name__ == "__main__":
    main()
