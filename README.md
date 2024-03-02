# kaituitui

An animated beader using python's turtle module

This Python program allows you to draw predefined designs using the turtle graphics library. You can customize the drawing by specifying the design, as well as the screen dimensions and turtle speed via command-line arguments.
Installation

Before running the program, ensure you have Python installed on your system. This program has been tested with Python 3.8 and above.

No additional Python libraries are required apart from turtle and argparse, which are included in the standard Python library. You do however need to install tkinter.

## Usage

To run the program, navigate to the program's directory in your terminal and use the following command:


```bash
python kaituitui.py --width 800 --height 600 --speed 5 --design watermelon
```

You can replace design_drawer.py with the name of your Python script.
Command-Line Arguments

    --width: Sets the width of the turtle screen (default is 800).
    --height: Sets the height of the turtle screen (default is 600).
    --speed: Sets the speed of the turtle, where 0 is the fastest and 10 is the slowest (default is 0).
    --design: Chooses the design to draw. Options are duck, watermelon, or heart (default is duck).

## Designs

The designs should be defined in text files within a directory named designs at the same level as the script. Each design file (duck.txt, watermelon.txt, heart.txt) contains a specific pattern that maps to the design's shape and color. Each pair of characters in these files represents a color (as defined in colour_dict) and a repetition count.
Example

To draw a heart design with a screen width of 900, a height of 700, at a turtle speed of 3, use the following command:

```bash
python kaituitui.py --width 900 --height 700 --speed 3 --design heart
```

This command will initiate the turtle graphics window and start drawing the specified heart design with the given parameters.

## Modifying Designs

To add or modify designs, edit or create new text files in the designs directory. Each line in a design file should consist of pairs of characters where the first character is a key from colour_dict representing a color and the second character is a digit representing how many times to repeat that color in a row.
Closing the Program

Close the turtle graphics window to terminate the program.

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository where this program is hosted.
