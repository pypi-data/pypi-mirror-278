import sys
import datetime
import colorama

colorama.init()

class TextStyle:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printc(*args, sep=" ", end="\n", file=None, flush=False, timestamp=False, prefix=None, color=None, style=None, **kwargs):
    # Prepare the concatenated message
    concatenated_string = sep.join(map(str, args))
    
    # Apply text styles if specified
    if style == 'bold':
        concatenated_string = f"{TextStyle.BOLD}{concatenated_string}{TextStyle.RESET}"
    elif style == 'underline':
        concatenated_string = f"{TextStyle.UNDERLINE}{concatenated_string}{TextStyle.RESET}"
    
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

# Example usage
printc("apple", "banana", "cherry", sep="/", end="***", timestamp=True, color="GREEN")
printc("pineapple", "orange", "grape", sep=", ", file="output.txt", flush=True, prefix="INFO", style="bold")
