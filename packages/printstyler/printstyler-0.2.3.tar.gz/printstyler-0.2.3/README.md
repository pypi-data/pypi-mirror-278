# Printer Package

The `printstyler` package provides a simple way to print messages with ANSI colors and styles in Python.

## Installation

You can install the package using pip:

```bash
pip install printstyler



## Available Colors
- black
- red
- green
- yellow
- blue
- magenta
- cyan
- white

## Available Styles
- bold
- faint
- italic
- underline
- blink
- reversed
- hidden

#Usage

from printstyler import Printer as pr


# Print a standard message
pr.standard("This is a standard message", style="bold")

# Print an error message
pr.error("This is an error message", style="underline")

# Print an info message
pr.info("This is an info message", style="italic")

# Print a warning message
pr.warning("This is a warning message", style="blink")

# Print a success message
pr.success("This is a success message", style="reversed")

# Print a debug message
pr.debug("This is a debug message", style="hidden")

# Print a custom message
pr.custom("This is a custom message", color="white", style="bold", prefix="Custom:")


![example](image.png)