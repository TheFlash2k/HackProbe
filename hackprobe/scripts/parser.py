import json
import marko
import argparse
from bs4 import BeautifulSoup
import re
from entry import Entry

def html_to_json(
    input_html : str
):
    soup = BeautifulSoup(input_html, 'html.parser')

    h2_tags = soup.find_all('h2')
    result = []

    for h2 in h2_tags:
        content = str(h2)
        next_sibling = h2.find_next_sibling()
        while next_sibling and next_sibling.name != 'h2':
            content += str(next_sibling)
            next_sibling = next_sibling.find_next_sibling()
        result.append(content)

    entries = [Entry]

    for i in result:
        entry = Entry()
        entry.tags = [re.sub(r"<.*?>", "", i.strip()) for i in re.findall(r'<blockquote>(.*?)</blockquote>', i, re.DOTALL)[0].split(',')]
        print(f"[*] Found tags: {entry.tags}")
        entry.description = re.sub(r"<.*?>", "", re.findall(r'<h2>(.*?)</h2>', i, re.DOTALL)[0])
        print(f"[*] Found description: {entry.description}")
        print(i, '\n\n')


def md_to_json(
    input_md : str,
):
    html = marko.convert(md)
    
    return html_to_json(
        input_html=html
    )

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='HackProbe Markdown to JSON Parser', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', help='Input Markdown file', required=True, type=str)
    parser.add_argument('-o', '--output', help='Output JSON file', default='cheat-sheet.json')

    args = parser.parse_args()

    in_md = args.input
    out_json = args.output

    with open(in_md, 'r') as f:
        md = f.read()

    print(f"Input Markdown file: {in_md}")
    md_to_json(input_md=in_md)

    pass