import sys
import re

print(sys.argv)
def test_patterns(text, patterns = []):
    print
    for pattern in patterns:
        p = re.compile(pattern)
        try:
            match = p.search(text)
            s = match.start()
            e = match.end()
            print(text[s:e])
        except:
            print(None)
    return

if __name__ == '__main__':
    test_patterns('abbaaabbbaaaaa',['ab'])
    f = open('trial-pages.txt','r')
    lines = f.readlines()
    for line in lines:
        test_patterns(line,['([\w|\d]+\s?(@|at){1}([\s]?)[\w|\d]*([\s]?)(\.|dot){1}([\s]?)[\w]+)'])
