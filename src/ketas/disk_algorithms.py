from ketas.data_defs import *

#input: list of requests in order of arrival
#output: list of landmarks where disk head was at

def run_FCFS(requests, start):
    return requests

def run_SSTF(requests, start):
    result = []
    head_current = start
    while requests:
        # find closest to current
        dist = lambda x: abs(x - head_current)
        smallest_distance = min(list(map(dist, requests)))
        closest = list(filter(lambda x: dist(x) == smallest_distance, requests))[0]
        # add it to result
        result.append(closest)
        # remove it from requests
        requests.remove(closest)
        # update head_current
        head_current = closest
    return result

def run_SCAN(requests, start):
    left_to_right = sorted(list(filter(lambda x: x >= start, requests)))
    right_to_left = sorted(list(filter(lambda x: x < start, requests)), reverse=True)
    addition = []
    print(left_to_right[-1])
    if(left_to_right)[-1] != MAX_INDEX - 1:
        addition.append(MAX_INDEX - 1)
    return left_to_right + addition + right_to_left

def run_LOOK(requests, start):
    left_to_right = list(filter(lambda x: x >= start, requests))
    right_to_left = list(filter(lambda x: x < start, requests))
    return sorted(left_to_right) + sorted(right_to_left, reverse=True)

def run_CSCAN(requests, start):
    left_to_right = sorted(list(filter(lambda x: x >= start, requests)))
    right_to_left = sorted(list(filter(lambda x: x < start, requests)))
    addition = []
    if(left_to_right)[-1] != MAX_INDEX - 1:
        addition.append(MAX_INDEX - 1)
    if(right_to_left)[0] != 0:
        addition.append(0)
    return left_to_right + addition + right_to_left


def run_CLOOK(requests, start):
    run1 = list(filter(lambda x: x >= start, requests))
    run2 = list(filter(lambda x: x < start, requests))
    return sorted(run1) + sorted(run2)