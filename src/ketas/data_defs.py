
# INPUT
# pattern string, consisting of >1 comma-separated requests
# OUTPUT
# list of requests ordered by arrive time

MAX_INDEX = 50

def testPatternToArray(s):
    requests_str = s.strip().split(",")
    toInt = lambda x: int(x)
    requests = list(map(toInt, requests_str))
    if list(filter(lambda x: x > MAX_INDEX-1, requests)):
        raise Exception("User index too large")
    return list(map(toInt, requests))

def preDefPattern(n):
    a = ["15,8,17,27,9,1,14", "1,2,3,4,5,29,45,6,7,8", "16,49,34,0,2,7,18,25"]
    return a[n]

def idToLetter(id):     # 1 -> A, 2 -> B, ...
    return chr(64+id)

#print(testPatternToArray(preDefPattern(0)))