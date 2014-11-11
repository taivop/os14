from malu.data_defs import *

MEMORY_SIZE = 50

# One state is a list of tuples, where each tuple shows:
# (process ID, duration left, start index, size)

def allocate_FF(requests):       # first-fit
    states = []
    states.append([])           # initially memory is empty
    t = 0

    current_state = []
    for r in requests:
        #print(r)
        if r[1] > MEMORY_SIZE:
            raise Exception("memory request larger than whole memory size")
            # or instead return some special value, e.g. None?
        while True:
            print("current state: ", end="")
            print(current_state)
            freeBlocks = getFreeBlocks(current_state, MEMORY_SIZE)  # get free blocks

            # check if any block would fit at all
            freeBlocksSorted = sortBlocksByField(freeBlocks, "size")

            if freeBlocksSorted[0][3] < r[1]:
                # if did not fit in any block, then move one timestep forward
                t += 1
                current_state = oneTimeStepForward(current_state)
            else:
                #print(list(sortBlocksByField(freeBlocks, "start index")))
                chosenFreeBlock = filterBlocksByField(sortBlocksByField(freeBlocks, "start index"), "size", lambda a: a >= r[1])[0]
                #TODO fill the block (and add to 'states'?)
                newMemoryBlock = (r[0], r[2], chosenFreeBlock[2], r[1])
                current_state.append(newMemoryBlock)
                states.append(current_state)                # remember that we updated the state
                break


    return states


def allocate_BF(requests):       # best-fit
    return None

def allocate_WF(requests):       # worst-fit
    return None

def allocate_RF(requests):       # random-fit
    return None

allocate_FF(testPatternToArray(preDefPattern(0)))
#print(allocate_FF(testPatternToArray(preDefPattern(1))))