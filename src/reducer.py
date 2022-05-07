from operator import itemgetter
import sys

lastWord = None 
lastCount = 0
word = None 

for line in sys.stdin:
    line = line.strip()
    word, count = line.split('\t', 1)

    try:
        count = int(count)
    except ValueError:
        pass 
    
    # the words are alphabetically sorted
    if lastWord == word:
        lastCount += count 
    else:
        if lastWord:
            print('%s\t%s' % (lastWord, lastCount))
        lastWord = word 
        lastCount = count 

if lastWord == word:
    print('%s\t%s' % (lastWord, lastCount))
