# Printer Package

The `Printer` package provides a simple way to print messages with ANSI colors and styles in Python.

## Installation

You can install the package using pip:

```bash
pip install printer



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

from printer import Printer as p



# Print a standard message
p.standard("This is a standard message", style="bold")

# Print an error message
p.error("This is an error message", style="underline")

# Print an info message
p.info("This is an info message", style="italic")

# Print a warning message
p.warning("This is a warning message", style="blink")

# Print a success message
p.success("This is a success message", style="reversed")

# Print a debug message
p.debug("This is a debug message", style="hidden")

# Print a custom message
p.custom("This is a custom message", color="cyan", style="bold", prefix="Custom:")
