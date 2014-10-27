from data_defs import *

# Define some lambdas
mean = lambda a: sum(a) / len(a)
wait_times = lambda ar, st: [st[i]-ar[i] for i in range(0,len(ar))]

# INPUT
# list of tuples (id, arrive_time, duration)
# OUTPUT: list 'started', real 'avg_wait_time'
# started[0] shows at what time the process with ID 0 was started
# avg_wait_time shows the average wait time of a process

def startTimesToOccupations(processes):
    occupations = []
    processes = sortProcessesByField(processes, "start_time")

    for p in processes:
        occupations.append((p[0], p[3], p[3] + p[2]))

    return occupations

def allocate_FCFS(processes):
    allocated = FCFS_recurs(sortProcessesByField(processes[:], "arrive_time"), [], 0)
    return startTimesToOccupations(allocated)

def FCFS_recurs(processes, allocated, t):
    if len(processes) == 1:     # recursion base
        return allocated + [addStartTime(processes[0], t)]
    else:                       # recursion step
        p = processes[0]
        if t < p[1]:            # if we are not yet at the time point where process should start
            t = p[1]
            return FCFS_recurs(processes, allocated, t)
        else:
            return FCFS_recurs(processes[1:], allocated + [addStartTime(p, t)], t + p[2])

def allocate_SJF(processes):
    allocated = SJF_recurs(processes[:], [], 0)
    return startTimesToOccupations(allocated)

def SJF_recurs(processes, allocated, t):
    # mitteväljatõrjuv variant

    if len(processes) == 1:     # recursion base
        return allocated + [addStartTime(processes[0], t)]
    else:                       # recursion step
        # get shortest process
        processes = sortProcessesByField(processes, "duration")
        shortestProcess = processes[0]
        #print("shortest process is: " + str(shortestProcess))
        if t < shortestProcess[1]:            # if we are not at the start time of the shortest job yet
            # find all processes that we could start before the arrival of the shortest process
            possibleToStart = filterProcessesByField(processes, "arrive_time", lambda x: x < shortestProcess[1])

            if not possibleToStart:
                # no processes until shortest job -> advance to time of shortest job
                return SJF_recurs(processes, allocated, shortestProcess[1])

            # get the first one available, if several, get shortest
            nextProcess = sortProcessesByField(sortProcessesByField(possibleToStart, "duration"), "arrive_time")[0]
            #print("\tdoing shortest job between now and actual shortest: " + str(nextProcess))
            processes.remove(nextProcess)
            return SJF_recurs(processes, allocated + [addStartTime(nextProcess, t)], t + nextProcess[2])
        else:                   # we can do the shortest job
            #print("\tdoing shortest job: " + str(shortestProcess))
            processes.remove(shortestProcess)
            return SJF_recurs(processes, allocated + [addStartTime(shortestProcess, t)], t + shortestProcess[2])


def allocate_RR(processes):
    return RR_loop(processes)

def RR_loop(processes):
    quant = 4
    processor_occupations = [] # list of tuples (id, start, end) to keep track of what process was done; -1 is IDLE

    # for each process, keep track of how much of it we still have to do
    t = 0
    while processes:
        # filter out all processes that are currently available
        available = filterProcessesByField(processes, "arrive_time", lambda x: x <= t)

        if not available:
            closest_process_start = sortProcessesByField(processes, "arrive_time")[0][1]
            processor_occupations.append((-1, t, closest_process_start))
            t = closest_process_start
            continue

        # take a random process from there
        process = available[0]
        if process[2] <= quant:          # if this process is shorter than quant
            processes.remove(process)
            processor_occupations.append((process[0], t, t + process[2]))
            t += process[2]
        else:                            # this process is longer than quant
            processes.remove(process)
            process_new = decreaseDuration(process, quant)
            processes.append(process_new)
            processor_occupations.append((process[0], t, t + quant))
            t += quant

    return processor_occupations

def allocate_MLQ(processes):
    return MLQ_loop(processes)

def MLQ_loop(processes):
    processor_occupations = []

    q0 = []
    q1 = []
    q2 = []

    quant_q0 = 8
    quant_q1 = 8

    t = 0

    while (q0 or q1 or q2) or processes:    # while there are processes in any of the queues or any not done
        # get all processes that arrived now
        arrivedProcesses = filterProcessesByField(processes, "arrive_time", lambda x: x <= t)
        for p in arrivedProcesses:          # append all new processes to q0 and remove from original list
            processes.remove(p)
            q0.append(p)

        if not (q0 or q1 or q2):            # if nothing to do right now
            t += 1                          # step one millisecond forward
            continue
        else:
            if q0:
                p = q0.pop(0)               # take first process from q0
                if p[2] <= quant_q0:        # if this process is doable in time limit
                    processor_occupations.append((p[0], t, t+p[2]))
                    t += p[2]
                    continue
                else:
                    processor_occupations.append((p[0], t, t+quant_q0))     # do this process for quant_q0 ms
                    q1.append(decreaseDuration(p, quant_q0))                # append it to q1
                    t += quant_q0
                    continue
            elif q1:                        # if no processes in q0 but some in q1
                p = q1.pop(0)               # take first process from q1
                if p[2] <= quant_q1:        # if it is doable in time limit
                    processor_occupations.append((p[0], t, t+p[2]))
                    t += p[2]
                    continue
                else:
                    processor_occupations.append((p[0], t, t+quant_q1))     # do this process for quant_q1 ms
                    q2.append(decreaseDuration(p, quant_q1))                # append it to q2
                    t += quant_q1
                    continue
            else:                           # there has to be a process in q2
                p = q2.pop(0)
                if processor_occupations[-1][0] == p[0]:    # if p was also the last process we did
                    last_occupation = processor_occupations.pop()
                    new_occupation = increaseOccupationDuration(last_occupation, 1)
                    processor_occupations.append(new_occupation)
                    if p[2] > 1:                           # if we did not complete the process, re-insert
                        q2.insert(0, decreaseDuration(p, 1))
                    t += 1
                    continue
                else:
                    occupation = (p[0], t, t+1)
                    processor_occupations.append(occupation)
                    if p[2] > 1:                           # if we did not complete the process, re-insert
                        q2.insert(0, decreaseDuration(p, 1))
                    t += 1
                    continue

    return processor_occupations




#processes = testPatternToArray("0,10;4,5;12,4")
#processes2 = testPatternToArray("0,7;2,4;4,1;5,4")
#processes3 = testPatternToArray("0,24;0,3;22,3")
#print(processes3)
#print(allocate_MLQ(processes3))
#print(startTimesToOccupations(allocate_FCFS(processes)))