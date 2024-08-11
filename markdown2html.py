#!/usr/bin/python3
"""
A script to convert a Markdown file to HTML.

Usage:
    ./markdown2html.py <input_file> <output_file>
"""

import sys
import os


def markdown_to_html(input_file, output_file):
    """Converts a Markdown file to HTML by processing headings and unordered lists."""
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        in_list = False
        for i in infile:
            stripped_line = i.strip()
            if stripped_line.startswith('#'):
                if in_list:
                    outfile.write("</ul>\n")
                    in_list = False
                heading_level = stripped_line.count('#')
                heading_text = stripped_line[heading_level:].strip()
                if 1 <= heading_level <= 6:
                    outfile.write(f"<h{heading_level}>{heading_text}</h{heading_level}>\n")

            elif stripped_line.startswith('- '):
                if not in_list:
                    outfile.write("<ul>\n")
                    in_list = True
                list_item_text = stripped_line[2:].strip()
                outfile.write(f"<li>{list_item_text}</li>\n")
            
            else:
                if in_list:
                    outfile.write("</ul>\n")
                    in_list = False
        
        if in_list:
            outfile.write("</ul>\n")

def main():
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    markdown_to_html(input_file, output_file)
    sys.exit(0)

if __name__ == "__main__":
    main()
