from malu.data_defs import *
import random

MEMORY_SIZE = 50

# One state is a list of tuples, where each tuple shows:
# (process ID, duration left, start index, size)

def allocate(requests, algo):       # first-fit
    states = []
    states.append([])           # initially memory is empty
    t = 0

    current_state = []
    for r in requests:
        #print(r)
        if r[1] > MEMORY_SIZE:
            raise MemoryRequestTooLargeError(r[0], removeDuplicateStates(states))
            # or instead return some special value, e.g. None?
        while True:

            freeBlocks = getFreeBlocks(current_state, MEMORY_SIZE)  # get free blocks

            #print("free blocks: ", end="")
            #print(freeBlocks)

            # check if any block would fit at all
            freeBlocksSorted = list(reversed(sortBlocksByField(freeBlocks, "size")))          # reverse because otherwise we sort smaller -> larger, but we want vice versa
            #print("sorted:      ", end="")
            #print(freeBlocksSorted)

            if not freeBlocks or freeBlocksSorted[0][3] < r[1]:
                # if did not fit in any block, then move one timestep forward
                t += 1
                current_state = oneTimeStepForward(current_state)
                states.append(current_state[:])
            else:
                # depending on method chosen, pick free block
                if algo == "FF":
                    chosenFreeBlock = filterBlocksByField(sortBlocksByField(freeBlocks, "start index"), "size", lambda a: a >= r[1])[0]
                elif algo == "BF":
                    chosenFreeBlock = filterBlocksByField(sortBlocksByField(freeBlocks, "size"), "size", lambda a: a >= r[1])[0]
                elif algo == "WF":
                    chosenFreeBlock = filterBlocksByField(reversed(sortBlocksByField(freeBlocks, "size")), "size", lambda a: a >= r[1])[0]
                else:        #RF
                    possibleBlocks = filterBlocksByField(sortBlocksByField(freeBlocks, "start index"), "size", lambda a: a >= r[1])
                    chosenFreeBlock = possibleBlocks[random.randint(0,len(possibleBlocks)-1)]

                newMemoryBlock = (r[0], r[2], chosenFreeBlock[2], r[1])
                current_state.append(newMemoryBlock)
                states.append(current_state[:])                # remember that we updated the state
                #print("current state: ", end="")
                #print(current_state)
                break

    return removeDuplicateStates(states)

def allocate_FF(requests):
    return allocate(requests, "FF")

def allocate_BF(requests):       # best-fit
    return allocate(requests, "BF")

def allocate_WF(requests):       # worst-fit
    return allocate(requests, "WF")

def allocate_RF(requests):       # random-fit
    return allocate(requests, "RF")

#allocate_FF(testPatternToArray(preDefPattern(0)))
#print(allocate_FF(testPatternToArray(preDefPattern(1))))

class MemoryRequestTooLargeError(Exception):
    def __init__(self, request_id, states):
        # Set some exception infomation
        self.msg = "memory request {0} is larger than whole memory size".format(request_id)