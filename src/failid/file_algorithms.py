from failid.data_defs import *

#input: list of files
#output: list of states, where each state is a list of tuples (file_id, start_index, size)

def allocateFiles(requests):
    states = []

    currentState = []

    for request in requests:
        states.append(currentState[:])

        file_id = request[0]
        file_size = request[1]

        if file_size == -1:                     # if got file delete command, delete all occurrences of this file
            for block in currentState:
                if block[0] == file_id:
                    currentState.remove(block)
        else:                                   # got file add command
            currentState = sortBlocksByStartIndex(currentState)
            if not currentState:        # no blocks allocated
                currentState.append((file_id, 0, file_size))
            else:
                size_remaining = file_size

                while size_remaining > 0:
                    freeBlocks = getFreeBlocks(currentState, DISK_SIZE)
                    if not freeBlocks:
                        raise NoFreeSpaceError(file_id, states)
                    else:
                        chosenFreeBlock = freeBlocks[0]
                        if chosenFreeBlock[2] >= size_remaining:        # free block is larger than needed
                            blockToAdd = (file_id, chosenFreeBlock[1], size_remaining)
                            currentState.append(blockToAdd)
                            size_remaining = 0
                        else:
                            blockToAdd = (file_id, chosenFreeBlock[1], chosenFreeBlock[2])
                            currentState.append(blockToAdd)
                            size_remaining -= chosenFreeBlock[2]

    states.append(currentState[:])

    return states

