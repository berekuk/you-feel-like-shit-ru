import sys
import re

def genderize_line(line, gender):
    assert gender in ('m', 'f')

    def repl_word(match):
        return match.group(1 if gender == 'm' else 2)
    line = re.sub(r'\((\w*)\)\((\w*)\)', repl_word, line)

    if gender == 'f':
        line = re.sub(r'pid="(\d+)"', r'pid="9\1"', line)

    def repl_name(match):
        return 'name="{}/{}"'.format(match.group(1), gender)
    line = re.sub(r'name="(.+?)"', repl_name, line)

    def repl_simple_link(match):
        return '[[{}|{}/{}]]'.format(match.group(1), match.group(1), gender)
    def repl_named_link(match):
        return '[[{}|{}/{}]]'.format(match.group(1), match.group(2), gender)
    line = re.sub(r'\[\[([^|]+)\|(.*?)\]\]', repl_named_link, line)
    line = re.sub(r'\[\[([^|]+)\]\]', repl_simple_link, line)

    return line


def extract_gendered_words(fh):
    for line in fh:
        match = re.search('(\w+)\((\w*)\)\((\w*)\)', line)
        if not match:
            continue
        print(match.group(1) + match.group(2), "\t", match.group(1) + match.group(3))

def genderize(fh):
    for line in open('pre.html'):
        print(line, end='')

    # prologue
    for line in fh:
        if line == "<!-- START GENDERING -->\n":
            break
        print(line, end='')

    lines = []
    for line in fh:
        if line == "<!-- END GENDERING -->\n":
            break
        lines.append(line)
    for gender in ('m', 'f'):
        for line in lines:
            print(genderize_line(line, gender), end='')

    # epilogue
    for line in fh:
        print(line, end=None)

    for line in open('post.html'):
        print(line, end=None)

genderize(open('translated.html'))
