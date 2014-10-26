from parse import *

# Define some lambdas
mean = lambda a: sum(a) / len(a)
wait_times = lambda ar, st: [st[i]-ar[i] for i in range(0,len(ar))]

# INPUT
# list of tuples (id, arrive_time, duration)
# OUTPUT: list 'started', real 'avg_wait_time'
# started[0] shows at what time the process with ID 0 was started
# avg_wait_time shows the average wait time of a process

def addStartTime(p, start_time):
    l = list(p)
    l.append(start_time)
    return tuple(l)

def allocate_FCFS(processes):
    allocated = FCFS_recurs(sortProcessesByField(processes[:], "arrive_time"), [], 0)
    return allocated

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
    return allocated

def SJF_recurs(processes, allocated, t):
    # mitteväljatõrjuv variant

    if len(processes) == 1:     # recursion base
        return allocated + [addStartTime(processes[0], t)]
    else:                       # recursion step
        # get shortest process
        processes = sortProcessesByField(processes, "duration")
        shortestProcess = processes[0]
        print("shortest process is: " + str(shortestProcess))
        if t < shortestProcess[1]:            # if we are not at the start time of the shortest job yet
            nearestProcess = sortProcessesByField(processes, "arrive_time")[0]       # get nearest job
            if nearestProcess[1] <= t:                                              # if we can already do nearest job
                print("\tdoing nearest job: " + str(nearestProcess))
                processes.remove(nearestProcess)
                return SJF_recurs(processes, allocated + [addStartTime(nearestProcess, t)], t + nearestProcess[2])
            else:
                return SJF_recurs(processes, allocated, nearestProcess[1])          # advance time to nearest job
        else:                   # we can do the shortest job
            print("\tdoing shortest job: " + str(shortestProcess))
            processes.remove(shortestProcess)
            return SJF_recurs(processes, allocated + [addStartTime(shortestProcess, t)], t + shortestProcess[2])





processes = testPatternToArrays("0,10;4,5;12,4")
processes2 = testPatternToArrays("0,10;0,5;22,4")
print(allocate_SJF(processes2))