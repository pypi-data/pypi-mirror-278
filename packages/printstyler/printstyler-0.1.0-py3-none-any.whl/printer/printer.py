class Printer:
    """
    A class to print messages with ANSI colors and styles.

    Available colors:
        - black
        - red
        - green
        - yellow
        - blue
        - magenta
        - cyan
        - white

    Available styles:
        - bold
        - faint
        - italic
        - underline
        - blink
        - reversed
        - hidden
    """
    
    COLORS = {
        'reset': '\033[0m',
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m'
    }

    STYLES = {
        'bold': '\033[1m',
        'faint': '\033[2m',
        'italic': '\033[3m',
        'underline': '\033[4m',
        'blink': '\033[5m',
        'reversed': '\033[7m',
        'hidden': '\033[8m'
    }

    @staticmethod
    def validate_parameters(style: str, sep: str, end: str, file) -> None:
        """
        Validate parameters for printing.
        
        Parameters:
            style (str): The style to apply.
            sep (str): Separator between messages.
            end (str): End character.
            file: The file to write to.
            
        Raises:
            ValueError: If any parameter is invalid.
        """
        try:
            if style and style not in Printer.STYLES:
                raise ValueError(f"Invalid style: {style}. Must be one of {list(Printer.STYLES.keys())}.")
            if sep is not None and not isinstance(sep, str):
                raise ValueError("Separator must be a string.")
            if end is not None and not isinstance(end, str):
                raise ValueError("End character must be a string.")
            if file is not None and not hasattr(file, 'write'):
                raise ValueError("File must be an object with a write method.")
            return True
        except ValueError as e:
            Printer.warning(f"Validation Error: {e}")
            return False

    @staticmethod
    def standard(message: str, style: str = None, sep: str = ' ', end: str = '\n', file=None, flush: bool = False) -> None:
        """
        Print a message in green color with "Success: " prefix.

        Parameters:
            message (str): The message to print.
            style (str, optional): The style to apply. Default is None.
            sep (str, optional): Separator between messages. Default is ' '.
            end (str, optional): End character. Default is '\n'.
            file (optional): The file to write to. Default is None.
            flush (bool, optional): Whether to flush the output. Default is False.
        """
        try:
            if Printer.validate_parameters(style, sep, end, file):
                style_code = Printer.STYLES.get(style, '')
                prefix = "Success: "
                print(f"{style_code}{Printer.COLORS['green']}{prefix}{message}{Printer.COLORS['reset']}", sep=sep, end=end, file=file, flush=flush)
        except Exception as e:
            Printer.warning(f"Error: {e}")

    @staticmethod
    def error(message: str, style: str = None, sep: str = ' ', end: str = '\n', file=None, flush: bool = False) -> None:
        """
        Print a message in red color with "Error: " prefix.

        Parameters:
            message (str): The message to print.
            style (str, optional): The style to apply. Default is None.
            sep (str, optional): Separator between messages. Default is ' '.
            end (str, optional): End character. Default is '\n'.
            file (optional): The file to write to. Default is None.
            flush (bool, optional): Whether to flush the output. Default is False.
        """
        Printer.validate_parameters(style, sep, end, file)
        style_code = Printer.STYLES.get(style, '')
        prefix = "Error: "
        print(f"{style_code}{Printer.COLORS['red']}{prefix}{message}{Printer.COLORS['reset']}", sep=sep, end=end, file=file, flush=flush)

    @staticmethod
    def info(message: str, style: str = None, sep: str = ' ', end: str = '\n', file=None, flush: bool = False) -> None:
        """
        Print a message in blue color with "Info: " prefix.

        Parameters:
            message (str): The message to print.
            style (str, optional): The style to apply. Default is None.
            sep (str, optional): Separator between messages. Default is ' '.
            end (str, optional): End character. Default is '\n'.
            file (optional): The file to write to. Default is None.
            flush (bool, optional): Whether to flush the output. Default is False.
        """
        Printer.validate_parameters(style, sep, end, file)
        style_code = Printer.STYLES.get(style, '')
        prefix = "Info: "
        print(f"{style_code}{Printer.COLORS['blue']}{prefix}{message}{Printer.COLORS['reset']}", sep=sep, end=end, file=file, flush=flush)

    @staticmethod
    def warning(message: str, style: str = None, sep: str = ' ', end: str = '\n', file=None, flush: bool = False) -> None:
        """
        Print a message in yellow color with "Warning: " prefix.

        Parameters:
            message (str): The message to print.
            style (str, optional): The style to apply. Default is None.
            sep (str, optional): Separator between messages. Default is ' '.
            end (str, optional): End character. Default is '\n'.
            file (optional): The file to write to. Default is None.
            flush (bool, optional): Whether to flush the output. Default is False.
        """
        Printer.validate_parameters(style, sep, end, file)
        style_code = Printer.STYLES.get(style, '')
        prefix = "Warning: "
        print(f"{style_code}{Printer.COLORS['yellow']}{prefix}{message}{Printer.COLORS['reset']}", sep=sep, end=end, file=file, flush=flush)

    @staticmethod
    def success(message: str, style: str = None, sep: str = ' ', end: str = '\n', file=None, flush: bool = False) -> None:
        """
        Print a message in magenta color with "Success: " prefix.

        Parameters:
            message (str): The message to print.
            style (str, optional): The style to apply. Default is None.
            sep (str, optional): Separator between messages. Default is ' '.
            end (str, optional): End character. Default is '\n'.
            file (optional): The file to write to. Default is None.
            flush (bool, optional): Whether to flush the output. Default is False.
        """
        Printer.validate_parameters(style, sep, end, file)
        style_code = Printer.STYLES.get(style, '')
        prefix = "Success: "
        print(f"{style_code}{Printer.COLORS['magenta']}{prefix}{message}{Printer.COLORS['reset']}", sep=sep, end=end, file=file, flush=flush)

    @staticmethod
    def debug(message: str, style: str = None, sep: str = ' ', end: str = '\n', file=None, flush: bool = False) -> None:
        """
        Print a message in cyan color with "Debug: " prefix.

        Parameters:
            message (str): The message to print.
            style (str, optional): The style to apply. Default is None.
            sep (str, optional): Separator between messages. Default is ' '.
            end (str, optional): End character. Default is '\n'.
            file (optional): The file to write to. Default is None.
            flush (bool, optional): Whether to flush the output. Default is False.
        """
        Printer.validate_parameters(style, sep, end, file)
        style_code = Printer.STYLES.get(style, '')
        prefix = "Debug: "
        print(f"{style_code}{Printer.COLORS['cyan']}{prefix}{message}{Printer.COLORS['reset']}", sep=sep, end=end, file=file, flush=flush)


    def custom(message: str, color: str = None, style: str = None, prefix: str = None, sep: str = ' ', end: str = '\n', file=None, flush: bool = False) -> None:
        """
        Print a message in a custom color with an optional prefix.

        Parameters:
            message (str): The message to print.
            color (str): The color to apply.
            style (str, optional): The style to apply. Default is None.
            prefix (str, optional): The prefix to add. Default is None.
            sep (str, optional): Separator between messages. Default is ' '.
            end (str, optional): End character. Default is '\n'.
            file (optional): The file to write to. Default is None.
            flush (bool, optional): Whether to flush the output. Default is False.
        """
        try:
            if not color:
                Printer.warning("Validation Error: The 'color' parameter is required.")
                return
            
            if Printer.validate_parameters(style, sep, end, file):
                style_code = Printer.STYLES.get(style, '')
                color_code = Printer.COLORS.get(color, Printer.COLORS['white'])
                if prefix:
                    message = f"{prefix} {message}"
                print(f"{style_code}{color_code}{message}{Printer.COLORS['reset']}", sep=sep, end=end, file=file, flush=flush)
                # Depuración adicional
                print(f"Debug: {style_code}{color_code}{message}{Printer.COLORS['reset']}")
        except ValueError as e:
            Printer.warning(f"Error: {e}")


