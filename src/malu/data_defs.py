
# INPUT
# pattern string, consisting of >1 semicolon-separated pairs
# each pair consists of process arrive time and process length
# OUTPUT
# list of tuples (id, arrive_time, duration)
def testPatternToArray(s):              # TODO parse input correctly/rename
    pairs = s.strip().split(";")

    requests = []

    id = 1
    for pair_str in pairs:
        pair = pair_str.strip().split(",")
        requests.append((id, int(pair[0]), int(pair[1])))
        id += 1

    # result checks
    assert len(requests) != 0

    # sort by arrive time

    return requests, "arrive_time"

# make copy of processes array and return sorted by required field
def sortProcessesByField(processes, field): #TODO rename input
    if isinstance(field, str):          # add support for referencing by name
        field = fieldNameToInt(field)
    return sorted(processes, key=lambda tup: tup[field])

def filterProcessesByField(processes, field, func): #TODO rename input
    if isinstance(field, str):          # add support for referencing by name
        field = fieldNameToInt(field)
    return list(filter(lambda tup: func(tup[field]), processes))

def fieldNameToInt(fieldName): #TODO specify field names
    if fieldName.lower() == "id":
        return 0
    elif fieldName.lower() in ["size"]:
        return 1
    elif fieldName.lower() in ["duration"]:
        return 2
    else:       # unrecognised field key => throw error
        raise Exception("fieldNameToInt: Unknown field name")

def preDefPattern(n):
    a = ["10,5;20,7;1,3;2,2;12,3","20,5;20,7;1,3;2,2;12,3", "30,5;20,7;1,3;2,2;12,3"]
    return a[n]

def idToLetter(id):     # 1 -> A, 2 -> B, ...
    return chr(64+id)
