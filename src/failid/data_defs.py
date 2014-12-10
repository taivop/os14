
# INPUT
# pattern string, consisting of >1 semicolon-separated pairs (fileID, file_size)
# OUTPUT
# list of requests ordered by arrive time

DISK_SIZE = 50

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

def sortBlocksByStartIndex(state):
    return sorted(state, key=lambda tup: tup[1])

def sortBlocksByEndIndex(state):
    return sorted(state, key=lambda tup: tup[2])



def preDefPattern(n):
    a = ["A,2;B,5;A,-;C,4", "A,2;B,5;A,-;C,4;D,1;E,3;B,-;F,11;G,2;H,3", "A,3;B,44;A,-;C,1;D,6", "A,2;B,5;A,-;C,4;D,1;E,3;B,-;F,1;G,2;H,3;I,1;J,2"]
    return a[n]

def idToLetter(id):     # 1 -> A, 2 -> B, ...
    return chr(64+id)

def letterToId(letter):
    return ord(letter)-64

def getFreeBlocks(disk_state, DISK_SIZE):
    sorted_blocks = sortBlocksByStartIndex(disk_state)

    freeBlocks = []

    freeBlockStartIndex = 0

    if not sorted_blocks:
        return [(None, 0, DISK_SIZE)]
    else:
        firstOccupied = sorted_blocks[0]
        if firstOccupied[1] != 0:
            freeBlock = (None, 0, firstOccupied[1])
            freeBlocks.append(freeBlock)
        freeBlockStartIndex = firstOccupied[1] + firstOccupied[2]

        for block in sorted_blocks[1:]:
            if block[1] > freeBlockStartIndex:
                # add free block to list
                freeBlock = (None, freeBlockStartIndex, block[1] - freeBlockStartIndex)
                freeBlocks.append(freeBlock)

            freeBlockStartIndex = block[1] + block[2]     # remember end index of last block

        # now check if the end of last block was at MEMORY_SIZE, if not then add another free block
        if freeBlockStartIndex < DISK_SIZE:
            freeBlocks.append((None, freeBlockStartIndex, DISK_SIZE - freeBlockStartIndex))

    #raise Exception("getFreeBlocks: not implemented")
    #for block in memory_state:
    return freeBlocks


def getFragmentedPercs(state):
    # Create list of fragmented files
    fragmented = []
    seen = []

    for block in state:
        id = block[0]
        if id in seen and id not in fragmented:
            fragmented.append(id)
        elif id not in seen:
            seen.append(id)

    count_fragmented = 0
    size_fragmented = 0

    for block in state:
        id = block[0]
        if id in fragmented:
            size_fragmented += block[2]

    return (len(fragmented) / len(seen), size_fragmented / DISK_SIZE)

class NoFreeSpaceError(Exception):
    def __init__(self, request_id, states):
        # Set some exception infomation
        self.msg = "file request {0} is larger than free file system size".format(request_id)