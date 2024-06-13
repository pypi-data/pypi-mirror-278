import json
import sys
from importlib.metadata import version

from levels import levels

__doc__ = f"""
¤ ~ ^ - levels - ^ ~ ¤
*. - _ of depth _ - .*
'_- _ - {version("levels")} - _ - _'

A vertical slicing tool for nested data structures of dictionaries and/or lists. (JSON)

Usage: python -m levels <filename.json> <level> [--generate <output_filename>]
Examples:

    Print the values of the JSON file at level 2:
python -m levels data.json 2

    Generate a script that prints the values of the JSON file at level 2:
python -m levels data.json 2 --generate script.py

Arguments:
    --help: Show this help message and exit

    filename: The JSON file to read
    level: The level to print
    --generate: Generate a script that prints the values of the JSON file at the given level
    output_filename: The name of the script to generate
"""


def generate_basic_script(filename, level, output_filename, data):
    script = f"""import json

with open("{filename}") as f:
    data = json.load(f)

"""
    script += f"print('Level {level}')\n"
    script += "\n".join(
        [f"print(data{path})  # {value}" for path, value in levels(data, level)]
    )

    with open(output_filename, "w") as f:
        f.write(script)


def main():
    if len(sys.argv) == 1 or sys.argv[1] in {"-h", "--help"}:
        print(__doc__)

        sys.exit(1)
    filename = sys.argv[1]
    try:
        level = int(sys.argv[2])
    except (ValueError, IndexError):
        print("Level must be an integer")
        sys.exit(1)
    with open(filename) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("Invalid JSON file")
            sys.exit(1)

    try:
        if sys.argv[3] == "--generate" and sys.argv[4]:
            output_filename = sys.argv[4]
            generate_basic_script(filename, level, output_filename, data)
            print(f"Script generated to {output_filename}")

    except IndexError:
        for path, value in levels(data, level):
            print(f"{path}: {value}")

    except IOError:
        print("Error writing to file")
        sys.exit(1)


if __name__ == "__main__":
    main()
