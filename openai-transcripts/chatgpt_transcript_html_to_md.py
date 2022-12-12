# Takes a single command-line argument: the ChatGPT saved HTML file to convert to Markdown format.
from bs4 import BeautifulSoup, NavigableString
import re
import sys

def mdescape(s):
    return re.sub("\n", "<br>\n", re.sub("[*#()\[\]!|+<>_]", "\\\\\g<0>", s))

with open(sys.argv[1]) as f:
    soup = BeautifulSoup(f, 'html.parser')

elts = [e for e in soup.find_all('div',class_="min-h-[20px] whitespace-pre-wrap flex flex-col items-start gap-4") if len(e.get_text()) > 1]

for i, elt in enumerate(elts):
    if elt.contents[0].name == 'div':
        who = "ChatGPT"
        subelts = elt.contents[0].find_all(['p', 'pre'], recursive=False)
        lines = []
        for e in subelts:
            if e.name == 'p':
                for c in e.children:
                    #import pdb;pdb.set_trace()
                    if isinstance(c, NavigableString):
                        c.replace_with(mdescape(c.string))
                for c in e('code'):
                    c.insert_before('`')
                    c.insert_after('`')
                for s in e('strong'):
                    s.insert_before('\*\*')
                    s.insert_after('\*\*')
                lines += e.get_text().split('\n')
            elif e.name == 'pre':
                lines += ["    " + s for s in e.find('code').get_text().split('\n')]
            lines += ['']
    elif elt.string:
        lines = mdescape(elt.string).split('\n')
        who = "Human"
    else:
        continue

    print(f"\n### {who}\n")
    for line in lines:
        print(f"{(line)}")
