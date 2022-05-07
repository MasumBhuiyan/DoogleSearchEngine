import sys 
from const import KEYWORDS

points = 0

for line in sys.stdin:
    line = line.strip()
    word, count = line.split('\t', 1)

    if word in KEYWORDS:
        points += int(count)  

print("%s" % (points))