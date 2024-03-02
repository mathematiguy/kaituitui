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
    Splits a given string into substrings of length 2.

    :param s: The string to be split into pairs.
    :return: A list of substrings, each of length 2.
    """

    # Initialize an empty list to store the substrings
    substrings = []

    # Iterate over the string with step size of 2
    for i in range(0, len(s) - 1, 2):
        # Append the substring of length 2 to the list
        substrings.append(s[i : i + 2])

    return substrings


def draw_square(t, fill):
    """
    Draws a filled square using the turtle graphics library.

    :param t: The turtle object used for drawing.
    :param fill: The color used to fill the square.
    """

    # Set the fill color
    t.fillcolor(fill)

    t.begin_fill()

    # Draw a square
    for _ in range(4):
        t.forward(100)  # Move the turtle forward by 100 units
        t.left(90)  # Turn the turtle right by 90 degrees

    # End filling the color
    t.end_fill()


def load_design(path):
    """
    Loads a design from a text file, where each character represents a color and a number that indicates the repetition.

    :param path: Path to the design file.
    :return: A list of lists representing the design, where each sublist corresponds to a row of the design.
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


def draw_design(t, d):
    """
    Draws a design based on the provided design matrix where each cell contains a color character.

    :param d: The design matrix with color codes.
    """

    for row in d:
        for pixel in row:
            draw_square(t, colour_dict[pixel])

            # Move to the next location
            t.left(90)
            t.forward(100)
            t.right(90)

        # Move to the next location
        t.right(90)
        t.forward(100 * len(row))
        t.left(90)
        t.forward(100)


# Modified main function
def main():
    parser = argparse.ArgumentParser(
        description="Draw a specified design with turtle graphics."
    )
    parser.add_argument(
        "--width", type=int, default=800, help="Width of the turtle screen."
    )
    parser.add_argument(
        "--height", type=int, default=600, help="Height of the turtle screen."
    )
    parser.add_argument(
        "--speed", type=int, choices=range(11), default=0, help="Speed of the turtle."
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
    parser.add_argument(
        "--output", type=str, default="animation.gif", help="Output GIF file name."
    )

    args = parser.parse_args()

    if args.savegif and not pil_available:
        print(
            "PIL (Pillow) is not available. The animation will not be saved as a GIF."
        )
        args.savegif = False  # Disable GIF saving if PIL is not available

    screen = turtle.Screen()
    screen.setup(width=args.width, height=args.height)
    screen.title(f"Turtle Drawing - {args.design.capitalize()}")

    path = f"designs/{args.design}.txt"
    design = load_design(path)

    t = turtle.Turtle(shape="turtle")
    t.speed(args.speed)

    start_x = -args.height / 2 + 20
    start_y = -args.width / 2 + 20

    t.penup()
    t.goto(start_x, start_y)
    t.pendown()

    # Modify the drawing process to optionally save each frame
    frame_count = 0
    for row in design:
        for pixel in row:
            draw_square(t, colour_dict[pixel])
            t.left(90)
            t.forward(100)
            t.right(90)

            # Save the frame if GIF saving is enabled
            if args.savegif:
                canvas = screen.getcanvas()
                canvas.postscript(file=f"frame_{frame_count:04}.eps")
                frame_count += 1

        t.right(90)
        t.forward(100 * len(row))
        t.left(90)
        t.forward(100)

    # Convert all frames to GIF and combine them if GIF saving is enabled
    if args.savegif:
        frames = []
        for i in range(frame_count):
            frame = Image.open(f"frame_{i:04}.eps")
            frame = frame.convert("RGBA")
            frame.save(f"frame_{i:04}.gif", "gif")
            frames.append(Image.open(f"frame_{i:04}.gif"))

        frames[0].save(
            args.output,
            save_all=True,
            append_images=frames[1:],
            optimize=False,
            duration=100,
            loop=0,
        )

        # Cleanup: remove temporary files
        for i in range(frame_count):
            os.remove(f"frame_{i:04}.eps")
            os.remove(f"frame_{i:04}.gif")

    screen.mainloop()


if __name__ == "__main__":
    main()
