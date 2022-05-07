import sys 

KEYWORDS = []
with open('keys.txt', 'r') as f:
    KEYWORDS = f.readline().split()


for line in sys.stdin:
    line = line.strip()
    words = line.split()
    
    for word in words:
        word = word.lower()
        if word in KEYWORDS:
            print('%s\t%s' % (word, 1))