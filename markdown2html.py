#!/usr/bin/python3
"""
A script to convert a Markdown file to HTML.

Usage:
    ./markdown2html.py <input_file> <output_file>
"""

import sys
import os
import re

def replace_bold_and_emphasis(text):
    """Replaces Markdown bold and emphasis with corresponding HTML tags."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.+?)__', r'<em>\1</em>', text)
    return text

def markdown_to_html(input_file, output_file):
    """Converts a Markdown file to HTML by processing headings, lists, paragraphs, and bold/emphasis."""
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        in_unordered_list = False
        in_ordered_list = False
        in_paragraph = False
        
        for i in infile:
            stripped_line = i.strip()
            stripped_line = replace_bold_and_emphasis(stripped_line)

            if stripped_line.startswith('#'):
                if in_unordered_list:
                    outfile.write("</ul>\n")
                    in_unordered_list = False
                if in_ordered_list:
                    outfile.write("</ol>\n")
                    in_ordered_list = False
                if in_paragraph:
                    outfile.write("</p>\n")
                    in_paragraph = False

                heading_level = stripped_line.count('#')
                heading_text = stripped_line[heading_level:].strip()
                if 1 <= heading_level <= 6:
                    outfile.write(f"<h{heading_level}>{heading_text}</h{heading_level}>\n")
            
            elif stripped_line.startswith('- '):
                if in_ordered_list:
                    outfile.write("</ol>\n")
                    in_ordered_list = False
                if in_paragraph:
                    outfile.write("</p>\n")
                    in_paragraph = False
                if not in_unordered_list:
                    outfile.write("<ul>\n")
                    in_unordered_list = True
                list_item_text = stripped_line[2:].strip()
                list_item_text = replace_bold_and_emphasis(list_item_text)
                outfile.write(f"<li>{list_item_text}</li>\n")
            
            elif stripped_line.startswith('* '):
                if in_unordered_list:
                    outfile.write("</ul>\n")
                    in_unordered_list = False
                if in_paragraph:
                    outfile.write("</p>\n")
                    in_paragraph = False
                if not in_ordered_list:
                    outfile.write("<ol>\n")
                    in_ordered_list = True
                list_item_text = stripped_line[2:].strip()
                list_item_text = replace_bold_and_emphasis(list_item_text)
                outfile.write(f"<li>{list_item_text}</li>\n")
            
            elif stripped_line == "":
                if in_paragraph:
                    outfile.write("</p>\n")
                    in_paragraph = False
                if in_unordered_list:
                    outfile.write("</ul>\n")
                    in_unordered_list = False
                if in_ordered_list:
                    outfile.write("</ol>\n")
                    in_ordered_list = False
            
            else:
                if in_unordered_list:
                    outfile.write("</ul>\n")
                    in_unordered_list = False
                if in_ordered_list:
                    outfile.write("</ol>\n")
                    in_ordered_list = False
                if not in_paragraph:
                    outfile.write("<p>\n")
                    in_paragraph = True
                else:
                    outfile.write("<br/>\n")
                outfile.write(f"{stripped_line}\n")
        
        if in_paragraph:
            outfile.write("</p>\n")
        if in_unordered_list:
            outfile.write("</ul>\n")
        if in_ordered_list:
            outfile.write("</ol>\n")


def main():
    """Main function that handles argument parsing and file checks."""
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
