import sys
import re

print(sys.argv)
infile = str(sys.argv[1])
outfile = str(sys.argv[2])
def test_patterns(text, patterns = []):
    print
    for pattern in patterns:
        p = re.compile(pattern)
        try:
            match = p.search(text)
            s = match.start()
            e = match.end()
            data = text[s:e]
        except:
            data = "None"
        print(data)
    return data+'\n'

if __name__ == '__main__':
    i = open(infile,'r')
    lines = i.readlines()
    ls = []
    for line in lines:
        ls.append(test_patterns(line,['([\w|\d]+\s?(@|at){1}([\s]?)[\w|\d]*([\s]?)(\.|dot){1}([\s]?)[\w]+)']))
    o = open(outfile,'w')
    for line in ls:
        o.write(line)
