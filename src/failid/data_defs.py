
# INPUT
# pattern string, consisting of >1 semicolon-separated pairs (fileID, ???)
# OUTPUT
# list of requests ordered by arrive time

MAX_INDEX = 50

def testPatternToArray(s):
    pairs = s.strip().split(";")
    requests = []

    def toInt(x):
        if x == '-':
            return -1
        else:
            return int(x)

    for pair in pairs:
        sp = pair.strip().split(",")
        requests.append((sp[0], toInt(sp[1])))

    return requests

def preDefPattern(n):
    a = ["A,2;B,5;A,0;C,4", "A,2;B,5;A,0;C,4", "A,2;B,5;A,0;C,4"]
    return a[n]

def idToLetter(id):     # 1 -> A, 2 -> B, ...
    return chr(64+id)

def letterToId(letter):
    return ord(letter)-64

print(testPatternToArray(preDefPattern(1)))