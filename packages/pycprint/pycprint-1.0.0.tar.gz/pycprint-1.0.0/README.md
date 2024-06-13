---

# printc: Enhanced Print Function for Python

`printc` is an enhanced print function for Python that provides additional features such as timestamping, text styling, colored output, and improved error handling, offering more flexibility and customization options compared to the standard `print` function.

## Features

- **Timestamps**: Optionally prepend messages with timestamps.
- **Prefixes**: Add customizable prefixes to messages for better categorization.
- **Text Styling**: Support for bold and underline text styles.
- **Text Coloring**: Ability to print text in various colors for visual differentiation.
- **File Output**: Direct output to both standard streams (`sys.stdout`, `sys.stderr`) and files for logging purposes.
- **Flexible Parameters**: Customize output behavior with parameters like `sep`, `end`, `flush`, etc.
- **Robust Error Handling**: Handles errors gracefully during timestamp formatting, file operations, and general printing.

## Installation

You can install `printc` from PyPI using pip:

```bash
pip install printc
```

## Usage

```python
from printc import printc

# Basic usage
printc("Hello", "World", sep="-", end="!\n")

# Adding timestamps
printc("Logging message", timestamp=True)

# Adding prefixes
printc("Error", "File not found", prefix="ERROR")

# Styling text
printc("Bold text", style="bold")
printc("Underlined text", style="underline")

# Coloring text (requires colorama package)
printc("Red text", color="RED")
printc("Blue text", color="BLUE")

# Output to a file
printc("Log entry", file="output.log")

# Customized usage with all options
printc("Detailed log entry", timestamp=True, prefix="INFO", style="bold", color="GREEN", file="output.log", flush=True)
```

## Parameters

- **`*args`**: Variable length arguments to print.
- **`sep`**: Separator between arguments (default is `" "`).
- **`end`**: Ending character(s) at the end of the printed line (default is `"\n"`).
- **`file`**: Output stream (`None` for standard output, file path for file output).
- **`flush`**: Whether to flush the output stream (default is `False`).
- **`timestamp`**: Whether to prepend messages with timestamps (default is `False`).
- **`prefix`**: Prefix string for messages (default is `None`).
- **`color`**: Text color (requires `colorama` package).
- **`style`**: Text style (`bold`, `underline`, or `None` for normal text).
- **`**kwargs`**: Additional keyword arguments passed to the underlying `print` function.

## Dependencies

- `colorama`: Required for text coloring (automatically installed with `pip`).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the need for enhanced printing capabilities in Python applications.

---

### Notes:

- **Dependencies**: Ensure to mention dependencies like `colorama` and include instructions for installation if not automatically handled by `pip`.
- **Examples**: Provide various examples demonstrating different features and combinations of parameters to illustrate usage scenarios effectively.

