def pycprint(*args, sep=" ", end="\n", file=None, flush=False, timestamp=False, prefix=None, color=None, style=None, bg=None, cursor="true", **kwargs):
    # Prepare the concatenated message
    import sys
    import datetime
    import colorama
    import random
    colorama.init()
    concatenated_string = sep.join(map(str, args))

    class TextStyle:
     RESET = '\033[0m'
     BOLD = '\033[1m'
     UNDERLINE = '\033[4m'
     ITALIC = '\033[3m'
     INVERSE = '\033[7m'
     STRIKETHROUGH = '\033[9m'
     
    if cursor == "false":
        HIDE_CURSOR = '\033[?25l'
        RESET = '\033[0m'
        concatenated_string = f"{HIDE_CURSOR}{concatenated_string}{RESET}"
        
    # Apply text styles if specified
    if style == 'bold':
        concatenated_string = f"{TextStyle.BOLD}{concatenated_string}{TextStyle.RESET}"
    elif style == 'underline':
        concatenated_string = f"{TextStyle.UNDERLINE}{concatenated_string}{TextStyle.RESET}"
    elif style == 'italic':
        concatenated_string = f"{TextStyle.ITALIC}{concatenated_string}{TextStyle.RESET}"
    elif style == 'inverse':
        concatenated_string = f"{TextStyle.INVERSE}{concatenated_string}{TextStyle.RESET}"
    elif style == 'strikethrough':
        concatenated_string = f"{TextStyle.STRIKETHROUGH}{concatenated_string}{TextStyle.RESET}"

    
    # Add timestamp or prefix if specified
    if timestamp:
        try:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            concatenated_string = f"[{now}] {concatenated_string}"
        except Exception as e:
            print(f"Error formatting timestamp: {e}")
    
    elif prefix:
        concatenated_string = f"{prefix}: {concatenated_string}"
    
    # Apply text color if specified
    if color:
        if color in colorama.Fore.__dict__:
            color_code = getattr(colorama.Fore, color)
            concatenated_string = f"{color_code}{concatenated_string}{colorama.Style.RESET_ALL}"
        else:
            print(f"Invalid color '{color}' specified. Printing without color.")
    if bg:
        if bg in colorama.Fore.__dict__:
            color_code = getattr(colorama.Back, bg)
            concatenated_string = f"{color_code}{concatenated_string}{colorama.Style.RESET_ALL}"
        else:
            print(f"Invalid color '{bg}' specified. Printing without color.")
    
    # Determine where to print
    try:
        if file is None:
            output_stream = sys.stdout
        else:
            output_stream = open(file, 'a')
        
        try:
            # Print to the appropriate stream
            print(concatenated_string, end=end, file=output_stream, flush=flush, **kwargs)
        finally:
            # Close the file if opened
            if file is not None:
                output_stream.close()
    except Exception as e:
        print(f"Error printing: {e}")
    
    
