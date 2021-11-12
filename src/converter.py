#!/usr/bin/env python3

import json
import plistlib

from argparse import ArgumentParser
from pathlib import Path

RED = "Red Component"
GREEN = "Green Component"
BLUE = "Blue Component"

mappings = {
    "Ansi 0 Color": "0",
    "Ansi 1 Color": "1",
    "Ansi 2 Color": "2",
    "Ansi 3 Color": "3",
    "Ansi 4 Color": "4",
    "Ansi 5 Color": "5",
    "Ansi 6 Color": "6",
    "Ansi 7 Color": "7",
    "Ansi 8 Color": "8",
    "Ansi 9 Color": "9",
    "Ansi 10 Color": "10",
    "Ansi 11 Color": "11",
    "Ansi 12 Color": "12",
    "Ansi 13 Color": "13",
    "Ansi 14 Color": "14",
    "Ansi 15 Color": "15",
    "Background Color": "background",
    "Foreground Color": "foreground",
    "Cursor Color": "cursor",
}

def decimal_to_hex(decimal):
    return (hex(int(decimal * 255))[2:].upper()).zfill(2)

def color_dict_to_hex_string(color_dict):
    r = decimal_to_hex(color_dict.get(RED))
    g = decimal_to_hex(color_dict.get(GREEN))
    b = decimal_to_hex(color_dict.get(BLUE))

    return f"{r}{g}{b}"

def convert_theme(theme_file):
    filepath = Path(theme_file).resolve()
    if not filepath.exists():
        raise FileNotFoundError(f"Theme file '{theme_file}' not found")

    with filepath.open(mode="rb") as file:
        iterm = plistlib.load(file)

    info = {
        "name": filepath.stem,
        "colors": {}
    }

    for key, value in iterm.items():
        if key in mappings:
            info["colors"].update({mappings.get(key): color_dict_to_hex_string(value)})

    return info

def parse(source, target):
    source_path = Path(source).resolve()
    if not source_path.is_dir():
        raise NotADirectoryError(f"Source path '{source}' is not a directory")

    target_path = Path(target).resolve()
    if not target_path.exists():
        target_path.touch()

    info = []
    themes = list(source_path.glob('**/*.itermcolors'))
    themes = map(lambda path: path.name, themes)
    for theme in sorted(themes, key=str.lower):
        info.append(convert_theme(source_path / theme))

    with target_path.open(mode="w") as output:
        json.dump(info, output, indent=4)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("source", help="Directory containing .itermcolors files to parse")
    parser.add_argument("target", help="Path to JSON file to save output")
    args = parser.parse_args()

    try:
        parse(args.source, args.target)
    except (NotADirectoryError, FileNotFoundError) as e:
        print(e)
        exit(1)

