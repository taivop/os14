s = "0,10;4,5;12,4"

# INPUT
# pattern string, consisting of >1 semicolon-separated pairs
# each pair consists of process arrive time and process length
# OUTPUT
# tuples (id, arrive_time, duration)
def testPatternToArrays(s):
    pairs = s.strip().split(";")

    processes = []

    id = 0
    for pair_str in pairs:
        pair = pair_str.strip().split(",")
        processes.append((id, int(pair[0]), int(pair[1])))
        id += 1

    # result checks
    assert len(processes) != 0

    # sort by arrive time

    return processes

# make copy of processes array and return sorted by required field
def sortProcessesByField(processes, field):
    if isinstance(field, str):          # add support for referencing by name
        if field.lower() == "id":
            field = 0
        elif field.lower() in ["arrive_time", "arrived", "arrive", "arr"]:
            field = 1
        elif field.lower() in ["duration", "dur"]:
            field = 2
        else:       # unrecognised field key => sort by ID
            field = 0
    return sorted(processes, key=lambda tup: tup[field])


print(sortProcessesByField(testPatternToArrays(s), "duration"))