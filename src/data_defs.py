s = "0,10;4,5;12,4"

# INPUT
# pattern string, consisting of >1 semicolon-separated pairs
# each pair consists of process arrive time and process length
# OUTPUT
# list of tuples (id, arrive_time, duration)
def testPatternToArrays(s):
    pairs = s.strip().split(";")

    processes = []

    id = 1
    for pair_str in pairs:
        pair = pair_str.strip().split(",")
        processes.append((id, int(pair[0]), int(pair[1])))
        id += 1

    # result checks
    assert len(processes) != 0

    # sort by arrive time

    return sortProcessesByField(processes, "arrive_time")

# make copy of processes array and return sorted by required field
def sortProcessesByField(processes, field):
    if isinstance(field, str):          # add support for referencing by name
        field = fieldNameToInt(field)
    return sorted(processes, key=lambda tup: tup[field])

def filterProcessesByField(processes, field, func):
    if isinstance(field, str):          # add support for referencing by name
        field = fieldNameToInt(field)
    return list(filter(lambda tup: func(tup[field]), processes))

def fieldNameToInt(fieldName):
    if fieldName.lower() == "id":
        return 0
    elif fieldName.lower() in ["arrive_time", "arrived", "arrive", "arr"]:
        return 1
    elif fieldName.lower() in ["duration", "dur"]:
        return 2
    elif fieldName.lower() in ["start_time", "started", "sta"]:
        return 3
    else:       # unrecognised field key => throw error
        raise Exception("Unknown field name")

def addStartTime(p, start_time):
    l = list(p)
    l.append(start_time)
    return tuple(l)

def decreaseDuration(p, delta):
    l = list(p)
    l[2] = l[2] - delta
    return tuple(l)


def removeById(processes, id):
    toRemove = None
    for p in processes:
        if p[0] == id:
            toRemove = p
            break
    if toRemove is not None:
        processes.remove(toRemove)
    else:
        raise ValueError("no such ID in list")


def preDefPattern(n):
    a = ["0,10;4,5;12,4","mingiteinePattern", "mingiKolmasPattern"]
    return a[n]