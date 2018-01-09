import sys
import re

infile = str(sys.argv[1])
outfile = str(sys.argv[2])
def test_patterns(text, patterns = []):
    for pattern in patterns:
        p = re.compile(pattern)
        try:
            match = p.search(text)
            a1 = match.group(1)
            a2 = match.group(2)
            a3 = match.group(3)
            a4 = match.group(4)
            a5 = match.group(5)
            data = ''.join([a1.strip(),'@',a3.strip(),'.',a5.strip()])
            print(''.join([a1.strip(),'@',a3.strip(),'.',a5.strip()]))
        except:
            data = "None"
    return data+'\n'

if __name__ == '__main__':
    i = open(infile,'r')
    lines = i.readlines()
    ls = []
    for line in lines:
        ls.append(test_patterns(line,['([^\s>]+\s?)(@|\sat\s ){1}([\s]?[\w|\d]*[\s]?)(\.|dot){1}([\s]?[\w]+)']))
    o = open(outfile,'w')
    for line in ls:
        o.write(line)
