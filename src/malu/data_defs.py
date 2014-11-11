
# INPUT
# pattern string, consisting of >1 semicolon-separated pairs
# OUTPUT
# list of tuples (id, size_in_memory, duration)
def testPatternToArray(s):
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

    return requests

def preDefPattern(n):
    a = ["10,5;20,7;1,3;2,2;12,3","20,5;20,7;1,3;2,2;12,3", "30,5;20,7;1,3;2,2;12,3"]
    return a[n]

def idToLetter(id):     # 1 -> A, 2 -> B, ...
    return chr(64+id)




# make copy of processes array and return sorted by required field
def sortRequestsByField(requests, field):
    if isinstance(field, str):          # add support for referencing by name
        field = fieldNameToInt(field)
    return sorted(requests, key=lambda tup: tup[field])

def filterRequestsByField(requests, field, func):
    if isinstance(field, str):          # add support for referencing by name
        field = fieldNameToInt(field)
    return list(filter(lambda tup: func(tup[field]), requests))

def fieldNameToInt(fieldName):
    if fieldName.lower() == "id":
        return 0
    elif fieldName.lower() in ["size"]:
        return 1
    elif fieldName.lower() in ["duration"]:
        return 2
    else:       # unrecognised field key => throw error
        raise Exception("fieldNameToInt: Unknown field name")

def sortBlocksByField(blocks, field):
    if isinstance(field, str):
        field = blockFieldNameToInt(field)
    return sorted(blocks, key=lambda tup: tup[field])

def filterBlocksByField(blocks, field, func):
    if isinstance(field, str):
        field = blockFieldNameToInt(field)
    return list(filter(lambda tup: func(tup[field]), blocks))

def blockFieldNameToInt(fieldName):
    if fieldName.lower() == "id":
        return 0
    elif fieldName.lower() in ["duration", "left", "duration left"]:
        return 1
    elif fieldName.lower() in ["start", "start index"]:
        return 2
    elif fieldName.lower() in ["size", "size in memory"]:
        return 3
    else:       # unrecognised field key => throw error
        raise Exception("blockFieldNameToInt: Unknown field name")

def oneTimeStepForward(state):
    # For each block in this state, reduce duration by one
    newState = []
    for block in state:
        if block[1] > 1:                                                # if this block will not end
            newBlock = (block[0], block[1] - 1, block[2], block[3])     # reduce 'duration left' by one
            newState.append(newBlock)
    return newState

# [(1, 5, 0, 10), (2, 7, 10, 20)]
def getFreeBlocks(memory_state, MEMORY_SIZE):
    sorted_blocks = sortBlocksByField(memory_state, "start index")

    freeBlocks = []

    freeBlockStartIndex = 0

    if not sorted_blocks:
        return [(None, None, 0, MEMORY_SIZE)]
    else:
        firstOccupied = sorted_blocks[0]
        if firstOccupied[2] != 0:
            freeBlock = (None, None, 0, firstOccupied[2])
            freeBlocks.append(freeBlock)
        freeBlockStartIndex = firstOccupied[2] + firstOccupied[3]

        for block in sorted_blocks[1:]:
            if block[2] > freeBlockStartIndex:
                # add free block to list
                freeBlock = (None, None, freeBlockStartIndex, block[2] - freeBlockStartIndex)
                freeBlocks.append(freeBlock)

            freeBlockStartIndex = block[2] + block[3]     # remember end index of last block

        # now check if the end of last block was at MEMORY_SIZE, if not then add another free block
        if freeBlockStartIndex < MEMORY_SIZE:
            freeBlocks.append((None, None, freeBlockStartIndex, MEMORY_SIZE - freeBlockStartIndex))

    #raise Exception("getFreeBlocks: not implemented")
    #for block in memory_state:
    return freeBlocks





















