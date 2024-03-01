import turtle
import argparse

colour_dict = dict(
    b="blue",
    y="yellow",
    o="orange",
    k="black",
    w="white",
    G="#006400", # Dark green
    p="#FD4659", # Watermelon pink
    r='red',
    g="#8FBC8F", # Light green
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


def main():
    """
    Main function to load a design and draw it with command line arguments for customization.
    """
    parser = argparse.ArgumentParser(description="Draw a specified design with turtle graphics.")
    parser.add_argument("--width", type=int, default=800, help="Width of the turtle screen.")
    parser.add_argument("--height", type=int, default=600, help="Height of the turtle screen.")
    parser.add_argument("--speed", type=int, choices=range(11), default=0, help="Speed of the turtle, from 0 (fastest) to 10 (slowest).")
    parser.add_argument("--design", type=str, choices=['duck', 'heart', 'watermelon'], default='duck', help="Design name to draw (duck, watermelon or heart).")

    args = parser.parse_args()

    # Set up the screen with specified dimensions
    screen = turtle.Screen()
    screen.setup(width=args.width, height=args.height)
    screen.title(f"Turtle Drawing - {args.design.capitalize()}")

    # Load the specified design
    path = f"designs/{args.design}.txt"
    design = load_design(path)

    # Create a turtle and set its speed
    t = turtle.Turtle(shape="turtle")
    t.speed(args.speed)

    # The starting coordinates will be a bit above and to the right of the bottom-left corner
    # to ensure the turtle is visible and starts drawing within the window.
    # These coordinates assume a screen size of 800x600.
    start_x = -args.height / 2 + 20  # 20 units inward from the left edge
    start_y = -args.width / 2 + 20  # 20 units upward from the bottom edge

    # Move the turtle to the bottom-left corner without drawing
    t.penup()  # Don't draw when moving.
    t.goto(start_x, start_y)
    t.pendown()  # Ready to draw.

    # Draw the design
    draw_design(t, design)

    screen.mainloop()  # Keep the window open until closed by the user


if __name__ == "__main__":
    main()
