#! /usr/local/bin/python3.3
import sys
import re
argv = sys.argv
# print('argvs are ', argv)
p = re.compile(argv[1])
print('regular expression is ' + argv[1])
file = argv[2:]
print('files are', file)
print()
for w in file:
    with open(w, mode='r',encoding='utf-8') as a_file:
        line_number = 0
        for a_line in a_file:
            line_number += 1
            if p.findall(a_line):
                print(w + ' {:>4} {}'.format(line_number, a_line.rstrip()))
