# kaituitui

An animated beader using python's turtle module

This Python program allows you to draw predefined designs using the turtle graphics library. You can customize the drawing by specifying the design, as well as the screen dimensions and turtle speed via command-line arguments.
Installation

Before running the program, ensure you have Python installed on your system. This program has been tested with Python 3.8 and above.

No additional Python libraries are required apart from turtle and argparse, which are included in the standard Python library. You do however need to install tkinter, and PIL (the Python Image Library) is required if you want to generate gifs.

## Usage

To run the program, navigate to the program's directory in your terminal and use the following command (for example):


```bash
python kaituitui.py --width 800 --height 600 --speed 5 --repeats 2 --design watermelon
```

You can replace design_drawer.py with the name of your Python script.
Command-Line Arguments
    
    --width: Sets the width of the screen (default is 800 + the height is calculated automatically).
    --speed: Sets the speed of the turtle. Options are 'fast' or 'slow'
    --design: Chooses the design to draw. Options are 'duck', 'watermelon', or 'heart' (default is duck).
    --repeats: Chooses how many times to repeat the design horizontally
    --savegif: If provided, the animation will be saved to the gifs/ directory

## Designs

The designs should be defined in text files within a directory named designs at the same level as the script. Each design file (duck.txt, watermelon.txt, heart.txt) contains a specific pattern that maps to the design's shape and color. Each pair of characters in these files represents a color (as defined in colour_dict) and a repetition count.

Users can create their own design files if they like, and animate them. The designs provided are from students at James Bay Eeyou School in Chisasibi, Cree Nation.

### Example

To draw a heart design with a screen width of 900, a height of 700, at a turtle speed of 3, use the following command:

```bash
python kaituitui.py --width 900 --speed fast --repeats 3 --design heart
```

This command will initiate the turtle graphics window and start drawing the specified heart design with the given parameters.

## Modifying Designs

To add or modify designs, edit or create new text files in the designs directory. Each line in a design file should consist of pairs of characters where the first character is a key from colour_dict representing a color and the second character is a digit representing how many times to repeat that color in a row.
Closing the Program

Close the turtle graphics window to terminate the program.

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository where this program is hosted.
